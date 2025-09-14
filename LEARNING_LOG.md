# Project Learning Log

### What I Worked On
- Creating Repo and Base Project Structure.

### What I Learned
- A Python virtual environment (venv) is an isolated, self-contained directory that holds a specific Python interpreter and its own set of installed packages for a project. Using a venv prevents conflicts between different projects that require conflicting versions of the same package.
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

-