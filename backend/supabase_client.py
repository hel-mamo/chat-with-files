from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY
from typing import Optional
import uuid
from datetime import datetime
import json
import os

# Local storage for chat history as fallback
HISTORY_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "chat_history.json")

def ensure_history_file():
    """Ensure the chat history file exists"""
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'w') as f:
            json.dump({}, f)

class SupabaseClient:
    def __init__(self):
        if SUPABASE_URL and SUPABASE_KEY:
            try:
                self.client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
                # Test connection
                self.client.table("files").select("id", count="exact").limit(1).execute()
                self.enabled = True
                self.use_supabase = True
                print("✅ Supabase connected successfully")
            except Exception as e:
                print(f"⚠️ Supabase connection failed: {e}. Using local storage.")
                self.client = None
                self.enabled = True
                self.use_supabase = False
        else:
            print("⚠️ Supabase credentials not found. Using local storage only.")
            self.client = None
            self.enabled = True
            self.use_supabase = False
        
        ensure_history_file()

    def create_file_record(self, file_id: str, filename: str, chunk_count: int) -> Optional[str]:
        """Create a new file record in Supabase"""
        if self.use_supabase:
            try:
                data = {
                    "id": file_id,
                    "filename": filename,
                    "chunk_count": chunk_count,
                    "uploaded_at": datetime.utcnow().isoformat()
                }
                self.client.table("files").insert(data).execute()
                print(f"✅ File record created in Supabase with ID: {file_id}")
                return file_id
            except Exception as e:
                print(f"❌ Error creating file record in Supabase: {e}")
        
        # Local storage fallback
        try:
            with open(HISTORY_FILE, 'r') as f:
                history = json.load(f)
        except:
            history = {}
        
        if "files" not in history:
            history["files"] = {}
        
        history["files"][file_id] = {
            "filename": filename,
            "chunk_count": chunk_count,
            "uploaded_at": datetime.utcnow().isoformat()
        }
        
        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=2)
        
        return file_id

    def get_all_files(self):
        """Get all uploaded files"""
        if self.use_supabase:
            try:
                response = self.client.table("files").select("*").order("uploaded_at", desc=True).execute()
                return response.data
            except Exception as e:
                print(f"Error fetching files from Supabase: {e}")
        
        # Local storage fallback
        try:
            with open(HISTORY_FILE, 'r') as f:
                history = json.load(f)
            files = []
            for file_id, file_data in history.get("files", {}).items():
                files.append({
                    "id": file_id,
                    **file_data
                })
            return sorted(files, key=lambda x: x.get("uploaded_at", ""), reverse=True)
        except:
            return []

    def get_file(self, file_id: str):
        """Get a specific file by ID"""
        if self.use_supabase:
            try:
                response = self.client.table("files").select("*").eq("id", file_id).execute()
                return response.data[0] if response.data else None
            except Exception as e:
                print(f"Error fetching file from Supabase: {e}")
        
        # Local storage fallback
        try:
            with open(HISTORY_FILE, 'r') as f:
                history = json.load(f)
            file_data = history.get("files", {}).get(file_id)
            if file_data:
                return {"id": file_id, **file_data}
            return None
        except:
            return None

    def save_chat_message(self, file_id: str, question: str, answer: str, sources: list):
        """Save a chat message to history"""
        if self.use_supabase:
            try:
                data = {
                    "file_id": file_id,
                    "question": question,
                    "answer": answer,
                    "sources": sources,
                    "created_at": datetime.utcnow().isoformat()
                }
                result = self.client.table("chat_history").insert(data).execute()
                print(f"✅ Chat message saved to Supabase for file {file_id}")
                return
            except Exception as e:
                print(f"❌ Error saving chat message to Supabase: {e}")
                print(f"Falling back to local storage")
        
        # Local storage fallback
        try:
            with open(HISTORY_FILE, 'r') as f:
                history = json.load(f)
        except:
            history = {}
        
        if "chat_history" not in history:
            history["chat_history"] = {}
        if file_id not in history["chat_history"]:
            history["chat_history"][file_id] = []
        
        message = {
            "id": str(uuid.uuid4()),
            "question": question,
            "answer": answer,
            "sources": sources,
            "created_at": datetime.utcnow().isoformat()
        }
        
        history["chat_history"][file_id].append(message)
        
        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=2)
        
        print(f"✅ Chat message saved to local storage for file {file_id}")

    def get_chat_history(self, file_id: str):
        """Get chat history for a specific file"""
        if not file_id or file_id == "undefined":
            return []
        
        if self.use_supabase:
            try:
                response = self.client.table("chat_history").select("*").eq("file_id", file_id).order("created_at").execute()
                return response.data
            except Exception as e:
                print(f"Error fetching chat history from Supabase: {e}")
        
        # Local storage fallback
        try:
            with open(HISTORY_FILE, 'r') as f:
                history = json.load(f)
            return history.get("chat_history", {}).get(file_id, [])
        except:
            return []

    def delete_file(self, file_id: str):
        """Delete a file and its chat history"""
        if self.use_supabase:
            try:
                # Delete chat history first
                self.client.table("chat_history").delete().eq("file_id", file_id).execute()
                # Delete file record
                self.client.table("files").delete().eq("id", file_id).execute()
                return
            except Exception as e:
                print(f"Error deleting file from Supabase: {e}")
        
        # Local storage fallback
        try:
            with open(HISTORY_FILE, 'r') as f:
                history = json.load(f)
            
            # Remove file record
            if "files" in history and file_id in history["files"]:
                del history["files"][file_id]
            
            # Remove chat history
            if "chat_history" in history and file_id in history["chat_history"]:
                del history["chat_history"][file_id]
            
            with open(HISTORY_FILE, 'w') as f:
                json.dump(history, f, indent=2)
        except Exception as e:
            print(f"Error deleting file locally: {e}")


# Singleton instance
supabase_client = SupabaseClient()
