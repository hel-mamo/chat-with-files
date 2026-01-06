# Chat with Files - Supabase Integration

The app now supports Supabase to manage files and chat history!

## 🎯 Features Added

- **Multiple File Management**: Upload and switch between different files
- **File History**: Each file maintains its own chat conversation
- **File List Sidebar**: See all your uploaded files at a glance
- **Delete Files**: Remove files and their chat history
- **Persistent Storage**: All data saved in Supabase database

## 🚀 Setup Instructions

### 1. Create a Supabase Project

1. Go to [https://supabase.com](https://supabase.com) and sign up/login
2. Create a new project
3. Wait for the project to be ready

### 2. Set Up Database Tables

1. In your Supabase project, go to the SQL Editor
2. Run the SQL script from `supabase_schema.sql`:
   ```sql
   -- Copy and paste the contents of supabase_schema.sql
   ```

### 3. Get Your Supabase Credentials

1. Go to Project Settings → API
2. Copy your Project URL
3. Copy your `anon/public` API key

### 4. Update Environment Variables

1. Copy `.env.example` to `.env`:
   ```powershell
   cp .env.example .env
   ```

2. Update `.env` with your credentials:
   ```
   OPENAI_API_KEY=your_openrouter_api_key
   OPENAI_BASE_URL=https://openrouter.ai/api/v1
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your_supabase_anon_key
   ```

### 5. Install Dependencies

```powershell
# Backend
pip install supabase

# Frontend (already installed)
cd react-frontend
npm install
```

### 6. Run the Application

**Backend:**
```powershell
cd backend
uvicorn main:app --reload --port 8000
```

**Frontend:**
```powershell
cd react-frontend
npm run dev
```

## 📖 How It Works

1. **Upload Files**: Click upload or drag & drop your documents
2. **Select File**: Click on any file in the sidebar to chat with it
3. **Ask Questions**: Questions are answered using only the selected file's content
4. **Switch Files**: Click different files to switch contexts
5. **Delete Files**: Click the 🗑️ button to remove files

## 🗄️ Database Schema

### Files Table
- `id`: UUID (Primary Key)
- `filename`: Text
- `chunk_count`: Integer
- `uploaded_at`: Timestamp

### Chat History Table
- `id`: UUID (Primary Key)
- `file_id`: UUID (Foreign Key to files)
- `question`: Text
- `answer`: Text
- `sources`: JSONB
- `created_at`: Timestamp

## 🔧 API Endpoints

- `POST /upload` - Upload and index a file
- `POST /ask` - Ask a question about a specific file
- `GET /files` - Get all uploaded files
- `GET /files/{file_id}/history` - Get chat history for a file
- `DELETE /files/{file_id}` - Delete a file and its history

## 💡 Tips

- The app works even without Supabase (it will generate file IDs locally)
- Supabase enables persistence across sessions
- You can view all your data in the Supabase dashboard
- Chat history is automatically saved for each file
