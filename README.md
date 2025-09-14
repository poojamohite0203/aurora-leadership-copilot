# aurora-leadership-copilot

### Project Structure 
- src/core/ – Handles LLM calls, prompt templates, text/audio processing.
- src/data_pipeline/ – Connects APIs, manages DB, embeddings.
- src/features/ – Implements your main EM-focused functionality.
- src/dashboard/ – Streamlit UI modularized per feature.
- data/ – Keep all raw or temporary data separate from code.
- tests/ – Write simple unit tests.
- docs/ – Architecture diagrams.

### Commands to run the project - specifically for macOS
- source .venv/bin/activate
- pip install typer pydantic requests
- 