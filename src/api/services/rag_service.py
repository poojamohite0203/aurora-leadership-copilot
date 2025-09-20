# src/services/rag_service.py
from db.vector_store import search
from core.llm_utils import query_ollama
from db.vector_store import search


# Enhance Propt - send it similary score - based on question and context answer this question - consider similarity score
RAG_PROMPT = """
You are an AI assistant. Use the context below to answer the question.
If the answer is not in the context, say you don’t know.

Context:
{context}

Question:
{question}

Answer:
"""

def ask_question(question: str, k: int = 5):
    # 1. Search vector DB
    results = search(question, k)

    # 2. Build context from top matches
    docs = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    context_chunks = []
    for doc, meta in zip(docs, metadatas):
        context_chunks.append(f"[{meta['type'].upper()}] {doc}")

    context = "\n".join(context_chunks)

    # 3. Send prompt to Ollama
    prompt = RAG_PROMPT.format(context=context, question=question)
    response = query_ollama(prompt)

    return {
        "question": question,
        "context_used": context_chunks,
        "answer": response.strip()
    }