import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SLIDES = ROOT / "slides" / "bayesian_poisson_worldcup.md"
NOTEBOOK = ROOT / "notebooks" / "bayesian_poisson_worldcup.ipynb"


class AssignmentArtifactTests(unittest.TestCase):
    def test_slide_markdown_has_core_story(self):
        text = SLIDES.read_text(encoding="utf-8")

        required_phrases = [
            "draft teman",
            "Poisson",
            "Bayes",
            "Gamma",
            "mengapa prior ini",
            "posterior",
            "prediktif posterior",
            "2010",
            "2014",
            "2018",
            "2022",
            "1930-2018",
            "aktual 2022",
            "probabilitas prediksi",
            "lebih dari 2.5 gol",
            "keterbatasan",
        ]

        for phrase in required_phrases:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase.lower(), text.lower())

        slide_count = len(re.findall(r"^---$", text, flags=re.MULTILINE)) + 1
        self.assertGreaterEqual(slide_count, 12)
        self.assertLessEqual(slide_count, 18)

    def test_notebook_has_executable_bayesian_poisson_workflow(self):
        notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
        cells = notebook["cells"]
        markdown = "\n".join(
            "".join(cell.get("source", []))
            for cell in cells
            if cell.get("cell_type") == "markdown"
        )
        code = "\n".join(
            "".join(cell.get("source", []))
            for cell in cells
            if cell.get("cell_type") == "code"
        )

        self.assertIn("Bayesian Poisson", markdown)
        self.assertIn("Gamma", markdown)
        self.assertIn("Prediktif posterior", markdown)
        self.assertIn("Bahasa Indonesia", markdown)
        self.assertIn("train_years = [2010, 2014, 2018]", code)
        self.assertIn("test_year = 2022", code)
        self.assertIn("alpha_post = alpha_prior + train_total_goals", code)
        self.assertIn("beta_post = beta_prior + train_match_count", code)
        self.assertIn("negative_binomial_predictive_pmf", code)
        self.assertIn("ascii_bar_chart", code)
        self.assertIn("actual_vs_predicted_rows", code)
        self.assertIn("credible_interval", code)
        self.assertIn("all_prior_years", code)

    def test_visible_language_is_polished_indonesian(self):
        visible_text = SLIDES.read_text(encoding="utf-8")
        notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))

        for cell in notebook["cells"]:
            if cell.get("cell_type") == "markdown":
                visible_text += "\n" + "".join(cell.get("source", []))

        awkward_phrases = [
            "data training",
            "model utama",
            "diberi prior",
            "mengamati tepat",
            "turnamen modern",
            "masuk akal menurut model",
            "berangkat dari draft teman",
            "memoles draft teman",
            "reproducible",
            "end-to-end",
            "Actual 2022",
            "Comparison of expected",
            "Posterior Predictive Distribution",
            "Historical Training Choice",
        ]

        for phrase in awkward_phrases:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase.lower(), visible_text.lower())

    def test_worldcup_dataset_expected_modern_match_counts(self):
        expected_counts = {2010: 64, 2014: 64, 2018: 64, 2022: 64}

        for year, expected in expected_counts.items():
            path = ROOT / "worldcup.json" / str(year) / "worldcup.json"
            data = json.loads(path.read_text(encoding="utf-8"))
            scored = [
                match
                for match in data["matches"]
                if "score" in match and "ft" in match["score"]
            ]

            with self.subTest(year=year):
                self.assertEqual(len(scored), expected)


if __name__ == "__main__":
    unittest.main()
