import json
import os
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
            "Apa Itu Poisson",
            "Apa Itu Bayes",
            "Penggunaan Umum",
            "Apa yang Kita Lakukan",
            "Mengapa Model Ini Cocok",
            "Contoh Manual Poisson",
            "Contoh Manual Bayes Sederhana",
            "Contoh Manual Gamma-Poisson",
            "Perhitungan Manual Data Asli",
            "Rumus Prediktif Posterior",
            "mengapa prior gamma",
            "posterior",
            "prediktif posterior",
            "2014",
            "2018",
            "2022",
            "2026",
            "171",
            "169",
            "172",
            "512",
            "513",
            "193",
            "prediksi probabilistik",
            "goodness-of-fit",
            "keterbatasan",
            "Sumber",
            "NIST",
            "Stanford Encyclopedia",
            "Gelman",
            "Think Bayes",
            "Maher",
            "Dixon",
            "Panduan Gambar",
        ]

        for phrase in required_phrases:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase.lower(), text.lower())

        slide_count = len(re.findall(r"^---$", text, flags=re.MULTILINE)) + 1
        self.assertGreaterEqual(slide_count, 24)
        self.assertLessEqual(slide_count, 38)

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
        self.assertIn("prediktif posterior", markdown.lower())
        self.assertIn("Bahasa Indonesia", markdown)
        self.assertIn("analysis_years = [2014, 2018, 2022]", code)
        self.assertIn("alpha_prior = 1.0", code)
        self.assertIn("beta_prior = 1.0", code)
        self.assertIn("score_for_model", code)
        self.assertIn("alpha_post = alpha_prior + train_total_goals", code)
        self.assertIn("beta_post = beta_prior + train_match_count", code)
        self.assertIn("negative_binomial_predictive_pmf", code)
        self.assertIn("ascii_bar_chart", code)
        self.assertIn("predictive_rows", code)
        self.assertIn("credible_interval_from_pmf", code)
        self.assertIn("goodness_of_fit_rows", code)
        self.assertIn("posterior untuk 2026", markdown.lower())

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
            "data latih:",
            "data evaluasi:",
            "2010-2018",
            "1930-2018",
            "false positive",
            "false negative",
            "mean absolute error",
            "root mean squared error",
        ]

        for phrase in awkward_phrases:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase.lower(), visible_text.lower())

    def test_worldcup_dataset_expected_modern_match_counts(self):
        expected_counts = {2014: 64, 2018: 64, 2022: 64}

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

    def test_draft_aggregate_goal_totals_are_reproduced(self):
        notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
        namespace = {"__name__": "__notebook_test__"}
        original_cwd = Path.cwd()

        try:
            os.chdir(ROOT)
            for index, cell in enumerate(notebook["cells"], start=1):
                if cell.get("cell_type") == "code":
                    source = "".join(cell.get("source", []))
                    exec(compile(source, f"{NOTEBOOK.name}#cell-{index}", "exec"), namespace)
        finally:
            os.chdir(original_cwd)

        self.assertEqual(namespace["train_match_count"], 192)
        self.assertEqual(namespace["train_total_goals"], 512)
        self.assertEqual(namespace["alpha_post"], 513.0)
        self.assertEqual(namespace["beta_post"], 193.0)

    def test_notebook_code_runs_when_kernel_starts_in_notebook_folder(self):
        notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
        namespace = {"__name__": "__notebook_test__"}
        original_cwd = Path.cwd()

        try:
            os.chdir(NOTEBOOK.parent)
            for index, cell in enumerate(notebook["cells"], start=1):
                if cell.get("cell_type") == "code":
                    source = "".join(cell.get("source", []))
                    exec(compile(source, f"{NOTEBOOK.name}#cell-{index}", "exec"), namespace)
        finally:
            os.chdir(original_cwd)

        self.assertEqual(namespace["train_match_count"], 192)
        self.assertEqual(namespace["train_total_goals"], 512)


if __name__ == "__main__":
    unittest.main()
