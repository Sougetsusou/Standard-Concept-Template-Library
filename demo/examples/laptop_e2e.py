from demo.stages.execution_engine import execute_plan
from demo.stages.stage1_llm_inference import infer_parts
from demo.stages.stage2_llm_inference import infer_assembly
from demo.visualization.renderer import summarize_report


def main():
    category = "Laptop"
    prompt = "Create a practical laptop with a rectangular base, a thin hinged screen, and two rectangular side ports."
    s1 = infer_parts(category, prompt)
    s2 = infer_assembly(category, prompt, s1.parts)
    report = execute_plan(category, s2.assembly_plan)
    print(summarize_report(report))


if __name__ == "__main__":
    main()
