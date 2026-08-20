import unittest

from tactical_rpg.actions import MoveAction
from tactical_rpg.model import Mode, Side
from tactical_rpg.resolver import InvalidAction
from tactical_rpg.web import GameSession


class WebSessionTests(unittest.TestCase):
    def setUp(self):
        self.session = GameSession()

    def test_all_240_classes_convert_to_playable_commanders(self):
        definitions = [self.session._playable_commander(item) for item in self.session.classes.values()]
        self.assertEqual(240, len(definitions))
        self.assertEqual(240, len({item.id for item in definitions}))
        self.assertTrue(all(item.hp > 0 and item.cap_limit > 0 for item in definitions))

    def test_all_144_troops_convert_to_playable_units(self):
        definitions = [self.session._playable_troop(item) for item in self.session.full_troops.values()]
        self.assertEqual(144, len(definitions))
        self.assertEqual(144, len({item.id for item in definitions}))
        self.assertTrue(all(item.hp > 0 and item.cap_cost > 0 for item in definitions))

    def test_selected_catalog_entries_reach_battle(self):
        result = self.session.new(
            "cenario_geada_10",
            "classe_geada_coracao_do_inverno",
            ["tropa_geada_guardas_da_geada", "tropa_geada_cavaleiros_glaciais"],
        )
        blue_names = [item["name"] for item in result["units"] if item["side"] == "AZUL"]
        self.assertEqual(["Coração do Inverno", "Guardas da Geada", "Cavaleiros Glaciais"], blue_names)

    def test_interface_assists_charge_destination_without_bypassing_rules(self):
        self.session.new("cenario_humano_01", troop_ids=["tropa_humano_cavalaria_leve","tropa_humano_recrutas_da_coroa"])
        self.session.state.units["azul-t1"].position = (4,3)
        self.session.state.units["vermelho-t1"].position = (7,3)
        action = self.session._parse_action({"type":"ability","actor_id":"azul-t1","ability_id":"investida","target_id":"vermelho-t1"})
        result = self.session.resolver.preview(self.session.state, action)
        self.assertTrue(any("moveu" in event for event in result.events))

    def test_move_keeps_the_actor_and_main_action_triggers_ai(self):
        self.session.new("cenario_humano_01")
        moved = self.session.act({"type":"move","actor_id":"azul-t1","x":0,"y":6})
        self.assertEqual("AZUL", moved["active_side"])
        self.assertEqual("azul-t1", moved["current_actor_id"])
        result = self.session.act({"type":"mode","actor_id":"azul-t1","mode":"LIVRE"})
        red_activated = [item for item in result["units"] if item["side"] == "VERMELHO" and item["activated"]]
        self.assertEqual(1, len(red_activated))
        self.assertEqual("AZUL", result["active_side"])

    def test_snapshot_exposes_only_server_validated_legal_destinations(self):
        snapshot = self.session.new("cenario_anao_01")
        hard = {"#", "B", "^", "X"}
        self.assertIn("azul-t1", snapshot["legal_moves"])
        for x, y, cost in snapshot["legal_moves"]["azul-t1"]:
            self.assertNotIn(snapshot["map"]["grid"][y][x], hard)
            self.assertGreaterEqual(cost, 1)

    def test_all_loaded_maps_use_navigation_schema_v3(self):
        self.assertEqual(160, len(self.session.maps))
        for item in self.session.maps.values():
            self.assertEqual(3, item["navigation"]["version"])
            self.assertEqual(["#", "B", "^", "X"], item["navigation"]["impassable_symbols"])

    def test_every_scenario_reaches_a_terminal_state_without_softlock(self):
        for scenario in self.session.scenarios:
            with self.subTest(scenario=scenario["id"]):
                self.session.new(scenario["id"])
                for _ in range(90):
                    if self.session.state.winner is not None:
                        break
                    payload = self._player_action()
                    self.session.act(payload)
                self.assertIsNotNone(self.session.state.winner)

    def _player_action(self):
        state = self.session.state
        actors = [unit for unit in state.units.values() if unit.side == Side.BLUE and unit.alive and not unit.activated]
        if state.current_actor_id:
            actors = [state.units[state.current_actor_id]]
        enemies = [unit for unit in state.units.values() if unit.side == Side.RED and unit.alive]
        red_commander = next(unit for unit in enemies if unit.instance_id.endswith("cmd"))
        for actor in actors:
            definition = self.session.resolver._definition(actor)
            targets = sorted(enemies, key=lambda unit:(unit is not red_commander, unit.hp))
            for target in targets:
                if self.session.resolver._distance(actor.position,target.position) <= definition.attack_range:
                    return {"type":"attack","actor_id":actor.instance_id,"target_id":target.instance_id}
        if state.current_actor_id:
            actor = actors[0]
            mode = Mode.ATTACK if actor.mode != Mode.ATTACK else Mode.FREE
            return {"type":"mode","actor_id":actor.instance_id,"mode":mode.value}
        best = None
        for actor in actors:
            for y in range(state.board_height):
                for x in range(state.board_width):
                    action = MoveAction(actor.instance_id,(x,y))
                    try:
                        self.session.resolver.preview(state,action)
                    except InvalidAction:
                        continue
                    score = self.session.resolver._distance((x,y),red_commander.position)
                    candidate = (score,actor.instance_id,y,x)
                    if best is None or candidate < best[0]:
                        best = (candidate,{"type":"move","actor_id":actor.instance_id,"x":x,"y":y})
        if best:
            return best[1]
        actor = actors[0]
        mode = Mode.ATTACK if actor.mode != Mode.ATTACK else Mode.FREE
        return {"type":"mode","actor_id":actor.instance_id,"mode":mode.value}


if __name__ == "__main__":
    unittest.main()
