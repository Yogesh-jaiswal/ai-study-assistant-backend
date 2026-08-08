import os
os.environ["ENVIRONMENT"] = "evaluation"

import json
from collections import defaultdict
from datetime import datetime, timezone
import time

from flask import Flask

from deepeval.metrics import (
    AnswerRelevancyMetric,
    ContextualRelevancyMetric,
    FaithfulnessMetric,
)
from deepeval.test_case import LLMTestCase

from services.retrieval.similarity_search_service import SimilaritySearchService
from services.retrieval.context_assembler import ContextAssembler
from services.chat.chat_generator import ChatGenerator

from rag_evaluation.setup import setup
from .deepeval_judge import DeepEvalJudge

DATASET_FILE = "rag_evaluation/dataset.json"
REPORT_FILE = "rag_evaluation/report.json"

# Change this while testing
QUESTION_LIMIT = 1

judge = DeepEvalJudge()

# Define the metrics to be used for evaluation
metrics = [
    AnswerRelevancyMetric(
        threshold=0.7,
        include_reason=True,
        async_mode=False,
        model=judge,
    ),
    FaithfulnessMetric(
        threshold=0.7,
        include_reason=True,
        async_mode=False,
        model=judge,
    ),
    ContextualRelevancyMetric(
        threshold=0.7,
        include_reason=True,
        async_mode=False,
        model=judge,
    ),
]


def load_dataset(limit: int | None = None) -> list[dict]:
    """Loads the dataset from a JSON file and optionally limits the number of samples returned."""
    with open(DATASET_FILE, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    if limit is not None:
        dataset = dataset[:limit]

    return dataset


def build_test_cases(
    notebook_id: str,
    user_id: str,
    dataset: list[dict],
) -> list[LLMTestCase]:
    """Builds test cases by retrieving relevant context for each question in the dataset and generating answers using the chat generator."""

    search_engine = SimilaritySearchService()
    generator = ChatGenerator()

    test_cases: list[LLMTestCase] = []

    total = len(dataset)

    for index, sample in enumerate(dataset, start=1):

        question = sample["question"]

        print(f"\n[{index}/{total}] {question}")

        print("Searching...")
        start = time.perf_counter()

        retrieved_chunks = search_engine.search(
            notebook_id,
            user_id,
            question,
        )

        print(
            f"Retrieved {len(retrieved_chunks)} chunk(s) "
            f"in {time.perf_counter() - start:.2f}s"
        )

        if not retrieved_chunks:
            print("Skipped (no retrieved chunks)")
            continue

        context = ContextAssembler.build_context(retrieved_chunks)

        print("Generating answer...")

        start = time.perf_counter()

        response = generator.generate(
            question,
            context.to_text(),
        )

        print(
            f"Answer generated in "
            f"{time.perf_counter() - start:.2f}s"
        )

        test_cases.append(
            LLMTestCase(
                input=question,
                actual_output=response["response"],
                expected_output=sample["expected_output"],
                retrieval_context=[
                    chunk.chunk.text
                    for chunk in retrieved_chunks
                ],
            )
        )

    return test_cases


def write_report(
    test_cases: list[LLMTestCase],
):
    """Evaluates the test cases using the defined metrics and writes a report to a JSON file."""

    report: list[dict] = []

    total_scores = defaultdict(float)
    total_passes = defaultdict(int)
    metric_counts = defaultdict(int)

    for case_index, test_case in enumerate(test_cases, start=1):

        print(
            f"\nEvaluating question "
            f"{case_index}/{len(test_cases)}"
        )

        case_result = {
            "question": test_case.input,
            "metrics": [],
        }

        for metric_index, metric in enumerate(metrics):

            metric_name = metric.__class__.__name__

            print(f"Running {metric_name}...")

            start = time.perf_counter()

            try:

                metric.measure(test_case)

                elapsed = time.perf_counter() - start

                print(
                    f"{metric_name} completed "
                    f"in {elapsed:.2f}s"
                )

                score = float(metric.score or 0.0)
                passed = metric.is_successful()

                total_scores[metric_name] += score
                metric_counts[metric_name] += 1

                if passed:
                    total_passes[metric_name] += 1

                case_result["metrics"].append(
                    {
                        "metric": metric_name,
                        "score": round(score, 4),
                        "passed": passed,
                        "reason": metric.reason,
                        "duration_seconds": round(elapsed, 2),
                    }
                )

            except Exception as e:

                elapsed = time.perf_counter() - start

                print(
                    f"{metric_name} FAILED "
                    f"in {elapsed:.2f}s"
                )

                print(str(e))

                # Save the failure instead of crashing
                case_result["metrics"].append(
                    {
                        "metric": metric_name,
                        "score": None,
                        "passed": False,
                        "reason": str(e),
                        "duration_seconds": round(elapsed, 2),
                    }
                )

                # Skip remaining metrics if daily quota is exhausted.
                # This avoids wasting time after the quota is already gone.
                if "RESOURCE_EXHAUSTED" in str(e):
                    print(
                        "\nGemini quota exhausted. "
                        "Skipping remaining metrics.\n"
                    )
                    break

            # Cooldown between metrices to avoid hitting API rate limits, especially for Gemini.
            if metric_index < len(metrics) - 1:
                print("\nSleeping 35 seconds...\n")
                time.sleep(35)

        report.append(case_result)

    # Summarize the results and write to a report file
    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "questions": len(test_cases),
        "metrics": {},
    }

    for metric_name in metric_counts:

        count = metric_counts[metric_name]

        summary["metrics"][metric_name] = {
            "average_score": round(
                total_scores[metric_name] / count,
                4,
            ),
            "pass_rate": round(
                total_passes[metric_name] / count,
                4,
            ),
        }

    final_report = {
        "summary": summary,
        "results": report,
    }

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(
            final_report,
            f,
            indent=4,
        )

    print(f"\nReport written to {REPORT_FILE}")


def evaluate():
    """Main evaluation function that sets up the application, loads the dataset, builds test cases, and writes the evaluation report."""

    print("Running setup...")

    app: Flask
    app, state = setup()

    print("Loading dataset...")

    dataset = load_dataset(limit=QUESTION_LIMIT)

    with app.app_context():

        test_cases = build_test_cases(
            notebook_id=state["notebook_id"],
            user_id=state["user_id"],
            dataset=dataset,
        )

        if not test_cases:
            print("No test cases generated.")
            return

        write_report(test_cases)

    print("Evaluation complete.")


if __name__ == "__main__":
    evaluate()