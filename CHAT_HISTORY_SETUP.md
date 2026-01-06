# Chat History Storage - Setup Guide

Your app now has **automatic chat history storage** with local backup!

## 🎯 How It Works

- **Primary**: Stores to Supabase (if configured)
- **Fallback**: Stores locally to `data/chat_history.json`
- **Automatic**: Chat messages saved after every question

## 📊 Storage Locations

### Supabase (Production)
- Best for: Multi-device access, cloud backup
- File: Supabase PostgreSQL database
- History loaded automatically when you switch files

### Local JSON (Always Available)
- File: `data/chat_history.json`
- Format: JSON with nested structure
- Works offline, persists between sessions

## 🚀 Setup Supabase Properly

### Step 1: Fix Your API Key

The publishable key you have only works for READ operations. For WRITE operations (saving chat), you need the **Service Role Key**:

1. Go to your Supabase project: https://supabase.com
2. Navigate to **Settings** → **API**
3. Copy the **Service Role Secret** (NOT the Anon Public key)
4. Update your `.env` file:

```env
OPENAI_API_KEY=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
OPENAI_BASE_URL=https://openrouter.ai/api/v1
SUPABASE_URL=https://arrhxbetsygtlisahgyy.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9... # Service Role key
```

### Step 2: Create Database Tables

1. Go to **SQL Editor** in your Supabase dashboard
2. Create a new query and paste this SQL:

```sql
-- Create files table
CREATE TABLE IF NOT EXISTS files (
    id TEXT PRIMARY KEY,
    filename TEXT NOT NULL,
    chunk_count INTEGER NOT NULL,
    uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create chat_history table
CREATE TABLE IF NOT EXISTS chat_history (
    id TEXT PRIMARY KEY,
    file_id TEXT NOT NULL REFERENCES files(id) ON DELETE CASCADE,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    sources JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_chat_history_file_id ON chat_history(file_id);
CREATE INDEX IF NOT EXISTS idx_chat_history_created_at ON chat_history(created_at);
CREATE INDEX IF NOT EXISTS idx_files_uploaded_at ON files(uploaded_at);
```

3. Click **Run** to execute

### Step 3: Restart Your Backend

```powershell
# Stop the current server (Ctrl+C)
# Then restart:
cd C:\Users\Houssam\Desktop\chat-with-file\backend
uvicorn main:app --reload --port 8000
```

## ✅ Verify It's Working

1. **Upload a file**
2. **Ask a question**
3. **Check the response** - you should see the history in:
   - **Supabase**: Go to SQL Editor → SELECT * FROM chat_history
   - **Local**: Check `data/chat_history.json`

## 🔍 Troubleshooting

### Chat history still not saving?

**Option 1: Check Supabase Connection**
```bash
# The backend will print one of these on startup:
# ✅ Supabase connected successfully
# ⚠️ Supabase connection failed: ...
# ⚠️ Supabase credentials not found
```

**Option 2: Verify API Key**
- Make sure you're using the **Service Role** key (starts with `eyJhbGci...`)
- NOT the publishable key

**Option 3: Check Local File**
```bash
# View local chat history:
cat data/chat_history.json
```

### Still having issues?

1. The app ALWAYS has local storage as backup
2. Your chat history is never lost
3. Check browser console for errors: F12 → Console
4. Check backend logs for Supabase errors

## 📈 View Your Data

### In Supabase Dashboard
- **Files**: https://your-project.supabase.co → Table Editor → files
- **Chat History**: https://your-project.supabase.co → Table Editor → chat_history

### Locally
- Check: `data/chat_history.json` in your project folder

## 🎯 Next Steps

1. Update `.env` with Service Role key ✓
2. Create tables in Supabase ✓
3. Restart backend ✓
4. Upload file and test ✓

After these steps, your chat history will be automatically saved and loaded!
