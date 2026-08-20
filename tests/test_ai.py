import unittest
from pathlib import Path

from tactical_rpg.actions import AttackAction, CommandAction, UseAbilityAction
from tactical_rpg.ai import TacticalAI
from tactical_rpg.catalog import load_catalog
from tactical_rpg.model import BattleState, CommanderState, Side, UnitState
from tactical_rpg.resolver import ActionResolver


ROOT = Path(__file__).resolve().parents[1]


class TacticalAITests(unittest.TestCase):
    def setUp(self):
        self.catalog = load_catalog(ROOT / "data" / "vertical_slice_v_3.json")
        self.resolver = ActionResolver(self.catalog, seed=3)
        self.ai = TacticalAI(self.resolver)

    def commander(self, instance, definition, side, position):
        item = self.catalog.commanders[definition]
        return CommanderState(instance, definition, side, item.hp, position, cmd=item.cmd_max)

    def troop(self, instance, definition, side, position, commander):
        item = self.catalog.units[definition]
        return UnitState(instance, definition, side, item.hp, position, commander)

    def test_ai_prioritizes_lethal_commander_attack(self):
        units = {
            "b-cmd":self.commander("b-cmd","cmd_vanguarda",Side.BLUE,(1,1)),
            "b-t":self.troop("b-t","tropa_espadas",Side.BLUE,(1,2),"b-cmd"),
            "r-cmd":self.commander("r-cmd","cmd_bastiao",Side.RED,(7,7)),
            "r-t":self.troop("r-t","tropa_espadas",Side.RED,(0,1),"r-cmd"),
        }
        units["b-cmd"].hp = 1
        units["b-t"].hp = 1
        action = self.ai.choose_action(BattleState(units,Side.RED,round_starter=Side.RED),Side.RED)
        self.assertIsInstance(action, AttackAction)
        self.assertEqual("b-cmd", action.target_id)

    def test_ai_uses_command_when_formation_is_out_of_contact(self):
        units = {
            "b-cmd":self.commander("b-cmd","cmd_vanguarda",Side.BLUE,(0,0)),
            "b-t":self.troop("b-t","tropa_espadas",Side.BLUE,(0,1),"b-cmd"),
            "r-cmd":self.commander("r-cmd","cmd_bastiao",Side.RED,(7,7)),
            "r-t":self.troop("r-t","tropa_lanceiros",Side.RED,(7,6),"r-cmd"),
        }
        action = self.ai.choose_action(BattleState(units,Side.RED,round_starter=Side.RED),Side.RED)
        self.assertIsInstance(action, CommandAction)
        self.assertEqual("manter_posicao", action.ability_id)

    def test_ai_prepares_lance_against_approaching_cavalry(self):
        units = {
            "b-cmd":self.commander("b-cmd","cmd_vanguarda",Side.BLUE,(0,0)),
            "b-cav":self.troop("b-cav","tropa_cavalaria_leve",Side.BLUE,(3,2),"b-cmd"),
            "r-cmd":self.commander("r-cmd","cmd_bastiao",Side.RED,(7,7)),
            "r-lance":self.troop("r-lance","tropa_lanceiros",Side.RED,(6,2),"r-cmd"),
        }
        units["r-cmd"].activated = True
        action = self.ai.choose_action(BattleState(units,Side.RED,round_starter=Side.RED),Side.RED)
        self.assertIsInstance(action, UseAbilityAction)
        self.assertEqual("preparar_lanca", action.ability_id)

    def test_ai_is_deterministic_and_returns_legal_action(self):
        units = {
            "b-cmd":self.commander("b-cmd","cmd_vanguarda",Side.BLUE,(0,0)),
            "b-t":self.troop("b-t","tropa_arqueiros",Side.BLUE,(0,2),"b-cmd"),
            "r-cmd":self.commander("r-cmd","cmd_hibrido",Side.RED,(7,7)),
            "r-t":self.troop("r-t","tropa_escaramucadores",Side.RED,(7,5),"r-cmd"),
        }
        state = BattleState(units,Side.RED,round_starter=Side.RED)
        first = self.ai.choose_action(state,Side.RED)
        second = self.ai.choose_action(state,Side.RED)
        self.assertEqual(first, second)
        self.resolver.preview(state, first)


if __name__ == "__main__":
    unittest.main()
