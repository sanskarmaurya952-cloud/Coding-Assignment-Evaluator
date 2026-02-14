# example_usage.py
from main_evaluator import CodingEvaluator, Language

# Initialize evaluator
evaluator = CodingEvaluator(
    openai_api_key="your-key",
    github_token="your-token"
)

# Example 1: Direct code evaluation
code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
"""

test_cases = [
    {"function_call": "fibonacci(0)", "expected": "0"},
    {"function_call": "fibonacci(1)", "expected": "1"},
    {"function_call": "fibonacci(5)", "expected": "5"},
]

result = evaluator.evaluate_submission(
    code_input=code,
    problem_description="Calculate the nth Fibonacci number",
    test_cases=test_cases,
    language=Language.PYTHON
)

print(f"Overall Score: {result.overall_score}/100")
print(f"Correctness: {result.correctness_score}/100")
print(f"Suggestions: {result.suggestions}")

# Example 2: GitHub URL evaluation
github_url = "https://github.com/username/repo/blob/main/solution.py"
result = evaluator.evaluate_submission(github_url)

# Example 3: File evaluation
result = evaluator.evaluate_submission("solution.py")
