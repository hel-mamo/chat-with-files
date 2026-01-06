# React Frontend for Chat with Files

This is the React frontend for the Chat with Files application.

## Setup

1. **Install dependencies:**
```powershell
cd react-frontend
npm install
```

2. **Run the development server:**
```powershell
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Backend

Make sure the Python FastAPI backend is running on port 8000:

```powershell
cd ..
uvicorn backend.main:app --reload --port 8000
```

## Features

- Modern React components with hooks
- File upload with drag & drop support
- Real-time chat interface
- Responsive design
- Axios for API communication
- Vite for fast development and building

## Project Structure

```
react-frontend/
├── src/
│   ├── components/
│   │   ├── Header.jsx
│   │   ├── UploadSection.jsx
│   │   ├── ChatSection.jsx
│   │   └── MessageList.jsx
│   ├── services/
│   │   └── api.js
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
├── index.html
├── package.json
└── vite.config.js
```

## Building for Production

```powershell
npm run build
```

The build output will be in the `dist/` folder.
