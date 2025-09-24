# Project Learning Log

### Topics
- A Python virtual environment (venv) is an isolated, self-contained directory that holds a specific Python interpreter and its own set of installed packages for a project. Using a venv prevents conflicts between different projects that require conflicting versions of the same package. (very similar to external libraries from spring)
    ### Code Snippets / Commands
    ```python
    # Example: creating a virtual environment
    python -m venv 

    ### Activating the virtual environment
    **On macOS / Linux:**
    ```sh
        source .venv/bin/activate
        **On Windows :**
        .venv\Scripts\activate


- The __init__.py file serves two primary functions in Python: to mark a directory as a regular package and to control what happens when that package is imported.
    1. Marks a directory as a regular package
        Historically, Python would only treat a directory as a package if it contained an __init__.py file. Without this marker, Python would not look inside the directory for modules during an import statement. 
    2. Runs initialization code
        The code inside the __init__.py file is executed the first time its package is imported.
        ## Example of creating a clean API:
            Imagine a project with a tools package containing submodules math_tools and string_tools.
            tools/
            ├── __init__.py
            ├── math_tools.py
            └── string_tools.py
            math_tools.py contains def add(a, b): ...
            string_tools.py contains def reverse(s): ...        
    ### Code Snippets / Commands
    ```python
    # Example:
    from .math_tools import add
    from .string_tools import reverse

    # Other File using it can import as 
    from tools import add, reverse

- Pydantic: Pydantic is the most widely used data validation and settings management library for Python (very similar to javax.validation (Spring Background))
    ### Code Snippets / Commands
    ```python
        from pydantic import BaseModel, ValidationError

        # Define a Pydantic model for a user
        class User(BaseModel):
            id: int
            name: str = 'John Doe'
            email: str

        # Example with valid data
        user_data_valid = {
            'id': 123,
            'name': 'Jane Doe',
            'email': 'jane.doe@example.com'
        }

        user = User(**user_data_valid)
        print(f"Successfully created user: {user.model_dump_json()}")

        # Example with invalid data
        user_data_invalid = {
            'id': 'abc',  # Invalid type, should be int
            'name': 'Alice',
            'email': 'alice@' # Invalid email format
        }
- SQLLite : "SQLite is plug and play in Python" is accurate because the sqlite3 module is built-in to Python's standard library. This means you don't need to install any external packages or set up a separate server to start working with a database.There are 2 options to save data in-memory as well as a FIle - opted as File to have data even after app restarts.
     ### Code Snippets / Commands
        To initialize DB once 
        ```sh
        python -m src.db
- requirement.txt - similar to gradle - list of all necessary
    ### Code Snippets / Commands
        pip freeze > requirements.txt = cmd used to update requirement.txt when you manually install each from terminal
- To Delete Data from a table
    ### Code Snippets / Commands
        sqlite3 aurora.db "DELETE FROM weekly_report;"
- Types of Guardrails
    1. Output Format Validation -- "Implemented"
        Ensure the LLM output is valid JSON (if expected).
        Check that required fields (like "summary") are present and are strings, not objects.
        Fallback to a default message or retry if validation fails.
    2. Content Length & Completeness -- "Implemented"
        Set minimum and maximum length for the summary to avoid empty or excessively long outputs.
        Check for truncation (e.g., summary ending with "...") and handle accordingly.
    3. Content Safety -- "Implemented"
        Scan for PII (personally identifiable information) or sensitive data leaks.
        Filter profanity, hate speech, or unsafe content using a content moderation library or API.
    4. Prompt Injection & Hallucination Mitigation -- "Implemented"
        Sanitize user inputs before including them in prompts.
        Detect and handle hallucinated facts (e.g., summary claims that don't match input data).
    5. Retry & Fallback Logic
        Retry LLM call if output is invalid or empty.
        Fallback to a template-based summary if LLM fails repeatedly.
    6. Logging & Monitoring -- "Implemented"
        Log all LLM prompts and responses for auditing and debugging.
        Alert on repeated failures or suspicious outputs.
    7. Rate Limiting & Abuse Prevention
        Limit how often a user can generate reports to prevent abuse or accidental overload.
    8. User Feedback Loop
        Allow users to flag/report bad summaries for review and model improvement.

- How to re-install requirements.txt
        pip uninstall -r requirements.txt -y
            pip install -r requirements.txt

            OR    
             pip install --force-reinstall -r requirements.txt

# Build the image
docker build -t aurora-copilot .

# Run the container
docker run -p 8501:8501 aurora-copilot

# Run the cntainer with feature for it to rememebr data 
docker run -p 8501:8501 \
  -e OPENAI_API_KEY=your-openai-api-key \
  -v $(pwd)/src/db/aurora.db:/app/src/db/aurora.db \
  -v $(pwd)/.chroma:/app/.chroma \
  aurora-copilot

  # to run same way as it run on Render 
  docker run -p 8501:8501 \
  -e OPENAI_API_KEY=your-openai-api-key \
  -v $(pwd)/src/db/aurora.db:/app/src/db/aurora.db \
  -v $(pwd)/.chroma:/app/.chroma \
 -v RENDER = true \
  aurora-copilot
  
# when you run in docker - your app will be @ http://localhost:8501/

