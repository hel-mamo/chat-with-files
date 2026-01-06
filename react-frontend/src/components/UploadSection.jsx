import React, { useState, useRef } from 'react'
import { uploadFile } from '../services/api'

function UploadSection({ onFileUploaded }) {
  const [uploadStatus, setUploadStatus] = useState({ message: '', type: '' })
  const [isDragging, setIsDragging] = useState(false)
  const fileInputRef = useRef(null)

  const handleFileUpload = async (file) => {
    if (!file) return

    setUploadStatus({ message: '⏳ Uploading and indexing...', type: 'loading' })

    try {
      const fileData = await uploadFile(file)
      setUploadStatus({ 
        message: `✅ ${file.name} uploaded successfully!`, 
        type: 'success' 
      })
      onFileUploaded(fileData)
      
      // Clear file input
      if (fileInputRef.current) {
        fileInputRef.current.value = ''
      }
    } catch (error) {
      setUploadStatus({ 
        message: `❌ Upload failed: ${error.message}`, 
        type: 'error' 
      })
    }
  }

  const handleFileChange = (e) => {
    const file = e.target.files[0]
    handleFileUpload(file)
  }

  const handleDragOver = (e) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = () => {
    setIsDragging(false)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setIsDragging(false)
    const file = e.dataTransfer.files[0]
    handleFileUpload(file)
  }

  return (
    <section className="upload-section">
      <div 
        className={`upload-box ${isDragging ? 'dragging' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <input 
          type="file" 
          id="fileInput" 
          ref={fileInputRef}
          accept=".pdf" 
          hidden
          onChange={handleFileChange}
        />
        <label htmlFor="fileInput" className="upload-label">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
            <polyline points="17 8 12 3 7 8"></polyline>
            <line x1="12" y1="3" x2="12" y2="15"></line>
          </svg>
          <span>Click to upload or drag & drop</span>
          <small>PDF only</small>
        </label>
      </div>
      {uploadStatus.message && (
        <div className={`upload-status ${uploadStatus.type}`}>
          {uploadStatus.message}
        </div>
      )}
    </section>
  )
}

export default UploadSection
