from llm_service import generate_answer


query = input(
    "\nDescribe issue/question: "
)


response = generate_answer(query)


print("\n")
print("=" * 80)
print("AI DEBUG ANALYSIS")
print("=" * 80)
print("\n")

print(response["answer"])