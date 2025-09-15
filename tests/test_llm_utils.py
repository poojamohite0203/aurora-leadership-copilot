import json
import pytest
from src.core import extract_insights_from_text
from src.core import prompt_templates

def test_extract_meeting_insights_basic():
    transcript = (
        "We decided to use Python. "
        "John will update Jira. "
        "Sarah mentioned the API is still down."
    )

    result = extract_insights_from_text(transcript, prompt_templates.MEETING_EXTRACTION_PROMPT)

    print("LLM Response:", result)  # Debug print to see the actual response

    # Case 1: If LLM responds in proper JSON
    if isinstance(result, dict) and "title" in result:
        assert "title" in result
        assert "participants" in result
        assert "summary" in result
        assert "action_items" in result
        assert "decisions" in result
        assert "blockers" in result

        # Further checks for nested structures (optional)
        assert isinstance(result["action_items"], list)
        assert isinstance(result["decisions"], list)
        assert isinstance(result["blockers"], list)

    # Case 2: If LLM responds in raw text (fallback)
    else:
        assert "raw_output" in result
        assert isinstance(result["raw_output"], str)


def test_extract_meeting_insights_empty():
    transcript = ""
    result = extract_insights_from_text(transcript, prompt_templates.MEETING_EXTRACTION_PROMPT)
    
    # It should either return empty lists or raw output
    if "raw_output" in result:
        assert isinstance(result["raw_output"], str)
    else:
        assert isinstance(result["title"], str)
        assert isinstance(result["participants"], list)
        assert isinstance(result["summary"], str)
        assert isinstance(result["action_items"], list)
        assert isinstance(result["decisions"], list)
        assert isinstance(result["blockers"], list)