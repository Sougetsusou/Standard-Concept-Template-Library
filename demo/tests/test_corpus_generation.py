import json
import unittest

from demo.stages.stage1_corpus_generator import generate_stage1_corpus
from demo.stages.stage2_corpus_generator import generate_stage2_corpus


class TestCorpusGeneration(unittest.TestCase):
    def test_stage1_corpus_generated(self):
        path = generate_stage1_corpus()
        self.assertTrue(path.exists())
        first_line = path.read_text(encoding="utf-8").splitlines()[0]
        row = json.loads(first_line)
        self.assertIn("task", row)
        self.assertEqual(row["task"], "write_part_class")

    def test_stage2_corpus_generated(self):
        path = generate_stage2_corpus(["Laptop", "Mug"])
        self.assertTrue(path.exists())
        lines = path.read_text(encoding="utf-8").splitlines()
        self.assertGreaterEqual(len(lines), 2)


if __name__ == "__main__":
    unittest.main()
