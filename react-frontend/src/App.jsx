import React, { useState, useEffect } from 'react'
import Header from './components/Header'
import UploadSection from './components/UploadSection'
import ChatSection from './components/ChatSection'
import FileList from './components/FileList'
import { getFiles } from './services/api'

function App() {
  const [files, setFiles] = useState([])
  const [currentFile, setCurrentFile] = useState(null)
  const [messages, setMessages] = useState([])

  useEffect(() => {
    loadFiles()
  }, [])

  const loadFiles = async () => {
    try {
      const fileList = await getFiles()
      setFiles(fileList)
    } catch (error) {
      console.error('Error loading files:', error)
    }
  }

  const handleFileUploaded = (fileData) => {
    const newFile = {
      id: fileData.file_id,
      filename: fileData.filename,
      uploaded_at: fileData.uploaded_at
    }
    setFiles(prev => [newFile, ...prev])
    setCurrentFile(newFile)
    setMessages([{
      type: 'system',
      content: `✅ ${fileData.filename} uploaded successfully! You can now ask questions.`
    }])
  }

  const handleFileSelect = (file) => {
    setCurrentFile(file)
    setMessages([])
  }

  const handleNewMessage = (message) => {
    setMessages(prev => [...prev, message])
  }

  const handleFileDeleted = (fileId) => {
    setFiles(prev => prev.filter(f => f.id !== fileId))
    if (currentFile?.id === fileId) {
      setCurrentFile(null)
      setMessages([])
    }
  }

  return (
    <div className="container">
      <Header />
      <div className="main-content">
        <div className="sidebar">
          <UploadSection onFileUploaded={handleFileUploaded} />
          <FileList 
            files={files}
            currentFile={currentFile}
            onFileSelect={handleFileSelect}
            onFileDeleted={handleFileDeleted}
          />
        </div>
        <ChatSection 
          currentFile={currentFile}
          messages={messages}
          onNewMessage={handleNewMessage}
        />
      </div>
    </div>
  )
}

export default App
