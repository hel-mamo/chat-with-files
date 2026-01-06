from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
from datetime import datetime
from ingest import ingest_file
from query import ask
from models import QuestionRequest, FileUploadResponse, FileInfo
from config import UPLOAD_DIR
from supabase_client import supabase_client

app = FastAPI(title="Chat with Files API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload", response_model=FileUploadResponse)
async def upload_file(file: UploadFile = File(...)):
    path = os.path.join(UPLOAD_DIR, file.filename)

    with open(path, "wb") as f:
        f.write(await file.read())

    result = ingest_file(path)

    return FileUploadResponse(
        status="uploaded and indexed",
        file_id=result["file_id"],
        filename=result["filename"],
        uploaded_at=datetime.utcnow().isoformat()
    )

@app.post("/ask")
async def ask_question(req: QuestionRequest):
    return ask(req.question, req.file_id)

@app.get("/files")
async def get_files():
    """Get all uploaded files"""
    files = supabase_client.get_all_files()
    return {"files": files}

@app.get("/files/{file_id}/history")
async def get_file_history(file_id: str):
    """Get chat history for a specific file"""
    if not file_id or file_id == "undefined":
        return {"history": []}
    history = supabase_client.get_chat_history(file_id)
    return {"history": history}

@app.get("/files/{file_id}/download")
async def download_file(file_id: str):
    """Download the original uploaded file"""
    if not file_id or file_id == "undefined":
        raise HTTPException(status_code=400, detail="Invalid file_id")

    file_record = supabase_client.get_file(file_id)
    if not file_record:
        raise HTTPException(status_code=404, detail="File not found")

    filename = file_record.get("filename")
    if not filename:
        raise HTTPException(status_code=404, detail="File name missing")

    path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found on server")

    return FileResponse(path, filename=filename, media_type="application/octet-stream")

@app.delete("/files/{file_id}")
async def delete_file(file_id: str):
    """Delete a file and its chat history"""
    supabase_client.delete_file(file_id)
    return {"status": "deleted"}
