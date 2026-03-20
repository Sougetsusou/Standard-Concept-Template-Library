from demo.stages.execution_engine import execute_plan
from demo.stages.stage1_llm_inference import infer_parts
from demo.stages.stage2_llm_inference import infer_assembly
from demo.visualization.renderer import summarize_report


def main():
    category = "Mug"
    prompt = "Create a mug with a hollow cylindrical body and one curved side handle."
    s1 = infer_parts(category, prompt)
    s2 = infer_assembly(category, prompt, s1.parts)
    report = execute_plan(category, s2.assembly_plan)
    print(summarize_report(report))


if __name__ == "__main__":
    main()
