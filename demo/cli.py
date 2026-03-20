import argparse
import json
from pathlib import Path

from demo.config import ARTIFACT_ROOT, CATEGORY_DESCRIPTIONS, DEFAULT_CATEGORIES
from demo.stages.execution_engine import execute_plan
from demo.stages.stage1_corpus_generator import generate_stage1_corpus
from demo.stages.stage1_llm_inference import infer_parts
from demo.stages.stage2_corpus_generator import generate_stage2_corpus
from demo.stages.stage2_llm_inference import infer_assembly
from demo.visualization.renderer import summarize_report


def _default_prompt(category: str) -> str:
    return CATEGORY_DESCRIPTIONS.get(category, f"Generate a concept template for {category}")


def cmd_generate_corpus(args):
    s1 = generate_stage1_corpus()
    s2 = generate_stage2_corpus(args.categories)
    print(f"Generated: {s1}")
    print(f"Generated: {s2}")


def cmd_run_stage1(args):
    prompt = args.prompt or _default_prompt(args.category)
    result = infer_parts(args.category, prompt)
    print(json.dumps(result.__dict__, indent=2))


def cmd_run_stage2(args):
    prompt = args.prompt or _default_prompt(args.category)
    s1 = infer_parts(args.category, prompt)
    s2 = infer_assembly(args.category, prompt, s1.parts)
    print(json.dumps(s2.__dict__, indent=2))


def cmd_run_e2e(args):
    prompt = args.prompt or _default_prompt(args.category)
    s1 = infer_parts(args.category, prompt)
    s2 = infer_assembly(args.category, prompt, s1.parts)
    report = execute_plan(args.category, s2.assembly_plan)
    print(summarize_report(report))


def cmd_verify(args):
    ARTIFACT_ROOT.mkdir(parents=True, exist_ok=True)
    failures = []
    for category in args.categories:
        prompt = _default_prompt(category)
        s1 = infer_parts(category, prompt)
        s2 = infer_assembly(category, prompt, s1.parts)
        report = execute_plan(category, s2.assembly_plan)
        print(summarize_report(report))
        if not report["mesh_ok"]:
            failures.append(category)

    if failures:
        raise SystemExit(f"Verification failed for: {', '.join(failures)}")


def build_parser():
    parser = argparse.ArgumentParser(description="STL-C demo workflow CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p_corpus = sub.add_parser("generate-corpus")
    p_corpus.add_argument("--categories", nargs="+", default=list(DEFAULT_CATEGORIES))
    p_corpus.set_defaults(func=cmd_generate_corpus)

    p_s1 = sub.add_parser("run-stage1")
    p_s1.add_argument("--category", default="Laptop")
    p_s1.add_argument("--prompt", default="")
    p_s1.set_defaults(func=cmd_run_stage1)

    p_s2 = sub.add_parser("run-stage2")
    p_s2.add_argument("--category", default="Laptop")
    p_s2.add_argument("--prompt", default="")
    p_s2.set_defaults(func=cmd_run_stage2)

    p_e2e = sub.add_parser("run-e2e")
    p_e2e.add_argument("--category", default="Laptop")
    p_e2e.add_argument("--prompt", default="")
    p_e2e.set_defaults(func=cmd_run_e2e)

    p_verify = sub.add_parser("verify")
    p_verify.add_argument("--categories", nargs="+", default=list(DEFAULT_CATEGORIES))
    p_verify.set_defaults(func=cmd_verify)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
