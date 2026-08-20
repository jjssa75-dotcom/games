from __future__ import annotations

import copy
import heapq
import random
from dataclasses import dataclass

from .actions import AttackAction, CommandAction, EndActivationAction, MoveAction, SetModeAction, UseAbilityAction
from .model import AbilityDefinition, BattleState, Catalog, CommanderState, IMPASSABLE_TERRAIN, Mode, Side, UnitState


class InvalidAction(ValueError):
    """A ação viola uma regra; o estado e o RNG permanecem inalterados."""


@dataclass(frozen=True)
class Resolution:
    state: BattleState
    events: tuple[str, ...]


class ActionResolver:
    """Autoridade única para preview, IA futura e aplicação de ações."""

    def __init__(self, catalog: Catalog, seed: int = 0):
        self.catalog = catalog
        self.rng = random.Random(seed)

    def preview(self, state: BattleState, action) -> Resolution:
        rng_state = self.rng.getstate()
        try:
            return self._resolve(copy.deepcopy(state), action)
        finally:
            self.rng.setstate(rng_state)

    def apply(self, state: BattleState, action) -> Resolution:
        rng_state = self.rng.getstate()
        try:
            return self._resolve(copy.deepcopy(state), action)
        except Exception:
            self.rng.setstate(rng_state)
            raise

    def _resolve(self, state: BattleState, action) -> Resolution:
        if state.winner is not None:
            raise InvalidAction("A batalha já terminou")
        actor = self._actor(state, action.actor_id)
        event_start = len(state.events)
        ends_activation = not isinstance(action, MoveAction)
        if isinstance(action, MoveAction):
            if actor.movement_spent:
                raise InvalidAction("Movimento já utilizado nesta ativação")
            self._move(state, actor, action.destination)
            actor.movement_spent = True
            state.current_actor_id = actor.instance_id
        elif isinstance(action, AttackAction):
            self._require_action(actor)
            self._attack(state, actor, action.target_id)
        elif isinstance(action, SetModeAction):
            self._require_action(actor)
            self._set_mode(state, actor, action.mode)
        elif isinstance(action, CommandAction):
            self._require_action(actor)
            self._command(state, actor, action)
        elif isinstance(action, UseAbilityAction):
            self._require_action(actor)
            self._use_ability(state, actor, action)
        elif isinstance(action, EndActivationAction):
            if not actor.movement_spent:
                raise InvalidAction("Só é possível encerrar manualmente após mover")
            state.events.append(f"{actor.instance_id} encerrou a ativação")
        else:
            raise InvalidAction("Tipo de ação desconhecido")
        if ends_activation:
            actor.action_spent = not isinstance(action, EndActivationAction)
            actor.activated = True
            state.current_actor_id = None
        self._update_winner(state)
        if state.winner is None and ends_activation:
            self._advance_side(state)
        return Resolution(state, tuple(state.events[event_start:]))

    def _actor(self, state: BattleState, actor_id: str) -> UnitState:
        actor = state.units.get(actor_id)
        if actor is None or not actor.alive:
            raise InvalidAction("Ator inexistente ou derrotado")
        if actor.side != state.active_side:
            raise InvalidAction("Não é o lado ativo")
        if actor.activated:
            raise InvalidAction("Unidade já ativada nesta rodada")
        if state.current_actor_id is not None and state.current_actor_id != actor_id:
            raise InvalidAction("Outra unidade já iniciou a ativação")
        return actor

    @staticmethod
    def _require_action(actor: UnitState):
        if actor.action_spent:
            raise InvalidAction("Ação principal já utilizada nesta ativação")

    def _definition(self, unit: UnitState):
        return self.catalog.commanders.get(unit.definition_id) or self.catalog.units[unit.definition_id]

    @staticmethod
    def _distance(a: tuple[int, int], b: tuple[int, int]) -> int:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    @staticmethod
    def _enemy(side: Side) -> Side:
        return Side.RED if side == Side.BLUE else Side.BLUE

    @staticmethod
    def _in_bounds(state: BattleState, position: tuple[int, int]) -> bool:
        return 0 <= position[0] < state.board_width and 0 <= position[1] < state.board_height

    def _move(self, state: BattleState, actor: UnitState, destination: tuple[int, int], limit: int | None = None):
        definition = self._definition(actor)
        movement = definition.movement + self._modifier(actor, "movement") if limit is None else limit
        if destination == actor.position:
            raise InvalidAction("Movimento precisa alterar a posição")
        if not self._in_bounds(state, destination):
            raise InvalidAction("Destino fora do tabuleiro")
        if self._hard_blocked(state, destination):
            raise InvalidAction("Terreno intransponível")
        occupied = {unit.position for unit in state.units.values() if unit.alive and unit.instance_id != actor.instance_id}
        if destination in occupied:
            raise InvalidAction("Casa ocupada")
        if destination not in self._movement_map(state, actor, movement, occupied):
            raise InvalidAction("Destino sem caminho dentro do movimento")
        actor.position = destination
        state.events.append(f"{actor.instance_id} moveu para {destination}")

    def reachable_positions(self, state: BattleState, actor_id: str) -> dict[tuple[int, int], int]:
        """Destinos legais e seus custos, usados por interface, IA e testes."""
        actor = self._actor(state, actor_id)
        if actor.movement_spent:
            return {}
        occupied = {
            unit.position
            for unit in state.units.values()
            if unit.alive and unit.instance_id != actor.instance_id
        }
        movement = self._definition(actor).movement + self._modifier(actor, "movement")
        return {
            position: cost
            for position, cost in self._movement_map(state, actor, movement, occupied).items()
            if position != actor.position
        }

    def _movement_map(self, state, actor, movement, occupied) -> dict[tuple[int, int], int]:
        queue = [(0, actor.position)]
        best = {actor.position: 0}
        while queue:
            distance, position = heapq.heappop(queue)
            if distance != best[position] or distance >= movement:
                continue
            x, y = position
            for neighbor in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if neighbor in occupied or not self._in_bounds(state, neighbor) or self._hard_blocked(state, neighbor):
                    continue
                new_distance = distance + self._movement_cost(state, actor, neighbor)
                if new_distance <= movement and new_distance < best.get(neighbor, movement + 1):
                    best[neighbor] = new_distance
                    heapq.heappush(queue, (new_distance, neighbor))
        return best

    @staticmethod
    def _hard_blocked(state: BattleState, position: tuple[int, int]) -> bool:
        return position in state.blocked or state.terrain.get(position) in IMPASSABLE_TERRAIN

    def _movement_cost(self, state: BattleState, actor: UnitState, position: tuple[int, int]) -> int:
        tile = state.terrain.get(position, ".")
        tags = set(self._definition(actor).tags)
        if "flying" in tags:
            return 1
        if tile == "F" and "forestwise" not in tags:
            return 2
        if tile == "~" and not ({"amphibious", "desertwise"} & tags):
            return 2
        if tile == "M" and "mountainwise" not in tags:
            return 2
        return 1

    def _attack(self, state, actor, target_id, *, damage_bonus=0, armor_piercing=0) -> bool:
        target = state.units.get(target_id)
        if target is None or not target.alive or target.side == actor.side:
            raise InvalidAction("Alvo inválido")
        actor_def = self._definition(actor)
        if self._distance(actor.position, target.position) > actor_def.attack_range:
            raise InvalidAction("Alvo fora de alcance")
        if not self._roll_hit(actor, target):
            state.events.append(f"{actor.instance_id} errou {target.instance_id}")
            return False
        self._deal_damage(
            state,
            actor,
            target,
            damage_bonus=damage_bonus,
            armor_piercing=actor_def.armor_piercing + armor_piercing,
            label="causou",
        )
        self._counter_reaction(state, attacker=actor, defender=target)
        return True

    def _roll_hit(self, actor: UnitState, target: UnitState) -> bool:
        actor_def = self._definition(actor)
        target_def = self._definition(target)
        chance = max(5, min(95, actor_def.accuracy + self._modifier(actor, "accuracy") - target_def.evasion))
        return self.rng.randrange(100) < chance

    def _deal_damage(self, state, attacker, defender, *, damage_bonus=0, armor_piercing=0, label="causou") -> int:
        attacker_def = self._definition(attacker)
        defender_def = self._definition(defender)
        attack_mode = 2 if attacker.mode == Mode.ATTACK else 0
        defense_mode = 2 if defender.mode == Mode.DEFENSE else 0
        cover = 2 if self._distance(attacker.position, defender.position) > 1 and state.terrain.get(defender.position) == "F" else 0
        elevation = 1 if state.terrain.get(attacker.position) == "M" and state.terrain.get(defender.position) != "M" else 0
        effective_defense = max(0, defender_def.defense + defense_mode + cover + self._modifier(defender, "defense") - armor_piercing)
        damage = max(1, attacker_def.attack + attack_mode + elevation + damage_bonus - effective_defense)
        defender.hp = max(0, defender.hp - damage)
        state.events.append(f"{attacker.instance_id} {label} {damage} em {defender.instance_id}")
        if not defender.alive:
            state.events.append(f"{defender.instance_id} foi derrotado")
        return damage

    def _counter_reaction(self, state, attacker, defender):
        if not attacker.alive or not defender.alive or not defender.reaction_available:
            return
        if self._distance(attacker.position, defender.position) > self._definition(defender).attack_range:
            return
        defender.reaction_available = False
        self._deal_damage(state, defender, attacker, label="reagiu por")

    def _set_mode(self, state, actor, mode):
        if mode not in self._definition(actor).allowed_modes:
            raise InvalidAction("Modo não permitido")
        if mode == actor.mode:
            raise InvalidAction("Unidade já está nesse modo")
        actor.mode = mode
        state.events.append(f"{actor.instance_id} adotou {mode.value}")

    def _command(self, state, actor, action):
        if not isinstance(actor, CommanderState):
            raise InvalidAction("Somente comandantes emitem comandos")
        definition = self.catalog.commanders[actor.definition_id]
        if action.ability_id not in definition.abilities:
            raise InvalidAction("Comando não conhecido")
        ability = self.catalog.abilities[action.ability_id]
        if ability.kind != "command" or actor.cmd < ability.cmd_cost:
            raise InvalidAction("Comando inválido ou CMD insuficiente")
        if not action.target_ids or len(action.target_ids) != len(set(action.target_ids)):
            raise InvalidAction("Alvos de comando vazios ou duplicados")
        if len(action.target_ids) > ability.max_targets:
            raise InvalidAction("Comando excede o limite de alvos")
        targets = [state.units.get(instance_id) for instance_id in action.target_ids]
        if any(target is None or not target.alive or target.commander_id != actor.instance_id for target in targets):
            raise InvalidAction("Comando só afeta tropas vivas vinculadas")
        if any(self._distance(actor.position, target.position) > definition.command_range for target in targets):
            raise InvalidAction("Tropa fora do alcance de comando")
        actor.cmd -= ability.cmd_cost
        for target in targets:
            target.status[action.ability_id] = ability.duration_rounds
            target.morale = max(0, min(100, target.morale + dict(ability.modifiers).get("morale", 0)))
        state.events.append(f"{actor.instance_id} usou {ability.name} em {len(targets)} tropa(s)")

    def _use_ability(self, state, actor, action):
        definition = self._definition(actor)
        if action.ability_id not in definition.abilities:
            raise InvalidAction("Habilidade não conhecida")
        ability = self.catalog.abilities[action.ability_id]
        if ability.kind == "command":
            raise InvalidAction("Use CommandAction para comandos")
        if ability.mechanic == "prepare_lance":
            if action.target_id is not None or action.destination is not None:
                raise InvalidAction("Preparar Lança não recebe alvo ou destino")
            actor.status[ability.id] = ability.duration_rounds
            state.events.append(f"{actor.instance_id} preparou a lança")
        elif ability.mechanic == "charge":
            self._charge(state, actor, action, ability)
        elif ability.mechanic == "skirmish":
            self._skirmish(state, actor, action, ability)
        else:
            raise InvalidAction("Mecânica de habilidade não implementada")

    def _charge(self, state, actor, action, ability: AbilityDefinition):
        if action.target_id is None or action.destination is None:
            raise InvalidAction("Investida exige alvo e destino")
        distance = self._distance(actor.position, action.destination)
        if distance < ability.min_move:
            raise InvalidAction("Investida sem distância mínima")
        self._move(state, actor, action.destination)
        self._prepared_lance_reactions(state, actor)
        if not actor.alive:
            state.events.append(f"A investida de {actor.instance_id} foi interrompida")
            return
        bonus = ability.damage_bonus + max(0, distance - ability.min_move)
        if state.terrain.get(action.destination) in {"F", "~"}:
            bonus = max(0, bonus - 2)
            state.events.append("O terreno reduziu o impacto da investida")
        self._attack(state, actor, action.target_id, damage_bonus=bonus, armor_piercing=ability.armor_piercing)

    def _prepared_lance_reactions(self, state, cavalry):
        if "cavalry" not in self._definition(cavalry).tags:
            return
        candidates = sorted(
            (
                unit
                for unit in state.units.values()
                if unit.alive
                and unit.side != cavalry.side
                and unit.reaction_available
                and "preparar_lanca" in unit.status
                and self._distance(unit.position, cavalry.position) <= self._definition(unit).attack_range
            ),
            key=lambda unit: unit.instance_id,
        )
        for lancer in candidates:
            lancer.reaction_available = False
            lancer.status.pop("preparar_lanca", None)
            ability = self.catalog.abilities["preparar_lanca"]
            self._deal_damage(
                state,
                lancer,
                cavalry,
                damage_bonus=ability.damage_bonus,
                armor_piercing=ability.armor_piercing,
                label="interceptou por",
            )
            if not cavalry.alive:
                break

    def _skirmish(self, state, actor, action, ability: AbilityDefinition):
        if action.target_id is None or action.destination is None:
            raise InvalidAction("Escaramuça exige alvo e reposicionamento")
        self._attack(state, actor, action.target_id, damage_bonus=ability.damage_bonus, armor_piercing=ability.armor_piercing)
        if actor.alive:
            self._move(state, actor, action.destination, limit=ability.max_reposition)

    def _modifier(self, unit, stat):
        return sum(
            dict(self.catalog.abilities[ability_id].modifiers).get(stat, 0)
            for ability_id, rounds in unit.status.items()
            if rounds > 0
        )

    def _update_winner(self, state):
        commanders = [unit for unit in state.units.values() if isinstance(unit, CommanderState)]
        alive_commanders = {unit.side for unit in commanders if unit.alive}
        if Side.BLUE not in alive_commanders:
            self._declare_winner(state, Side.RED)
            return
        if Side.RED not in alive_commanders:
            self._declare_winner(state, Side.BLUE)
            return

        if state.victory_condition == "escort":
            escort = state.units.get(state.escort_unit_id or "")
            if escort is None or not escort.alive:
                self._declare_winner(state, Side.RED)
            elif state.escort_exit is not None and escort.position == state.escort_exit:
                self._declare_winner(state, Side.BLUE)
        elif state.victory_condition == "intercept":
            target = state.units.get(state.intercept_unit_id or "")
            if target is None or not target.alive:
                self._declare_winner(state, Side.BLUE)
            elif state.intercept_exit is not None and target.position == state.intercept_exit:
                self._declare_winner(state, Side.RED)

    @staticmethod
    def _declare_winner(state: BattleState, side: Side):
        if state.winner is None:
            state.winner = side
            state.events.append(f"Vitória do lado {side.value}")

    def _advance_side(self, state):
        enemy = self._enemy(state.active_side)
        if any(unit.alive and not unit.activated and unit.side == enemy for unit in state.units.values()):
            state.active_side = enemy
        elif not any(unit.alive and not unit.activated for unit in state.units.values()):
            self._new_round(state)

    def _new_round(self, state):
        state.round_number += 1
        self._score_round_objectives(state)
        self._update_winner(state)
        if state.winner is not None:
            return
        state.round_starter = self._enemy(state.round_starter)
        state.active_side = state.round_starter
        state.current_actor_id = None
        for unit in state.units.values():
            unit.activated = False
            unit.movement_spent = False
            unit.action_spent = False
            unit.reaction_available = True
            unit.status = {ability_id: rounds - 1 for ability_id, rounds in unit.status.items() if rounds > 1}
            if isinstance(unit, CommanderState):
                definition = self.catalog.commanders[unit.definition_id]
                unit.cmd = min(definition.cmd_max, unit.cmd + definition.cmd_regen)

    def _score_round_objectives(self, state: BattleState):
        if state.victory_condition == "survive" and state.round_limit is not None:
            if state.round_number > state.round_limit:
                self._declare_winner(state, Side.BLUE)
                return
        elif state.victory_condition == "control_area":
            blue_controls = any(
                unit.alive and unit.side == Side.BLUE and unit.position in state.objective_tiles
                for unit in state.units.values()
            )
            red_contests = any(
                unit.alive and unit.side == Side.RED and unit.position in state.objective_tiles
                for unit in state.units.values()
            )
            state.control_progress = state.control_progress + 1 if blue_controls and not red_contests else 0
            state.events.append(f"Controle do objetivo: {state.control_progress}/{state.control_required}")
            if state.control_required > 0 and state.control_progress >= state.control_required:
                self._declare_winner(state, Side.BLUE)
                return

        if (
            state.round_limit is not None
            and state.round_number > state.round_limit
            and state.victory_condition in {"control_area", "escort", "intercept"}
        ):
            self._declare_winner(state, Side.RED)
