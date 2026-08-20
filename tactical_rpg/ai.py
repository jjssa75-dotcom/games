from __future__ import annotations

from dataclasses import dataclass

from .actions import AttackAction, CommandAction, EndActivationAction, MoveAction, SetModeAction, UseAbilityAction
from .model import BattleState, CommanderState, Mode, Side, UnitState
from .resolver import ActionResolver, InvalidAction


@dataclass(frozen=True)
class ScoredAction:
    score: float
    tie_breaker: str
    action: object


class TacticalAI:
    """Planejador determinístico que usa apenas estado visível e ações legais."""

    def __init__(self, resolver: ActionResolver):
        self.resolver = resolver

    def choose_action(self, state: BattleState, side: Side | None = None):
        side = side or state.active_side
        if state.winner is not None or side != state.active_side:
            raise InvalidAction("IA chamada fora do lado ativo")
        actors = sorted(
            (
                unit for unit in state.units.values()
                if unit.side == side
                and unit.alive
                and not unit.activated
                and (state.current_actor_id is None or unit.instance_id == state.current_actor_id)
            ),
            key=lambda unit: unit.instance_id,
        )
        if not actors:
            raise InvalidAction("IA sem unidade disponível")
        scored = []
        for actor in actors:
            for action in self._candidate_actions(state, actor):
                try:
                    resolution = self.resolver.preview(state, action)
                except InvalidAction:
                    continue
                scored.append(ScoredAction(self._score(state, resolution.state, actor, action), repr(action), action))
        if not scored:
            raise InvalidAction("IA não encontrou ação legal")
        return max(scored, key=lambda item: (item.score, item.tie_breaker)).action

    def _candidate_actions(self, state: BattleState, actor: UnitState):
        definition = self.resolver._definition(actor)
        enemies = sorted(
            (unit for unit in state.units.values() if unit.side != actor.side and unit.alive),
            key=lambda unit: unit.instance_id,
        )
        for target in enemies:
            yield AttackAction(actor.instance_id, target.instance_id)
        for mode in Mode:
            if mode != actor.mode and mode in definition.allowed_modes:
                yield SetModeAction(actor.instance_id, mode)
        if isinstance(actor, CommanderState):
            yield from self._command_actions(state, actor)
        for ability_id in definition.abilities:
            ability = self.resolver.catalog.abilities[ability_id]
            if ability.mechanic == "prepare_lance":
                yield UseAbilityAction(actor.instance_id, ability_id)
            elif ability.mechanic == "charge":
                yield from self._charge_actions(state, actor, enemies, ability)
            elif ability.mechanic == "skirmish":
                yield from self._skirmish_actions(state, actor, enemies, ability)
        if not actor.movement_spent:
            yield from self._move_actions(state, actor, enemies)
        else:
            yield EndActivationAction(actor.instance_id)

    def _move_actions(self, state: BattleState, actor: UnitState, enemies: list[UnitState]):
        definition = self.resolver._definition(actor)
        destinations = list(self.resolver.reachable_positions(state, actor.instance_id))

        def priority(position):
            if state.victory_condition == "intercept" and actor.instance_id == state.intercept_unit_id and state.intercept_exit:
                strategic = self.resolver._distance(position, state.intercept_exit)
            elif state.victory_condition == "control_area" and state.objective_tiles:
                strategic = min(self.resolver._distance(position, tile) for tile in state.objective_tiles)
            elif state.victory_condition == "escort" and state.escort_unit_id and actor.side == Side.RED:
                escort = state.units.get(state.escort_unit_id)
                strategic = self.resolver._distance(position, escort.position) if escort and escort.alive else 0
            elif enemies:
                nearest = min(self.resolver._distance(position, unit.position) for unit in enemies)
                strategic = abs(nearest - max(1, definition.attack_range))
            else:
                strategic = 0
            return strategic, position[1], position[0]

        for destination in sorted(destinations, key=priority)[:16]:
            yield MoveAction(actor.instance_id, destination)

    def _command_actions(self, state, actor):
        definition = self.resolver.catalog.commanders[actor.definition_id]
        linked = sorted(
            (
                unit
                for unit in state.units.values()
                if unit.commander_id == actor.instance_id
                and unit.alive
                and self.resolver._distance(actor.position, unit.position) <= definition.command_range
            ),
            key=lambda unit: unit.instance_id,
        )
        for ability_id in definition.abilities:
            ability = self.resolver.catalog.abilities[ability_id]
            if ability.kind == "command" and actor.cmd >= ability.cmd_cost and linked:
                targets = tuple(unit.instance_id for unit in linked[: ability.max_targets])
                yield CommandAction(actor.instance_id, ability_id, targets)

    def _charge_actions(self, state, actor, enemies, ability):
        for target in enemies:
            tx, ty = target.position
            for destination in ((tx+1,ty),(tx-1,ty),(tx,ty+1),(tx,ty-1)):
                yield UseAbilityAction(actor.instance_id, ability.id, target.instance_id, destination)

    def _skirmish_actions(self, state, actor, enemies, ability):
        for target in enemies:
            for y in range(max(0,actor.position[1]-ability.max_reposition), min(state.board_height,actor.position[1]+ability.max_reposition+1)):
                for x in range(max(0,actor.position[0]-ability.max_reposition), min(state.board_width,actor.position[0]+ability.max_reposition+1)):
                    yield UseAbilityAction(actor.instance_id, ability.id, target.instance_id, (x,y))

    def _score(self, before: BattleState, after: BattleState, actor: UnitState, action) -> float:
        side = actor.side
        enemy = Side.RED if side == Side.BLUE else Side.BLUE
        own_before = sum(unit.hp for unit in before.units.values() if unit.side == side)
        own_after = sum(unit.hp for unit in after.units.values() if unit.side == side)
        enemy_before = sum(unit.hp for unit in before.units.values() if unit.side == enemy)
        enemy_after = sum(unit.hp for unit in after.units.values() if unit.side == enemy)
        score = (enemy_before - enemy_after) * 14 - (own_before - own_after) * 10
        if isinstance(action, AttackAction) and enemy_after < enemy_before:
            score += 12
        if after.winner == side:
            score += 10000
        elif after.winner == enemy:
            score -= 10000
        for instance_id, old in before.units.items():
            new = after.units[instance_id]
            if old.alive and not new.alive:
                score += 900 if old.side == enemy else -800
                if isinstance(old, CommanderState):
                    score += 4000 if old.side == enemy else -4000
        if isinstance(action, CommandAction):
            score += 32 * len(action.target_ids)
        if isinstance(action, UseAbilityAction):
            score += 18
            if action.ability_id == "preparar_lanca":
                threat = any(
                    "cavalry" in self.resolver._definition(unit).tags
                    and self.resolver._distance(actor.position, unit.position) <= 5
                    for unit in before.units.values() if unit.side == enemy and unit.alive
                )
                score += 80 if threat else -25
        moved_actor = after.units[actor.instance_id]
        enemies = [unit for unit in after.units.values() if unit.side == enemy and unit.alive]
        if enemies and moved_actor.alive:
            nearest_enemy = min(self.resolver._distance(moved_actor.position, unit.position) for unit in enemies)
            own_commanders = [unit for unit in after.units.values() if unit.side == side and isinstance(unit, CommanderState) and unit.alive]
            commander_distance = min((self.resolver._distance(moved_actor.position, unit.position) for unit in own_commanders), default=0)
            role = self.resolver._definition(moved_actor).role
            if moved_actor.mode == Mode.ATTACK or role in {"assalto","ruptura","marcial"}:
                score -= nearest_enemy * 4
            elif moved_actor.mode == Mode.DEFENSE or role in {"defesa","linha","suporte"}:
                score -= commander_distance * 3
                score -= abs(nearest_enemy - 2)
            else:
                score -= nearest_enemy * 2
                score -= commander_distance
        if isinstance(action, SetModeAction):
            role = self.resolver._definition(actor).role
            preferred = Mode.DEFENSE if role in {"defesa","suporte"} else Mode.ATTACK if role in {"assalto","ruptura","marcial"} else Mode.FREE
            score += 8 if action.mode == preferred else -6
        if isinstance(action, EndActivationAction):
            score -= 30
        if moved_actor.alive and isinstance(action, MoveAction):
            if before.victory_condition == "intercept" and actor.instance_id == before.intercept_unit_id and before.intercept_exit:
                score -= self.resolver._distance(moved_actor.position, before.intercept_exit) * 18
            elif before.victory_condition == "control_area" and before.objective_tiles:
                score -= min(self.resolver._distance(moved_actor.position, tile) for tile in before.objective_tiles) * 10
            elif before.victory_condition == "escort" and before.escort_unit_id:
                escort = after.units.get(before.escort_unit_id)
                if escort and escort.alive and actor.side != escort.side:
                    score -= self.resolver._distance(moved_actor.position, escort.position) * 8
        return score
