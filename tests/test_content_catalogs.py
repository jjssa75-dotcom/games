import json
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((ROOT / "data" / name).read_text(encoding="utf-8"))


class ContentCatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.classes = load("classes_personagens_v_1.json")["classes"]
        cls.troops = load("classes_tropas_v_1.json")["troops"]
        cls.regions = load("regioes_v_1.json")["regions"]
        cls.characters = load("personagens_v_1.json")["characters"]
        cls.scenarios = load("cenarios_v_2.json")["scenarios"]
        cls.maps = load("mapas_v_3.json")["maps"]

    def test_exactly_240_character_classes(self):
        self.assertEqual(240, len(self.classes))
        self.assertEqual(240, len({item["id"] for item in self.classes}))
        self.assertEqual({15}, set(Counter(item["family_id"] for item in self.classes).values()))

    def test_class_trees_are_connected_and_tiered(self):
        by_id = {item["id"]:item for item in self.classes}
        for family in {item["family_id"] for item in self.classes}:
            tree = [item for item in self.classes if item["family_id"] == family]
            self.assertEqual([1,2,4,4,4], [sum(item["tier"] == tier for item in tree) for tier in range(1,6)])
            for item in tree:
                if item["tier"] == 1:
                    self.assertIsNone(item["parent_id"])
                else:
                    self.assertIn(item["parent_id"], by_id)
                    self.assertEqual(item["tier"] - 1, by_id[item["parent_id"]]["tier"])

    def test_approximately_140_troop_classes(self):
        self.assertEqual(144, len(self.troops))
        self.assertEqual(144, len({item["id"] for item in self.troops}))
        self.assertEqual({9}, set(Counter(item["family_id"] for item in self.troops).values()))
        self.assertEqual({1,2,3}, {item["tier"] for item in self.troops})

    def test_world_references_are_complete(self):
        family_ids = {item["family_id"] for item in self.regions}
        class_ids = {item["id"] for item in self.classes}
        self.assertEqual(16, len(self.regions))
        self.assertEqual(32, len(self.characters))
        self.assertEqual(family_ids, {item["family_id"] for item in self.classes})
        self.assertTrue(all(item["starting_class_id"] in class_ids for item in self.characters))

    def test_maps_are_rectangular_and_spawns_are_walkable(self):
        self.assertEqual(160, len(self.maps))
        for item in self.maps:
            self.assertEqual(item["height"], len(item["grid"]))
            self.assertTrue(all(len(row) == item["width"] for row in item["grid"]))
            for x,y in item["blue_spawns"] + item["red_spawns"]:
                self.assertNotIn(item["grid"][y][x], "#B^X")
            if item["exit"]:
                x, y = item["exit"]
                self.assertEqual("E", item["grid"][y][x])

    def test_every_map_has_connected_walkable_space_and_explicit_hard_barriers(self):
        hard = {"#", "B", "^", "X"}
        for item in self.maps:
            walkable = {
                (x, y)
                for y, row in enumerate(item["grid"])
                for x, tile in enumerate(row)
                if tile not in hard
            }
            visited, stack = set(), [min(walkable)]
            while stack:
                position = stack.pop()
                if position in visited:
                    continue
                visited.add(position)
                x, y = position
                stack.extend(
                    neighbor
                    for neighbor in ((x+1,y),(x-1,y),(x,y+1),(x,y-1))
                    if neighbor in walkable and neighbor not in visited
                )
            self.assertEqual(walkable, visited, item["id"])
            self.assertTrue(any(tile in hard for row in item["grid"] for tile in row), item["id"])
            self.assertEqual(["#", "B", "^", "X"], item["navigation"]["impassable_symbols"])
            self.assertFalse(item["navigation"]["flying_ignores_impassable"])

    def test_scenario_references_exist(self):
        map_ids = {item["id"] for item in self.maps}
        region_ids = {item["id"] for item in self.regions}
        self.assertEqual(list(range(1,161)), [item["order"] for item in self.scenarios])
        self.assertTrue(all(item["map_id"] in map_ids for item in self.scenarios))
        self.assertTrue(all(item["region_id"] in region_ids for item in self.scenarios))

    def test_campaign_has_ten_stages_per_region_and_all_enemy_families(self):
        by_region = Counter(item["region_id"] for item in self.scenarios)
        self.assertEqual({10}, set(by_region.values()))
        enemy_families = {family for item in self.scenarios for family in item["enemy_family_ids"]}
        self.assertEqual({item["family_id"] for item in self.regions}, enemy_families)
        self.assertEqual(
            {"defeat_commander","control_area","escort","survive","intercept"},
            {item["victory_condition"] for item in self.scenarios},
        )

    def test_every_stage_declares_a_soft_counter_without_hard_lock(self):
        for item in self.scenarios:
            counter = item["soft_counter"]
            self.assertTrue(counter["enemy_plan"] and counter["punishes"])
            self.assertGreaterEqual(len(counter["recommended_roles"]), 2)
            self.assertFalse(counter["hard_lock"])
            self.assertTrue(item["formation_twist"])


if __name__ == "__main__":
    unittest.main()
