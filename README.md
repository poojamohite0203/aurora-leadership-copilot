# Aurora – AI Leadership Copilot  

### Project Structure 
- src/core/ – Handles LLM calls, prompt templates, text/audio processing.
- src/data_pipeline/ – Connects APIs, manages DB, embeddings.
- src/features/ – Implements your main EM-focused functionality.
- src/dashboard/ – Streamlit UI modularized per feature.
- data/ – Keep all raw or temporary data separate from code.
- tests/ – Write simple unit tests.
- docs/ – Architecture diagrams.

*Week 1 Deliverable: Core Extraction Pipeline*  

## 📌 Overview
Aurora is an AI-powered leadership copilot that helps Engineering Managers save time and communicate effectively.  
In Week 1, we build the **core extraction pipeline**: taking raw meeting text (transcripts or notes) and converting it into structured outputs:  
- ✅ **Decisions**  
- ✅ **Action Items**  
- ✅ **Blockers**  

This will form the foundation for later features like weekly reports, dashboards, and automated follow-ups.  

---

## ⚙️ Setup Instructions
```bash
### 1. Clone Repository
git clone https://github.com/<your-username>/aurora-leadership-copilot.git
cd aurora-leadership-copilot

### 2. Create Virtual Environment
python -m venv .venv
source .venv/bin/activate   # Mac/Linux
.venv\Scripts\activate      # Windows

### 3. Install Dependencies
pip install -r requirements.txt

### 4. Ensure Ollama is Running
Install Ollama: https://ollama.ai

Start Ollama in background.

Test a model:
ollama run llama3.1 "Hello"

### Run Tests
python -m pytest
OR
python3 -m pytest --capture=no # to display print on terminal from test cases






