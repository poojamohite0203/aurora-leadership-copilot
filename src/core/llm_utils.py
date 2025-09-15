import subprocess
import json

def query_ollama(prompt: str, model: str = "llama3.1"):
    result = subprocess.run(
        ["ollama", "run", model],
        input=prompt.encode("utf-8"),
        capture_output=True
    )
    return result.stdout.decode("utf-8")

if __name__ == "__main__":
    print(query_ollama("Summarize: We discussed project X and Bob will write the docs. Alice flagged a blocker with API access."))
