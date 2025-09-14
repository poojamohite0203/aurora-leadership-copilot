from ollama_client import query_ollama
import json

EXTRACTION_PROMPT = """
You are an assistant that extracts structured meeting insights.
Given the following text, extract:
- Decisions
- Action Items
- Blockers

Return JSON in this format:
{
  "decisions": [...],
  "action_items": [...],
  "blockers": [...]
}

Meeting transcript:
"{text}"
"""

def extract_meeting_insights(transcript: str):
    prompt = EXTRACTION_PROMPT.format(text=transcript)
    response = query_ollama(prompt)
    try:
        return json.loads(response)
    except:
        return {"raw_output": response}

if __name__ == "__main__":
    sample = "We decided to use Python. John will update Jira. Sarah mentioned the API is still down."
    print(extract_meeting_insights(sample))
