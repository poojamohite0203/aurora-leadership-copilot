import re
from core.llm_utils import query_ollama
import json

# EXTRACTION_PROMPT = """
# You are an assistant that extracts structured meeting insights.
# Given the following text, extract:
# - Decisions
# - Action Items
# - Blockers

# Return JSON in this format:
# {{
#   "decisions": [...],
#   "action_items": [...],
#   "blockers": [...]
# }}

# Meeting transcript:
# "{text}"
# """

MEETING_EXTRACTION_PROMPT = """
You are an AI assistant. Extract structured information from a meeting transcript. 
Return the output in strict JSON format.

Transcript:
"{text}"


Output JSON fields:
{{
  'title': 'Suggested title based on context',
  'participants': ['List of participants'],
  'summary': 'Brief summary of meeting',
  'action_items': [
      {{'description': '...', 'due_date': '...'}}
  ],
  'decisions': [
      {{'description': '...', 'other_options': ['...']}}
  ],
  'blockers': [
      {{'description': '...'}}
  ]
}}


Make sure JSON is valid.
The 'title' key should contain a string.
The 'participants' key should contain a list of strings.
The 'summary' key should contain a string.
The 'action_items' key should contain a list of dictionaries, where each dictionary has a 'description' key and a 'due_date' key.
The 'decisions' key should contain a list of dictionaries, where each dictionary has a 'description' key and an 'other_options' key.
The 'blockers' key should contain a list of dictionaries, where each dictionary has a 'description' key.
"""


def extract_meeting_insights(transcript: str):
    prompt = MEETING_EXTRACTION_PROMPT.format(text=transcript)
    print("Prompt being sent to LLM:", prompt)
    response = query_ollama(prompt)
    print("Raw LLM Response:", response)

    try:
        # Extract JSON portion using regex (more specific)
        match = re.search(r"```json\n(.*)\n```", response, re.DOTALL)
        if match:
            json_string = match.group(1)
            return json.loads(json_string)
        else:
            match = re.search(r"\{(.*)\}", response, re.DOTALL)
            if match:
                json_string = match.group(1)
                return json.loads(json_string)
            else:
                print("No JSON found in LLM response")
                return {"raw_output": response}
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return {"raw_output": response}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"raw_output": response}

if __name__ == "__main__":
    sample = "We decided to use Python. John will update Jira. Sarah mentioned the API is still down."
    print(extract_meeting_insights(sample))