from __future__ import annotations

import json
import threading
import urllib.request
import webbrowser
from dataclasses import replace
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from .actions import AttackAction, CommandAction, EndActivationAction, MoveAction, SetModeAction, UseAbilityAction
from .ai import TacticalAI
from .catalog import load_catalog
from .model import BattleState, Catalog, CommanderState, IMPASSABLE_TERRAIN, Mode, Side, UnitDefinition, UnitState
from .resolver import ActionResolver, InvalidAction


ROOT = Path(__file__).resolve().parents[1]
HOST = "127.0.0.1"
PORT = 8765


class GameSession:
    def __init__(self):
        self.base_catalog = load_catalog(ROOT / "data" / "vertical_slice_v_3.json")
        self.catalog = self.base_catalog
        self.classes = {item["id"]:item for item in json.loads((ROOT / "data" / "classes_personagens_v_1.json").read_text(encoding="utf-8"))["classes"]}
        self.full_troops = {item["id"]:item for item in json.loads((ROOT / "data" / "classes_tropas_v_1.json").read_text(encoding="utf-8"))["troops"]}
        self.scenarios = json.loads((ROOT / "data" / "cenarios_v_3.json").read_text(encoding="utf-8"))["scenarios"]
        self.maps = {item["id"]: item for item in json.loads((ROOT / "data" / "mapas_v_3.json").read_text(encoding="utf-8"))["maps"]}
        self.resolver = ActionResolver(self.catalog, seed=42)
        self.ai = TacticalAI(self.resolver)
        self.state: BattleState | None = None
        self.scenario = None
        self.map = None
        self.player_class_id = next(iter(self.classes))
        self.player_troop_ids = list(self.full_troops)[:2]
        self.lock = threading.Lock()

    def new(self, scenario_id: str, class_id: str | None = None, troop_ids: list[str] | None = None):
        self.scenario = next((item for item in self.scenarios if item["id"] == scenario_id), self.scenarios[0])
        self.map = self.maps[self.scenario["map_id"]]
        self.player_class_id = class_id if class_id in self.classes else self.player_class_id
        requested_troops = [item for item in (troop_ids or self.player_troop_ids) if item in self.full_troops]
        requested_troops.extend(item for item in self.full_troops if item not in requested_troops)
        self.player_troop_ids = requested_troops[:2]
        dynamic_commander = self._playable_commander(self.classes[self.player_class_id])
        dynamic_troops = [self._playable_troop(self.full_troops[item]) for item in self.player_troop_ids]
        formation_cap = sum(item.cap_cost for item in dynamic_troops)
        if formation_cap > dynamic_commander.cap_limit:
            raise InvalidAction(f"Formação custa {formation_cap} CAP, mas o comandante permite {dynamic_commander.cap_limit}")
        enemy_commander = self._playable_commander(self.classes[self.scenario["enemy_class_id"]])
        enemy_troops = [self._playable_troop(self.full_troops[item]) for item in self.scenario["enemy_troop_ids"]]
        commanders = dict(self.base_catalog.commanders)
        commanders[dynamic_commander.id] = dynamic_commander
        commanders[enemy_commander.id] = enemy_commander
        troops = dict(self.base_catalog.units)
        troops.update({item.id:item for item in dynamic_troops})
        troops.update({item.id:item for item in enemy_troops})
        self.catalog = Catalog.frozen(troops, commanders, dict(self.base_catalog.abilities), self.base_catalog.schema_version, dict(self.base_catalog.scope))
        self.resolver = ActionResolver(self.catalog, seed=42 + self.scenario["order"])
        self.ai = TacticalAI(self.resolver)
        blue_spawns = [tuple(item) for item in self.map["blue_spawns"]]
        red_spawns = [tuple(item) for item in self.map["red_spawns"]]
        blue_def = dynamic_commander
        red_def = enemy_commander
        units = {
            "azul-cmd": CommanderState("azul-cmd", blue_def.id, Side.BLUE, blue_def.hp, blue_spawns[0], cmd=blue_def.cmd_max),
            "azul-t1": UnitState("azul-t1", dynamic_troops[0].id, Side.BLUE, dynamic_troops[0].hp, blue_spawns[1], "azul-cmd", mode=Mode(self.full_troops[self.player_troop_ids[0]]["preferred_mode"])),
            "azul-t2": UnitState("azul-t2", dynamic_troops[1].id, Side.BLUE, dynamic_troops[1].hp, blue_spawns[2], "azul-cmd", mode=Mode(self.full_troops[self.player_troop_ids[1]]["preferred_mode"])),
            "vermelho-cmd": CommanderState("vermelho-cmd", red_def.id, Side.RED, red_def.hp, red_spawns[0], cmd=red_def.cmd_max),
            "vermelho-t1": UnitState("vermelho-t1", enemy_troops[0].id, Side.RED, enemy_troops[0].hp, red_spawns[1], "vermelho-cmd", mode=Mode(self.full_troops[self.scenario["enemy_troop_ids"][0]]["preferred_mode"])),
            "vermelho-t2": UnitState("vermelho-t2", enemy_troops[1].id, Side.RED, enemy_troops[1].hp, red_spawns[2], "vermelho-cmd", mode=Mode(self.full_troops[self.scenario["enemy_troop_ids"][1]]["preferred_mode"])),
        }
        blocked = {
            (x, y)
            for y, row in enumerate(self.map["grid"])
            for x, tile in enumerate(row)
            if tile in IMPASSABLE_TERRAIN
        }
        terrain = {(x, y): tile for y, row in enumerate(self.map["grid"]) for x, tile in enumerate(row)}
        condition = self.scenario["victory_condition"]
        self.state = BattleState(
            units, Side.BLUE, board_width=self.map["width"], board_height=self.map["height"], blocked=blocked, terrain=terrain,
            victory_condition=condition, round_limit=self.scenario.get("round_limit"),
            objective_tiles={tuple(item) for item in self.scenario.get("objective_tiles", [])},
            control_required=self.scenario.get("control_required", 0),
            escort_unit_id="azul-t2" if condition == "escort" else None,
            escort_exit=tuple(self.scenario["escort_exit"]) if self.scenario.get("escort_exit") else None,
            intercept_unit_id="vermelho-t2" if condition == "intercept" else None,
            intercept_exit=tuple(self.scenario["intercept_exit"]) if self.scenario.get("intercept_exit") else None,
        )
        self.state.events.append(f"Cenário iniciado: {self.scenario['name']}")
        self.state.events.append(f"Objetivo: {self.scenario['objective']}")
        return self.snapshot()

    def _playable_commander(self, item):
        role_base = {"defesa":"cmd_bastiao","controle":"cmd_estrategista","mistico":"cmd_estrategista","lideranca":"cmd_hibrido","assalto":"cmd_vanguarda","marcial":"cmd_vanguarda"}.get(item["role"],"cmd_hibrido")
        base = self.base_catalog.commanders[role_base]
        growth = item["growth"]
        tier = item["tier"]
        affinity = {"elfo":"forestwise","anao":"mountainwise","mares":"amphibious","avariano":"flying","deserto":"desertwise"}.get(item["family_id"])
        return replace(
            base, id=f"jogavel_{item['id']}", name=item["name"], role=item["role"],
            hp=base.hp + growth["vigor"] + tier * 2,
            attack=base.attack + growth["forca"] + (tier - 1),
            defense=base.defense + growth["vigor"] // 2 + (tier - 1),
            accuracy=min(95, base.accuracy + growth["destreza"] * 2),
            cap_limit=min(12, base.cap_limit + tier // 2), cmd_max=base.cmd_max + growth["presenca"] // 2,
            tags=base.tags + tuple(tag for tag in (item["family_id"], affinity) if tag),
        )

    def _playable_troop(self, item):
        stats = item["stats"]
        role = item["role"]
        abilities = ()
        affinity = {"elfo":"forestwise","anao":"mountainwise","mares":"amphibious","avariano":"flying","deserto":"desertwise"}.get(item["family_id"])
        tags = (role, item["family_id"]) + ((affinity,) if affinity else ())
        if "Lance" in item["name"]:
            abilities = ("preparar_lanca",)
            tags += ("lancer",)
        elif role == "mobilidade":
            abilities = ("investida",)
            tags += ("cavalry",)
        elif role in {"distancia","especialista"}:
            abilities = ("escarmuca",)
            tags += ("skirmisher",)
        return UnitDefinition(
            id=f"jogavel_{item['id']}", name=item["name"], role=role, hp=stats["hp"],
            attack=stats["attack"], defense=stats["defense"], movement=stats["movement"],
            attack_range=stats["range"], cap_cost=item["cap_cost"],
            accuracy=84 if role == "distancia" else 80, evasion=16 if role == "mobilidade" else 10,
            armor_piercing=2 if role in {"ruptura","especialista"} else 0, tags=tags, abilities=abilities,
        )

    def act(self, payload):
        if self.state is None:
            return self.new("cenario_humano_01")
        action = self._parse_action(payload)
        result = self.resolver.apply(self.state, action)
        self.state = result.state
        safety = len(self.state.units) * 2
        while self.state.winner is None and self.state.active_side == Side.RED and safety > 0:
            self._run_ai_activation()
            safety -= 1
        if safety == 0 and self.state.winner is None and self.state.active_side == Side.RED:
            raise InvalidAction("A IA não conseguiu devolver a iniciativa")
        return self.snapshot()

    def _parse_action(self, payload):
        kind = payload.get("type")
        actor_id = payload.get("actor_id", "")
        if kind == "move":
            return MoveAction(actor_id, (int(payload["x"]), int(payload["y"])))
        if kind == "end":
            return EndActivationAction(actor_id)
        if kind == "attack":
            return AttackAction(actor_id, payload["target_id"])
        if kind == "mode":
            return SetModeAction(actor_id, Mode(payload["mode"]))
        if kind == "command":
            return CommandAction(actor_id, payload["ability_id"], tuple(payload["target_ids"]))
        if kind == "ability":
            destination = payload.get("destination")
            if destination is None and payload.get("target_id"):
                return self._assisted_ability(actor_id, payload["ability_id"], payload["target_id"])
            return UseAbilityAction(actor_id, payload["ability_id"], payload.get("target_id"), tuple(destination) if destination else None)
        raise InvalidAction("Ação da interface desconhecida")

    def _assisted_ability(self, actor_id, ability_id, target_id):
        actor = self.state.units.get(actor_id)
        target = self.state.units.get(target_id)
        if actor is None or target is None:
            raise InvalidAction("Ator ou alvo inválido")
        ability = self.catalog.abilities.get(ability_id)
        candidates = []
        if ability and ability.mechanic == "charge":
            tx, ty = target.position
            destinations = ((tx+1,ty),(tx-1,ty),(tx,ty+1),(tx,ty-1))
        elif ability and ability.mechanic == "skirmish":
            destinations = (
                (x,y)
                for y in range(max(0,actor.position[1]-ability.max_reposition),min(self.state.board_height,actor.position[1]+ability.max_reposition+1))
                for x in range(max(0,actor.position[0]-ability.max_reposition),min(self.state.board_width,actor.position[0]+ability.max_reposition+1))
            )
        else:
            raise InvalidAction("Habilidade não aceita assistência de destino")
        for destination in destinations:
            action = UseAbilityAction(actor_id, ability_id, target_id, destination)
            try:
                result = self.resolver.preview(self.state, action)
            except InvalidAction:
                continue
            score = self.ai._score(self.state, result.state, actor, action)
            candidates.append((score, repr(action), action))
        if not candidates:
            raise InvalidAction("Nenhum destino legal para a habilidade")
        return max(candidates, key=lambda item:(item[0],item[1]))[2]

    def _run_ai_activation(self):
        action = self.ai.choose_action(self.state, Side.RED)
        self.state = self.resolver.apply(self.state, action).state

    def snapshot(self):
        state = self.state
        units = []
        for unit in state.units.values():
            definition = self.resolver._definition(unit)
            units.append({
                "id":unit.instance_id,"definition_id":unit.definition_id,"name":definition.name,
                "side":unit.side.value,"hp":unit.hp,"max_hp":definition.hp,"position":list(unit.position),
                "mode":unit.mode.value,"activated":unit.activated,"reaction":unit.reaction_available,
                "movement_spent":unit.movement_spent,"action_spent":unit.action_spent,
                "alive":unit.alive,"attack":definition.attack,"defense":definition.defense,
                "movement":definition.movement,"range":definition.attack_range,"abilities":list(definition.abilities),
                "cmd":unit.cmd if isinstance(unit, CommanderState) else None,
                "commander_id":unit.commander_id,
            })
        legal_moves = {}
        if state.winner is None and state.active_side == Side.BLUE:
            for unit in state.units.values():
                if unit.side != Side.BLUE or not unit.alive or unit.activated or unit.movement_spent:
                    continue
                if state.current_actor_id not in (None, unit.instance_id):
                    continue
                destinations = self.resolver.reachable_positions(state, unit.instance_id)
                legal_moves[unit.instance_id] = [
                    [x, y, cost]
                    for (x, y), cost in sorted(destinations.items(), key=lambda item: (item[0][1], item[0][0]))
                ]
        return {
            "scenario":self.scenario,"map":self.map,"round":state.round_number,
            "active_side":state.active_side.value,"winner":state.winner.value if state.winner else None,
            "current_actor_id":state.current_actor_id,"victory_condition":state.victory_condition,
            "round_limit":state.round_limit,"control_progress":state.control_progress,"control_required":state.control_required,
            "formation_cap":sum(self.catalog.units[self.state.units[item].definition_id].cap_cost for item in ("azul-t1","azul-t2")),
            "formation_cap_limit":self.catalog.commanders[self.state.units["azul-cmd"].definition_id].cap_limit,
            "units":units,"events":state.events[-12:],"legal_moves":legal_moves,
            "player_class_id":self.player_class_id,"player_troop_ids":self.player_troop_ids
        }


SESSION = GameSession()


class LocalGameServer(ThreadingHTTPServer):
    # No Windows, allow_reuse_address=True pode deixar várias cópias do jogo
    # responderem na mesma porta. Isso fazia o navegador receber assets antigos.
    allow_reuse_address = False


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):
        if self.path == "/":
            self.path = "/web/index.html"
        if self.path == "/api/state":
            with SESSION.lock:
                payload = SESSION.snapshot() if SESSION.state else SESSION.new("cenario_humano_01")
            return self._json(200, payload)
        return super().do_GET()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        try:
            payload = json.loads(self.rfile.read(length) or b"{}")
            with SESSION.lock:
                result = SESSION.new(payload.get("scenario_id", "cenario_humano_01"), payload.get("class_id"), payload.get("troop_ids")) if self.path == "/api/new" else SESSION.act(payload)
            self._json(200, result)
        except (InvalidAction, ValueError, KeyError) as exc:
            self._json(400, {"error":str(exc)})

    def end_headers(self):
        # O servidor é local e os dados mudam durante o desenvolvimento. Desativar
        # cache evita que o navegador misture index/app/JSON de versões diferentes.
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def _json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        return


def main():
    url = f"http://{HOST}:{PORT}"
    try:
        server = LocalGameServer((HOST, PORT), Handler)
    except OSError as exc:
        if getattr(exc, "winerror", None) == 10048 or getattr(exc, "errno", None) in {48, 98}:
            try:
                with urllib.request.urlopen(f"{url}/api/state", timeout=1) as response:
                    running_game = json.load(response)
                if running_game.get("scenario") and running_game.get("player_class_id"):
                    print(f"Asterra já está em execução em {url}. Abrindo o jogo existente.")
                    webbrowser.open(url)
                    return
            except (OSError, ValueError, json.JSONDecodeError):
                pass
            print(f"A porta {PORT} está sendo usada por outro programa. Encerre-o ou reinicie o computador.")
            return
        raise
    print(f"Asterra disponível em {url} — Ctrl+C para encerrar")
    threading.Timer(0.4, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
