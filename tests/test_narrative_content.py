import json
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((ROOT / "data" / name).read_text(encoding="utf-8"))


class NarrativeContentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.regions = load("regioes_v_2.json")["regions"]
        cls.characters = load("personagens_v_2.json")["characters"]
        cls.campaign = load("campanha_v_3.json")
        cls.scenarios = load("cenarios_v_3.json")["scenarios"]
        cls.previous_scenarios = load("cenarios_v_2.json")["scenarios"]
        cls.classes = load("classes_personagens_v_1.json")["classes"]
        cls.troops = load("classes_tropas_v_1.json")["troops"]

    def test_campaign_scope_and_catalog_scope_are_preserved(self):
        self.assertEqual(16, len(self.regions))
        self.assertEqual(32, len(self.characters))
        self.assertEqual(160, len(self.scenarios))
        self.assertEqual({10}, set(Counter(item["region_id"] for item in self.scenarios).values()))
        self.assertEqual(240, len(self.classes))
        self.assertEqual(144, len(self.troops))
        self.assertEqual(240, self.campaign["catalog_scope"]["character_classes"])
        self.assertEqual(144, self.campaign["catalog_scope"]["troop_classes"])

    def test_regions_have_political_economic_and_territorial_logic(self):
        required = {
            "polity",
            "governance",
            "political_economy",
            "strategic_resources",
            "territorial_role",
            "historical_grievance",
            "fracture_stake",
            "coalition_demand",
            "convergence_offer",
            "internal_blocs",
            "credible_betrayal",
            "regional_resolution",
        }
        for region in self.regions:
            self.assertTrue(required.issubset(region), region["id"])
            self.assertGreaterEqual(len(region["internal_blocs"]), 2, region["id"])
            self.assertTrue(all(region[key] for key in required), region["id"])
        self.assertEqual(16, len({item["historical_grievance"] for item in self.regions}))
        self.assertEqual(16, len({item["credible_betrayal"] for item in self.regions}))

    def test_every_region_has_a_hero_and_rival_with_distinct_motives(self):
        for region in self.regions:
            cast = [item for item in self.characters if item["family_id"] == region["family_id"]]
            self.assertEqual(2, len(cast), region["id"])
            self.assertEqual(2, len({item["alignment"] for item in cast}))
            self.assertEqual(2, len({item["goal"] for item in cast}))
            for character in cast:
                for key in (
                    "goal",
                    "internal_conflict",
                    "political_position",
                    "creed",
                    "moral_gray_function",
                    "regional_betrayal_or_reversal",
                ):
                    self.assertTrue(character[key], character["id"])

    def test_political_marks_and_endings_are_coherent(self):
        mark_ids = {item["id"] for item in self.campaign["political_marks"]}
        self.assertEqual(6, len(mark_ids))
        self.assertEqual(mark_ids, set(self.campaign["initial_marks"]))
        endings = self.campaign["ending_routes"]
        self.assertEqual(3, len(endings))
        self.assertEqual(1, sum(bool(item["canonical"]) for item in endings))
        for ending in endings:
            self.assertTrue(ending["requirements"])
            self.assertTrue(ending["outcome"])

    def test_all_160_stages_have_complete_unique_narrative(self):
        mark_ids = {item["id"] for item in self.campaign["political_marks"]}
        contexts, dilemmas, revelations = set(), set(), set()
        for scenario in self.scenarios:
            narrative = scenario["narrative"]
            for key in (
                "regional_phase",
                "historical_context",
                "continuity",
                "pre_battle_dialogue",
                "post_battle_dialogue",
                "moral_dilemma",
                "revelation",
                "political_marks",
                "enemy_justification",
                "level_design_justification",
                "soft_counter_narrative",
            ):
                self.assertTrue(narrative[key], scenario["id"])
            self.assertEqual(2, len(narrative["pre_battle_dialogue"]), scenario["id"])
            self.assertEqual(2, len(narrative["post_battle_dialogue"]), scenario["id"])
            for dialogue in narrative["pre_battle_dialogue"] + narrative["post_battle_dialogue"]:
                self.assertTrue(dialogue["speaker"] and dialogue["line"], scenario["id"])
            choice = narrative["political_marks"]["choice"]
            self.assertEqual(2, len(choice["options"]), scenario["id"])
            self.assertIn(choice["canonical_option_id"], {item["id"] for item in choice["options"]})
            for option in choice["options"]:
                self.assertTrue(set(option["effects"]).issubset(mark_ids), scenario["id"])
                self.assertTrue(all(-3 <= value <= 3 for value in option["effects"].values()))
            self.assertTrue(set(narrative["political_marks"]["canonical_route"]).issubset(mark_ids))
            contexts.add(narrative["historical_context"])
            dilemmas.add(narrative["moral_dilemma"])
            revelations.add(narrative["revelation"])
        self.assertEqual(160, len(contexts))
        self.assertEqual(160, len(dilemmas))
        self.assertEqual(160, len(revelations))

    def test_web_campaign_renderer_uses_the_published_narrative_schema(self):
        app = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
        index = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
        server = (ROOT / "tactical_rpg" / "web.py").read_text(encoding="utf-8")
        self.assertIn("narrative.pre_battle_dialogue", app)
        self.assertIn("narrative.post_battle_dialogue", app)
        self.assertIn("narrative.moral_dilemma", app)
        self.assertNotIn("narrative.dialogue.pre_battle", app)
        self.assertNotIn("narrative.dialogue.post_battle", app)
        self.assertIn("/web/app.js?v=2.2.1", index)
        self.assertIn('Cache-Control", "no-store', server)
        self.assertIn('PORT = 8765', server)
        self.assertIn('allow_reuse_address = False', server)

    def test_continuity_links_the_entire_campaign_without_gaps(self):
        for index, scenario in enumerate(self.scenarios):
            continuity = scenario["narrative"]["continuity"]
            expected_previous = self.scenarios[index - 1]["id"] if index else None
            expected_next = self.scenarios[index + 1]["id"] if index + 1 < len(self.scenarios) else None
            self.assertEqual(expected_previous, continuity["from_scenario_id"], scenario["id"])
            self.assertEqual(expected_next, continuity["to_scenario_id"], scenario["id"])
            if scenario["stage_in_region"] == 10:
                self.assertTrue(continuity["regional_payoff"], scenario["id"])

    def test_level_design_and_enemy_families_are_justified(self):
        family_ids = {item["family_id"] for item in self.regions}
        for scenario in self.scenarios:
            narrative = scenario["narrative"]
            self.assertTrue(set(scenario["enemy_family_ids"]).issubset(family_ids))
            self.assertIn(scenario["objective"], narrative["level_design_justification"])
            self.assertIn(scenario["formation_twist"].lower(), narrative["level_design_justification"].lower())
            self.assertIn(scenario["soft_counter"]["punishes"], narrative["soft_counter_narrative"])

    def test_narrative_revision_does_not_change_tactical_contracts(self):
        tactical_keys = (
            "id",
            "order",
            "region_id",
            "map_id",
            "objective",
            "victory_condition",
            "round_limit",
            "control_required",
            "objective_tiles",
            "escort_exit",
            "intercept_exit",
            "enemy_family_ids",
            "enemy_class_id",
            "enemy_troop_ids",
            "soft_counter",
            "formation_twist",
            "difficulty",
            "boss",
        )
        self.assertEqual(len(self.previous_scenarios), len(self.scenarios))
        for previous, current in zip(self.previous_scenarios, self.scenarios):
            for key in tactical_keys:
                self.assertEqual(previous[key], current[key], f"{current['id']}:{key}")


if __name__ == "__main__":
    unittest.main()
