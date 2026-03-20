import unittest

from demo.stages.stage1_llm_inference import infer_parts
from demo.stages.stage2_llm_inference import infer_assembly


class TestMockInference(unittest.TestCase):
    def test_stage1_laptop(self):
        res = infer_parts("Laptop", "test")
        self.assertGreaterEqual(len(res.parts), 1)
        self.assertEqual(res.parts[0]["decision"], "use_existing")

    def test_stage2_laptop(self):
        s1 = infer_parts("Laptop", "test")
        s2 = infer_assembly("Laptop", "test", s1.parts)
        self.assertGreaterEqual(len(s2.assembly_plan), 1)
        self.assertIn("class_name", s2.assembly_plan[0])


if __name__ == "__main__":
    unittest.main()
