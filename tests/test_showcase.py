"""Check the published calculations and update schedule independently of APIs."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.summarize_results import CONDITIONS, load_table, relative_gap
from examples.mrp_schedule import stages_for_round


class ShowcaseTests(unittest.TestCase):
    def test_gap_is_absolute_on_either_side_of_benchmark(self):
        self.assertEqual(relative_gap(40, 50, 100), 0.2)
        self.assertEqual(relative_gap(60, 50, 100), 0.2)
        self.assertEqual(relative_gap(110, 50, 100), 1.2)

    def test_exact_matches_and_undefined_baseline(self):
        self.assertEqual(relative_gap(50, 50, 100), 0)
        self.assertIsNone(relative_gap(60, 50, 50))

    def test_complete_conditions_and_network_identity(self):
        data = load_table()
        self.assertEqual(set(data), set(CONDITIONS) | {'human_control'})
        for row in data.values():
            self.assertAlmostEqual(row['density'], row['recipients'] / 5)

    def test_claims_match_archived_means(self):
        data = load_table()
        self.assertAlmostEqual(data['human_control']['total_sent'], 43.394675925925924)
        self.assertAlmostEqual(data['reasoning_high']['total_sent'], 41.5162037037037)
        self.assertAlmostEqual(data['mrp']['total_sent'], 63.04398148148148)

    def test_plan_and_reflection_rounds(self):
        schedule = {r: stages_for_round(r) for r in range(1, 16)}
        self.assertEqual([r for r, stages in schedule.items() if 'plan' in stages], [1, 4, 7, 10, 13])
        self.assertEqual([r for r, stages in schedule.items() if 'reflect' in stages], [4, 7, 10, 13])
        self.assertTrue(all(stages[-1] == 'act' for stages in schedule.values()))

    def test_invalid_schedule_parameters(self):
        with self.assertRaises(ValueError):
            stages_for_round(0)
        with self.assertRaises(ValueError):
            stages_for_round(1, 0)


if __name__ == '__main__':
    unittest.main()
