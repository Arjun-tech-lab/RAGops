import json

from retrieval_engine import search_project


# =====================================================
# LOAD BENCHMARK QUESTIONS
# =====================================================

with open("benchmark_questions.json", "r") as f:

    benchmarks = json.load(f)


# =====================================================
# METRICS
# =====================================================

top1_correct = 0

top3_correct = 0

total = len(benchmarks)


# =====================================================
# RUN BENCHMARKS
# =====================================================

for benchmark in benchmarks:

    question = benchmark["question"]

    expected_file = benchmark["expected_file"]


    # =================================================
    # RUN RETRIEVAL
    # =================================================

    results = search_project(question)


    # =================================================
    # EXTRACT TOP RESULTS
    # =================================================

    top_results = results[:3]


    retrieved_files = []

    for result in top_results:

        path = result["metadata"]["path"]

        filename = path.split("/")[-1]

        retrieved_files.append(filename)


    # =================================================
    # TOP-1 CHECK
    # =================================================

    top1_match = (
        retrieved_files[0] == expected_file
    )


    if top1_match:
        top1_correct += 1


    # =================================================
    # TOP-3 CHECK
    # =================================================

    top3_match = (
        expected_file in retrieved_files
    )


    if top3_match:
        top3_correct += 1


    # =================================================
    # PRINT QUESTION HEADER
    # =================================================

    print("\n")
    print("=" * 100)

    print(f"QUESTION: {question}")

    print(f"EXPECTED: {expected_file}")

    print("\n")


    # =================================================
    # PRINT RETRIEVAL RESULTS
    # =================================================

    for rank, result in enumerate(top_results):

        metadata = result["metadata"]

        filename = metadata["path"].split("/")[-1]

        print("-" * 80)

        print(f"RANK: {rank + 1}")

        print(f"FILE: {filename}")

        print(f"SERVICE: {metadata['service']}")

        print(f"TYPE: {metadata['type']}")

        print(f"FINAL SCORE: {result['final_score']}")

        print("\n")


    # =================================================
    # RESULT STATUS
    # =================================================

    print("=" * 100)

    print(f"TOP-1 RESULT: {'PASS' if top1_match else 'FAIL'}")

    print(f"TOP-3 RESULT: {'PASS' if top3_match else 'FAIL'}")

    print("\n")


# =====================================================
# FINAL METRICS
# =====================================================

top1_accuracy = (
    top1_correct / total
) * 100

top3_accuracy = (
    top3_correct / total
) * 100


print("\n")
print("=" * 100)

print("FINAL RETRIEVAL METRICS")

print("=" * 100)

print(f"TOTAL QUESTIONS: {total}")

print("\n")

print(
    f"TOP-1 ACCURACY: "
    f"{top1_accuracy:.2f}% "
    f"({top1_correct}/{total})"
)

print(
    f"TOP-3 ACCURACY: "
    f"{top3_accuracy:.2f}% "
    f"({top3_correct}/{total})"
)

print("\n")