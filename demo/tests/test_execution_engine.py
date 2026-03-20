import unittest

from demo.stages.execution_engine import execute_plan
from demo.stages.presets import PRESET_WORKFLOW


class TestExecutionEngine(unittest.TestCase):
    def test_execute_laptop_plan(self):
        report = execute_plan("Laptop", PRESET_WORKFLOW["Laptop"]["parts"])
        self.assertTrue(report["mesh_ok"])
        self.assertGreater(report["vertex_count"], 0)
        self.assertGreater(report["face_count"], 0)


if __name__ == "__main__":
    unittest.main()
