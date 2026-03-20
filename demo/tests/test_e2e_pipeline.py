import unittest

from demo.stages.execution_engine import execute_plan
from demo.stages.stage1_llm_inference import infer_parts
from demo.stages.stage2_llm_inference import infer_assembly


class TestE2EPipeline(unittest.TestCase):
    def test_laptop_e2e(self):
        prompt = "Create a practical laptop"
        s1 = infer_parts("Laptop", prompt)
        s2 = infer_assembly("Laptop", prompt, s1.parts)
        report = execute_plan("Laptop", s2.assembly_plan)
        self.assertTrue(report["mesh_ok"])

    def test_mug_e2e(self):
        prompt = "Create a mug"
        s1 = infer_parts("Mug", prompt)
        s2 = infer_assembly("Mug", prompt, s1.parts)
        report = execute_plan("Mug", s2.assembly_plan)
        self.assertTrue(report["mesh_ok"])


if __name__ == "__main__":
    unittest.main()
