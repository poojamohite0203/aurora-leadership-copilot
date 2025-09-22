import subprocess
import json
from openai import OpenAI
import os
from dotenv import load_dotenv

def query_ollama(prompt: str, model: str = "llama3.1"):
    result = subprocess.run(
        ["ollama", "run", model],
        input=prompt.encode("utf-8"),
        capture_output=True
    )
    return result.stdout.decode("utf-8")

def query_gpt(prompt: str, model: str = "gpt-4o-mini") -> str:
    """
    Query OpenAI's GPT model using the same API key as check_moderation.
    Returns the generated text as a string.
    """
    load_dotenv()
    import os
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=512,
        temperature=0.7
    )
    # Extract the assistant's reply
    return response.choices[0].message.content.strip()

def validate_llm_output(data: dict, required_fields: list) -> bool:
    """
    Ensure all required fields exist and are of correct type.
    """
    for field in required_fields:
        if field not in data or not isinstance(data[field], str) or not data[field].strip():
            return False
    return True

def is_content_length_valid(text: str, min_len: int = 20, max_len: int = 2000) -> bool:
    """
    Guardrail: Ensure content is not too short, not too long, and not obviously truncated.
    """
    if not isinstance(text, str):
        return False
    text = text.strip()
    if len(text) < min_len or len(text) > max_len:
        return False
    # Check for truncation
    if text.endswith("...") or text.endswith("..") or text.endswith(" . . ."):
        return False
    return True

def is_content_safe(text: str) -> bool:
    """
    Guardrail: Check for unsafe content (PII, profanity, hate speech, racism, sexism, etc.).
    This is a simple keyword-based filter. For production, use a dedicated content moderation API.
    """
    if not isinstance(text, str):
        return False
    # Example: Add more as needed
    unsafe_keywords = [
        # ...existing...
        'fuck', 'shit', 'bitch', 'asshole', 'nigger', 'faggot', 'cunt', 'slut',
        # Racism/sexism/bias examples:
        'all women are', 'all men are', 'white people are', 'black people are',
        'jew', 'muslim', 'terrorist', 'slave', 'inferior', 'superior',
        'retard', 'cripple', 'illegal alien', 'go back to your country',
        # Add more as needed
    ]
    lowered = text.lower()
    for word in unsafe_keywords:
        if word in lowered:
            return False
    return True

def validate_llm_summary_output(
    extracted: dict,
    required_fields: list = ["summary"],
    context: str = "summary"
) -> str:
    """
    Central guardrail: Validate LLM output for required fields, content length, and safety.
    Returns the summary string if valid, else raises ValueError with a specific message.
    """
    print("LLM Response:", extracted)
    if "raw_output" in extracted:
        print(f"LLM extraction failed for {context}")
        raise ValueError(f"LLM extraction failed for {context}")
    if not validate_llm_output(extracted, required_fields):
        print(f"LLM output format invalid for {context}")
        raise ValueError(f"LLM output format invalid for {context}")
    
    summary = extracted.get("summary", "")

    if not is_content_length_valid(summary):
        print(f"LLM output content invalid for {context}")
        raise ValueError(f"LLM output content invalid for {context}")
    if not is_content_safe(summary):
        print(f"LLM output flagged as unsafe for {context}")
        raise ValueError(f"LLM output flagged as unsafe for {context}")
    if not detect_hallucination(summary, context):
        print(f"LLM output may contain hallucinated facts for {context}")
        raise ValueError(f"LLM output may contain hallucinated facts for {context}")
    ok, categories = check_moderation(summary)
    if not ok:
         print(f"LLM output blocked due to: {categories}")
         raise ValueError(f"LLM output blocked due to: {categories}")
        
    return sanitize_llm_input_output(summary)

def sanitize_llm_input_output(text: str) -> str:
    """
    Sanitize user input before including in LLM prompts to mitigate prompt injection.
    Removes or escapes suspicious patterns (curly braces, backticks, etc.).
    """
    if not isinstance(text, str):
        return ""
    sanitized = text.replace('{', '').replace('}', '').replace('`', '').replace('"""', '').replace("'''", '')
    # Add more sophisticated checks as needed
    return sanitized

def detect_hallucination(output: str, context: str) -> bool:
    """
    Detect hallucinated facts in LLM output by checking if output mentions entities not in context.
    For production, use NLP/entity matching. Here, just a placeholder returning True (safe).
    """
    # TODO: Implement entity matching or more advanced checks
    return True

def check_moderation(text: str):
    load_dotenv()
    import os
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.moderations.create(
        model="omni-moderation-latest",
        input=text
    )
    results = response.results[0]
    if results.flagged:
        return False, results.categories
    return True, None
