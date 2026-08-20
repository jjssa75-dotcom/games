import json
import tempfile
import unittest
from pathlib import Path

from tactical_rpg.actions import AttackAction, CommandAction, EndActivationAction, MoveAction, SetModeAction
from tactical_rpg.army import build_detachment
from tactical_rpg.catalog import load_catalog
from tactical_rpg.model import BattleState, Mode, Side
from tactical_rpg.resolver import ActionResolver, InvalidAction


ROOT = Path(__file__).resolve().parents[1]


class CoreInvariants(unittest.TestCase):
    def setUp(self):
        self.catalog = load_catalog(ROOT / "data" / "vertical_slice_v_3.json")
        units = build_detachment(self.catalog, "cmd_vanguarda", ["tropa_espadas"], Side.BLUE, "b", (0, 0))
        units.update(build_detachment(self.catalog, "cmd_bastiao", ["tropa_lanceiros"], Side.RED, "r", (1, 0)))
        self.state = BattleState(units, Side.BLUE)
        self.resolver = ActionResolver(self.catalog, 7)

    def test_catalog_scope_is_exact(self):
        self.assertEqual(6, len(self.catalog.commanders))
        self.assertEqual(8, len(self.catalog.units))

    def test_cap_is_not_cmd(self):
        commander = self.catalog.commanders["cmd_vanguarda"]
        self.assertNotEqual(commander.cap_limit, commander.cmd_max)
        with self.assertRaises(ValueError):
            build_detachment(self.catalog, "cmd_vanguarda", ["tropa_guarda"] * 3, Side.BLUE, "x")

    def test_no_double_activation(self):
        first = self.resolver.apply(self.state, SetModeAction("b-t1", Mode.ATTACK)).state
        first.active_side = Side.BLUE
        with self.assertRaises(InvalidAction):
            self.resolver.apply(first, MoveAction("b-t1", (1, 1)))

    def test_move_then_decide_is_one_locked_activation(self):
        moved = self.resolver.apply(self.state, MoveAction("b-t1", (1, 2))).state
        self.assertEqual(Side.BLUE, moved.active_side)
        self.assertEqual("b-t1", moved.current_actor_id)
        self.assertTrue(moved.units["b-t1"].movement_spent)
        self.assertFalse(moved.units["b-t1"].activated)
        with self.assertRaises(InvalidAction):
            self.resolver.apply(moved, MoveAction("b-t1", (0, 2)))
        with self.assertRaises(InvalidAction):
            self.resolver.apply(moved, SetModeAction("b-cmd", Mode.ATTACK))
        acted = self.resolver.apply(moved, AttackAction("b-t1", "r-t1")).state
        self.assertTrue(acted.units["b-t1"].activated)
        self.assertEqual(Side.RED, acted.active_side)
        self.assertIsNone(acted.current_actor_id)

    def test_move_only_can_be_ended_without_free_second_action(self):
        moved = self.resolver.apply(self.state, MoveAction("b-t1", (0, 2))).state
        ended = self.resolver.apply(moved, EndActivationAction("b-t1")).state
        self.assertTrue(ended.units["b-t1"].activated)
        self.assertEqual(Side.RED, ended.active_side)
        ended.active_side = Side.BLUE
        with self.assertRaises(InvalidAction):
            self.resolver.apply(ended, SetModeAction("b-t1", Mode.ATTACK))

    def test_end_activation_requires_a_prior_move(self):
        with self.assertRaises(InvalidAction):
            self.resolver.apply(self.state, EndActivationAction("b-t1"))

    def test_enemy_cannot_act_out_of_turn(self):
        with self.assertRaises(InvalidAction):
            self.resolver.apply(self.state, MoveAction("r-t1", (1, 1)))

    def test_invalid_action_is_atomic(self):
        before = self.state.units["b-t1"].position
        with self.assertRaises(InvalidAction):
            self.resolver.apply(self.state, MoveAction("b-t1", (99, 99)))
        self.assertEqual(before, self.state.units["b-t1"].position)
        self.assertFalse(self.state.units["b-t1"].activated)

    def test_preview_does_not_mutate(self):
        preview = self.resolver.preview(self.state, SetModeAction("b-t1", Mode.ATTACK))
        self.assertEqual(Mode.ATTACK, preview.state.units["b-t1"].mode)
        self.assertEqual(Mode.FREE, self.state.units["b-t1"].mode)

    def test_friendly_fire_rejected(self):
        with self.assertRaises(InvalidAction):
            self.resolver.apply(self.state, AttackAction("b-cmd", "b-t1"))

    def test_reaction_occurs_at_most_once(self):
        result = self.resolver.apply(self.state, AttackAction("b-t1", "r-t1"))
        self.assertFalse(result.state.units["r-t1"].reaction_available)
        self.assertEqual(1, sum("reagiu" in x for x in result.events))

    def test_cmd_cannot_go_negative(self):
        self.state.units["b-cmd"].cmd = 1
        with self.assertRaises(InvalidAction):
            self.resolver.apply(self.state, CommandAction("b-cmd", "avancar", ("b-t1",)))
        self.assertEqual(1, self.state.units["b-cmd"].cmd)

    def test_commander_cannot_command_enemy_or_unbound_unit(self):
        with self.assertRaises(InvalidAction):
            self.resolver.apply(self.state, CommandAction("b-cmd", "avancar", ("r-t1",)))

    def test_occupied_tile_rejected(self):
        with self.assertRaises(InvalidAction):
            self.resolver.apply(self.state, MoveAction("b-t1", (0, 0)))

    def test_command_spends_cmd_and_applies_data_modifier(self):
        self.state.units["b-t1"].morale = 90
        result = self.resolver.apply(
            self.state, CommandAction("b-cmd", "avancar", ("b-t1",))
        )
        self.assertEqual(3, result.state.units["b-cmd"].cmd)
        self.assertEqual(95, result.state.units["b-t1"].morale)
        self.assertEqual(1, result.state.units["b-t1"].status["avancar"])
        result.state.active_side = Side.BLUE
        moved = self.resolver.apply(result.state, MoveAction("b-t1", (0, 6)))
        self.assertEqual((0, 6), moved.state.units["b-t1"].position)

    def test_round_starter_alternates(self):
        state = self.resolver.apply(self.state, SetModeAction("b-cmd", Mode.ATTACK)).state
        state = self.resolver.apply(state, SetModeAction("r-cmd", Mode.DEFENSE)).state
        state = self.resolver.apply(state, SetModeAction("b-t1", Mode.ATTACK)).state
        state = self.resolver.apply(state, SetModeAction("r-t1", Mode.DEFENSE)).state
        self.assertEqual(2, state.round_number)
        self.assertEqual(Side.RED, state.round_starter)
        self.assertEqual(Side.RED, state.active_side)

    def test_survival_and_control_objectives_are_deterministic(self):
        survive = BattleState(self.state.units, Side.BLUE, victory_condition="survive", round_limit=1)
        self.resolver._new_round(survive)
        self.assertEqual(Side.BLUE, survive.winner)

        units = self.state.units
        units["b-t1"].position = (2, 2)
        control = BattleState(
            units, Side.BLUE, victory_condition="control_area", round_limit=4,
            objective_tiles={(2, 2)}, control_required=2,
        )
        self.resolver._new_round(control)
        self.assertEqual(1, control.control_progress)
        self.resolver._new_round(control)
        self.assertEqual(Side.BLUE, control.winner)

    def test_escort_and_intercept_objectives_have_no_ambiguous_terminal(self):
        escort = BattleState(
            self.state.units, Side.BLUE, victory_condition="escort",
            escort_unit_id="b-t1", escort_exit=(0, 2),
        )
        result = self.resolver.apply(escort, MoveAction("b-t1", (0, 2))).state
        self.assertEqual(Side.BLUE, result.winner)

        intercept = BattleState(
            self.state.units, Side.BLUE, victory_condition="intercept",
            intercept_unit_id="r-t1", intercept_exit=(7, 7),
        )
        intercept.units["r-t1"].hp = 1
        result = self.resolver.apply(intercept, AttackAction("b-t1", "r-t1")).state
        self.assertEqual(Side.BLUE, result.winner)


if __name__ == "__main__":
    unittest.main()
