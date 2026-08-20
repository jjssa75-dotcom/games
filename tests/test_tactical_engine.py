import unittest
from pathlib import Path

from tactical_rpg.actions import AttackAction, CommandAction, MoveAction, UseAbilityAction
from tactical_rpg.catalog import load_catalog
from tactical_rpg.model import BattleState, CommanderState, Side, UnitState
from tactical_rpg.resolver import ActionResolver, InvalidAction


ROOT = Path(__file__).resolve().parents[1]


class TacticalEngineTests(unittest.TestCase):
    def setUp(self):
        self.catalog = load_catalog(ROOT / "data" / "vertical_slice_v_3.json")

    def unit(self, instance, definition, side, position, commander=None):
        item = self.catalog.units[definition]
        return UnitState(instance, definition, side, item.hp, position, commander)

    def commander(self, instance, definition, side, position):
        item = self.catalog.commanders[definition]
        return CommanderState(instance, definition, side, item.hp, position, cmd=item.cmd_max)

    def state(self):
        return BattleState({
            "b-cmd":self.commander("b-cmd","cmd_vanguarda",Side.BLUE,(0,0)),
            "b-t":self.unit("b-t","tropa_espadas",Side.BLUE,(0,1),"b-cmd"),
            "r-cmd":self.commander("r-cmd","cmd_bastiao",Side.RED,(7,0)),
            "r-t":self.unit("r-t","tropa_lanceiros",Side.RED,(7,1),"r-cmd"),
        }, Side.BLUE)

    def test_off_board_movement_is_rejected(self):
        with self.assertRaisesRegex(InvalidAction, "fora do tabuleiro"):
            ActionResolver(self.catalog).apply(self.state(), MoveAction("b-t", (-1, 1)))

    def test_blocked_cells_are_not_traversable(self):
        state = self.state()
        state.blocked = {(1,0),(1,1),(1,2)}
        with self.assertRaisesRegex(InvalidAction, "sem caminho"):
            ActionResolver(self.catalog).apply(state, MoveAction("b-t", (2,1)))

    def test_hard_terrain_is_rejected_even_if_loader_omits_blocked_set(self):
        for tile in ("#", "B", "^", "X"):
            with self.subTest(tile=tile):
                state = self.state()
                state.terrain[(1,1)] = tile
                with self.assertRaisesRegex(InvalidAction, "intransponível"):
                    ActionResolver(self.catalog).apply(state, MoveAction("b-t", (1,1)))

    def test_reachable_preview_never_includes_units_or_hard_terrain(self):
        state = self.state()
        state.terrain.update({(2,1):"^", (2,2):"X", (1,2):"B"})
        reachable = ActionResolver(self.catalog).reachable_positions(state, "b-t")
        self.assertTrue(reachable)
        self.assertNotIn((2,1), reachable)
        self.assertNotIn((2,2), reachable)
        self.assertNotIn((1,2), reachable)
        self.assertNotIn((0,0), reachable)
        self.assertTrue(all(abs(x) + abs(y - 1) <= self.catalog.units["tropa_espadas"].movement for x,y in reachable))

    def test_difficult_terrain_consumes_movement_budget(self):
        state = self.state()
        state.terrain = {(1,1):"F", (2,1):"F"}
        with self.assertRaisesRegex(InvalidAction, "sem caminho"):
            ActionResolver(self.catalog).apply(state, MoveAction("b-t", (3,1)))

    def test_forest_cover_reduces_ranged_damage(self):
        units = {
            "b-cmd":self.commander("b-cmd","cmd_vanguarda",Side.BLUE,(0,0)),
            "b-archer":self.unit("b-archer","tropa_besteiros",Side.BLUE,(0,2),"b-cmd"),
            "r-cmd":self.commander("r-cmd","cmd_bastiao",Side.RED,(3,2)),
        }
        clear = BattleState(units, Side.BLUE)
        covered = BattleState(units, Side.BLUE, terrain={(3,2):"F"})
        clear_result = ActionResolver(self.catalog,seed=1).apply(clear, AttackAction("b-archer","r-cmd")).state
        cover_result = ActionResolver(self.catalog,seed=1).apply(covered, AttackAction("b-archer","r-cmd")).state
        self.assertGreater(cover_result.units["r-cmd"].hp, clear_result.units["r-cmd"].hp)

    def test_command_range_and_duplicate_targets_are_enforced(self):
        state = self.state()
        state.units["b-t"].position = (7,7)
        resolver = ActionResolver(self.catalog)
        with self.assertRaisesRegex(InvalidAction, "alcance"):
            resolver.apply(state, CommandAction("b-cmd","avancar",("b-t",)))
        state.units["b-t"].position = (0,1)
        with self.assertRaisesRegex(InvalidAction, "duplicados"):
            resolver.apply(state, CommandAction("b-cmd","avancar",("b-t","b-t")))

    def test_prepared_lance_intercepts_cavalry_charge(self):
        units = {
            "b-cmd":self.commander("b-cmd","cmd_vanguarda",Side.BLUE,(0,0)),
            "b-cav":self.unit("b-cav","tropa_cavalaria_leve",Side.BLUE,(0,1),"b-cmd"),
            "r-cmd":self.commander("r-cmd","cmd_bastiao",Side.RED,(7,0)),
            "r-lance":self.unit("r-lance","tropa_lanceiros",Side.RED,(3,1),"r-cmd"),
        }
        resolver = ActionResolver(self.catalog, seed=1)
        state = BattleState(units, Side.RED, round_starter=Side.RED)
        state = resolver.apply(state, UseAbilityAction("r-lance","preparar_lanca")).state
        result = resolver.apply(state, UseAbilityAction("b-cav","investida","r-lance",(2,1)))
        self.assertTrue(any("interceptou" in event for event in result.events))
        self.assertFalse(result.state.units["r-lance"].reaction_available)
        self.assertNotIn("preparar_lanca", result.state.units["r-lance"].status)

    def test_charge_requires_distance(self):
        units = {
            "b-cmd":self.commander("b-cmd","cmd_vanguarda",Side.BLUE,(0,0)),
            "b-cav":self.unit("b-cav","tropa_cavalaria_leve",Side.BLUE,(1,1),"b-cmd"),
            "r-cmd":self.commander("r-cmd","cmd_bastiao",Side.RED,(3,1)),
        }
        with self.assertRaisesRegex(InvalidAction, "distância mínima"):
            ActionResolver(self.catalog).apply(BattleState(units,Side.BLUE),UseAbilityAction("b-cav","investida","r-cmd",(2,1)))

    def test_skirmish_attacks_then_repositions(self):
        units = {
            "b-cmd":self.commander("b-cmd","cmd_vanguarda",Side.BLUE,(0,0)),
            "b-skir":self.unit("b-skir","tropa_escaramucadores",Side.BLUE,(0,2),"b-cmd"),
            "r-cmd":self.commander("r-cmd","cmd_bastiao",Side.RED,(2,2)),
        }
        result = ActionResolver(self.catalog,seed=1).apply(BattleState(units,Side.BLUE),UseAbilityAction("b-skir","escarmuca","r-cmd",(0,4)))
        self.assertEqual((0,4), result.state.units["b-skir"].position)
        self.assertLess(result.state.units["r-cmd"].hp, self.catalog.commanders["cmd_bastiao"].hp)

    def test_defeating_commander_ends_battle(self):
        state = self.state()
        state.units["r-cmd"].position = (1,1)
        state.units["r-cmd"].hp = 1
        result = ActionResolver(self.catalog,seed=1).apply(state,AttackAction("b-t","r-cmd"))
        self.assertEqual(Side.BLUE, result.state.winner)
        with self.assertRaisesRegex(InvalidAction, "já terminou"):
            ActionResolver(self.catalog).apply(result.state,MoveAction("b-cmd",(1,0)))

    def test_failed_action_restores_rng(self):
        units = {
            "b-cmd":self.commander("b-cmd","cmd_vanguarda",Side.BLUE,(0,0)),
            "b-skir":self.unit("b-skir","tropa_escaramucadores",Side.BLUE,(0,2),"b-cmd"),
            "r-cmd":self.commander("r-cmd","cmd_bastiao",Side.RED,(2,2)),
        }
        state = BattleState(units,Side.BLUE)
        resolver = ActionResolver(self.catalog,seed=9)
        with self.assertRaises(InvalidAction):
            resolver.apply(state,UseAbilityAction("b-skir","escarmuca","r-cmd",(9,9)))
        after_failure = resolver.apply(state,AttackAction("b-skir","r-cmd"))
        fresh = ActionResolver(self.catalog,seed=9).apply(state,AttackAction("b-skir","r-cmd"))
        self.assertEqual(after_failure.events, fresh.events)


if __name__ == "__main__":
    unittest.main()
