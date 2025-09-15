import re
from core.llm_utils import query_ollama
import json

MEETING_EXTRACTION_PROMPT = """
You are an AI assistant. Extract structured information from a meeting transcript. 
The transcript may include timestamps, speaker names, and natural conversation flow.
Parse the content regardless of format (timestamps, speaker labels, etc.).
Return the output in strict JSON format.

Transcript:
"{text}"

Instructions:
- Extract participant names from speaker labels (e.g., "Luong, Vito (V.)", "Jeter, Colton (C.)")
- Ignore timestamps and formatting artifacts  
- Focus on the actual conversation content
- Identify clear action items, decisions, and blockers from the discussion
- Create a meaningful title based on the meeting topic

Output JSON fields:
{{
  'title': 'Suggested title based on context',
  'participants': ['List of participants'],
  'summary': 'Brief summary of meeting',
  'action_items': [
      {{'description': '...', 'due_date': '...'}}
  ],
  'decisions': [
      {{'description': '...', 'other_options': {{}}}}
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

CLIP_EXTRACTION_PROMPT = """
You are an AI assistant. Extract structured insights from the given text.
Return the output in strict JSON format.
action_items, decisions, blockers can be empty list if not relevant.

Transcript:
"{text}"

Output JSON fields:
{{
  'text': 'Original text snippet',
  'summary': 'Brief summary of meeting',
  'action_items': [
      {{'description': '...', 'due_date': '...'}}
  ],
  'decisions': [
      {{'description': '...', 'other_options': {{}}}}
  ],
  'blockers': [
      {{'description': '...'}}
  ]
}}


Make sure JSON is valid.
The 'text' key should contain a string and original text.
The 'summary' key should contain a string.
The 'action_items' key should contain a list of dictionaries, where each dictionary has a 'description' key and a 'due_date' key.
The 'decisions' key should contain a list of dictionaries, where each dictionary has a 'description' key and an 'other_options' key.
The 'blockers' key should contain a list of dictionaries, where each dictionary has a 'description' key.
"""

JOURNAL_EXTRACTION_PROMPT = """
You are an AI assistant. Extract structured insights from the given journal entry.
Return the output in strict JSON format.
action_items, decisions, blockers can be empty list if not relevant.

Transcript:
"{text}"

Output JSON fields:
{{
  'text': 'Original text snippet',
  'summary': 'Brief summary of meeting',
  'theme': 'Identified theme',
  'strength': 'Identified strength',
  'growth_area': 'Identified growth area',
  'action_items': [
      {{'description': '...', 'due_date': '...'}}
  ],
  'decisions': [
      {{'description': '...', 'other_options': {{}}}}
  ],
  'blockers': [
      {{'description': '...'}}
  ]
}}


Make sure JSON is valid.
The 'text' key should contain a string and original text.
The 'summary' key should contain a string.
The 'action_items' key should contain a list of dictionaries, where each dictionary has a 'description' key and a 'due_date' key.
The 'decisions' key should contain a list of dictionaries, where each dictionary has a 'description' key and an 'other_options' key.
The 'blockers' key should contain a list of dictionaries, where each dictionary has a 'description' key.
"""

def extract_insights_from_text(
    text: str, 
    prompt_template: str
):
    """
    Generalized method to extract structured insights from any text
    using a provided prompt template.
    
    Args:
        text (str): The raw input text (meeting, clip, or journal).
        prompt_template (str): The template to use for LLM prompt.
    
    Returns:
        dict: Parsed JSON output from LLM or raw output on failure.
    """
    prompt = prompt_template.format(text=text)
    # print("Prompt being sent to LLM:", prompt)
    response = query_ollama(prompt)
    # print("Raw LLM Response:", response)

    try:
        # First try fenced ```json blocks
        match = re.search(r"```json\n(.*)\n```", response, re.DOTALL)
        if match:
            json_string = match.group(1)
            return json.loads(json_string)
        
        # Fallback: try any {} JSON block
        match = re.search(r"\{.*\}", response, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        
        # If no JSON, return raw output
        print("No JSON found in LLM response")
        return {"raw_output": response}

    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return {"raw_output": response}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"raw_output": response}