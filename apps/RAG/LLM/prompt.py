# RAG/llm/prompt.py

RAG_PROMPT_TEMPLATE = """
You are an expert assistant analyzing document context. 
Answer the user's question accurately using ONLY the provided context retrieved from the uploaded document.
If the answer cannot be found in the context, explicitly state: "I cannot find the answer to this question in the uploaded document."

CONTEXT FROM PDF:
-----------------
{context}
-----------------

USER QUESTION:
{question}

ANSWER:
"""

def build_rag_prompt(context: str, question: str) -> str:
    """Combines context chunks and question into a final prompt."""
    return RAG_PROMPT_TEMPLATE.format(context=context, question=question)

