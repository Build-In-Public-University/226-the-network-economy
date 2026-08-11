import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from capitalism_analysis.analyze import argument_edges, parse_sections, seed_claims


class AnalysisTests(unittest.TestCase):
    def test_source_has_sections(self):
        sections = parse_sections(ROOT / "source/sep-capitalism.md")
        self.assertGreater(len(sections), 20)
        self.assertEqual(sections[0].heading, "Capitalism")

    def test_claim_ids_and_edges_are_consistent(self):
        claims = seed_claims()
        ids = {c.id for c in claims}
        self.assertEqual(len(ids), len(claims))
        for edge in argument_edges(claims):
            self.assertIn(edge["source"], ids)
            self.assertIn(edge["target"], ids)

    def test_claims_have_falsifiers(self):
        self.assertTrue(all(c.falsifier.strip() for c in seed_claims()))

    def test_alignment_ledger_is_structured_and_falsifiable(self):
        rows = json.loads((ROOT / "data/time-violence-alignment.json").read_text())
        self.assertEqual(len(rows), 10)
        self.assertTrue(all(row["sep_claims"] for row in rows))
        self.assertTrue(all(row["falsifier"].strip() for row in rows))
        self.assertIn("open_hypothesis", {row["alignment"] for row in rows})

    def test_review_artifacts_exist_and_human_judge_is_unfilled(self):
        pro = (ROOT / "reviews/pro-review.md").read_text()
        con = (ROOT / "reviews/con-review.md").read_text()
        judge = (ROOT / "reviews/HUMAN-JUDGE.md").read_text()
        self.assertIn("## Executive case", pro)
        self.assertIn("## Executive case", con)
        self.assertIn("Human verdict", judge)
        self.assertIn("Status: pending human adjudication", judge)

    def test_multi_resource_model_has_three_distinct_baselines(self):
        model = json.loads((ROOT / "data/multi-resource-model.json").read_text())
        self.assertEqual({s["id"] for s in model["systems"]}, {
            "communism_idealized", "capitalism_idealized", "network_economy_proposed"
        })
        self.assertGreaterEqual(len(model["falsifiers"]), 4)
        self.assertIn("future weight ≥ past weight", (ROOT / "multi-resource-model.md").read_text())


if __name__ == "__main__":
    unittest.main()
