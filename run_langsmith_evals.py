import os
from dotenv import load_dotenv
from langsmith import traceable
from langsmith.client import Client
from langsmith_evals import (
    SummaryNotEmptyEval,
    OutputIsValidJSONEval,
    ContentSafetyEval,
    SemanticSimilarityEval,
)

# Load environment variables from .env
load_dotenv()

# Example run data (replace with your actual LLM output)
class SimpleRun:
    def __init__(self, output):
        self.output = output

run = SimpleRun(output={"summary": "This is a test summary."})

reference = "This is a test summary."  # For similarity eval

# Instantiate evals
EVALS = [
    SummaryNotEmptyEval(),
    OutputIsValidJSONEval(),
    ContentSafetyEval(),
    SemanticSimilarityEval(),
]

client = Client()

run_obj = client.create_run(
    name="Local Eval Run",
    project_name="aurora-leadership-copilot",
    run_type="tool",
    inputs={"summary": run.output.get("summary", "")},
)
print(f"create_run returned: {run_obj}")
# if run_obj is None:
#     print("LANGCHAIN_API_KEY:", os.getenv("LANGCHAIN_API_KEY"))
#     print("LANGSMITH_API_KEY:", os.getenv("LANGSMITH_API_KEY"))
#     print("LANGCHAIN_ENDPOINT:", os.getenv("LANGCHAIN_ENDPOINT"))
#     print("Project name:", "aurora-leadership-copilot")
#     print("Failed to create run. Check your API key, project name, and network connectivity.")
#     exit(1)
#run_id = run_obj.id

PROJECT_ID = "93ddcb3a-ed58-449d-a637-a19a0827bedf"  # TODO: Replace with your actual project UUID from LangSmith dashboard

client = Client()

@traceable
def run_and_log_evals(run, reference=None):
    results = []
    for eval in EVALS:
        result = eval.run(run, reference=reference)
        results.append(result)
        print(f"{eval.__class__.__name__}: {result.passed}, {result.comment}")
        client.create_feedback(
            key=eval.__class__.__name__,
            score=result.score,
            comment=result.comment,
            project_id=PROJECT_ID
        )
    print("Eval results complete and published to LangSmith!")
    return results

run_and_log_evals(run, reference=reference)
