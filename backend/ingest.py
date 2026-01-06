import os
import uuid
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from config import (
    VECTOR_DB_PATH,
    OPENAI_API_KEY,
    OPENAI_BASE_URL,
    OPENAI_EMBEDDING_MODEL,
    CHUNK_SIZE,
    CHUNK_OVERLAP
)
from supabase_client import supabase_client

def load_file(path):
    ext = path.split(".")[-1].lower()

    if ext == "pdf":
        return PyPDFLoader(path).load()
    else:
        raise ValueError("Unsupported file type. Only PDF is supported.")

def ingest_file(path):
    docs = load_file(path)

    if not docs:
        raise ValueError("No content could be extracted from the file")

    # Generate file ID
    file_id = str(uuid.uuid4())
    filename = os.path.basename(path)

    for d in docs:
        d.metadata["source"] = filename
        d.metadata["file_id"] = file_id

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    chunks = splitter.split_documents(docs)

    if not chunks:
        raise ValueError("No text chunks generated from the document")

    embeddings = OpenAIEmbeddings(
        model=OPENAI_EMBEDDING_MODEL,
        openai_api_key=OPENAI_API_KEY,
        base_url=OPENAI_BASE_URL
    )

    # Load existing index or create new one
    index_exists = os.path.exists(os.path.join(VECTOR_DB_PATH, "index.faiss"))
    
    if index_exists:
        try:
            db = FAISS.load_local(
                VECTOR_DB_PATH,
                embeddings,
                allow_dangerous_deserialization=True
            )
            # Add documents one at a time to handle potential errors
            if len(chunks) > 0:
                db.add_documents(chunks)
        except Exception as e:
            print(f"Error loading existing index, creating new one: {e}")
            db = FAISS.from_documents(chunks, embeddings)
    else:
        db = FAISS.from_documents(chunks, embeddings)

    db.save_local(VECTOR_DB_PATH)
    
    # Save file record to Supabase with the same file_id
    supabase_client.create_file_record(file_id, filename, len(chunks))
    
    return {"file_id": file_id, "filename": filename, "chunk_count": len(chunks)}
