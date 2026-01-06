from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from config import (
    VECTOR_DB_PATH,
    OPENAI_API_KEY,
    OPENAI_BASE_URL,
    OPENAI_MODEL,
    OPENAI_TEMPERATURE,
    OPENAI_EMBEDDING_MODEL,
    TOP_K
)
from supabase_client import supabase_client
from typing import Optional

def ask(question: str, file_id: Optional[str] = None):
    embeddings = OpenAIEmbeddings(
        model=OPENAI_EMBEDDING_MODEL,
        openai_api_key=OPENAI_API_KEY,
        base_url=OPENAI_BASE_URL
    )

    db = FAISS.load_local(
        VECTOR_DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    retriever = db.as_retriever(search_kwargs={"k": TOP_K})
    docs = retriever.invoke(question)
    
    # Filter documents by file_id if provided
    if file_id:
        docs = [doc for doc in docs if doc.metadata.get("file_id") == file_id]
    
    if not docs:
        return {
            "answer": "No relevant information found in the selected file.",
            "sources": []
        }

    context = "\n\n".join([doc.page_content for doc in docs])

    system_prompt = """You are a helpful assistant that answers questions based on the provided context. 
Use only the information from the context to answer the question. 
If the answer is not in the context, say "I don't have enough information to answer that question."
"""
    
    user_prompt = f"""Context:
{context}

Question: {question}

Answer:"""

    llm = ChatOpenAI(
        model=OPENAI_MODEL,
        temperature=OPENAI_TEMPERATURE,
        openai_api_key=OPENAI_API_KEY,
        base_url=OPENAI_BASE_URL
    )

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]
    
    response = llm.invoke(messages)
    
    sources = [doc.metadata for doc in docs]
    answer = response.content
    
    # Save to chat history if file_id is provided
    if file_id:
        supabase_client.save_chat_message(file_id, question, answer, sources)

    return {
        "answer": answer,
        "sources": sources
    }
