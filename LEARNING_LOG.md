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
- 


How to deploy ?
Models to hugging face - Explore 
Docker to any precompute service - 

change the url - 