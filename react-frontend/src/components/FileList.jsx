import React from 'react'
import { deleteFile, downloadFile } from '../services/api'

function FileList({ files, currentFile, onFileSelect, onFileDeleted }) {
  const handleDelete = async (e, fileId, filename) => {
    e.stopPropagation()
    
    const confirmMessage = `Delete "${filename}"?\n\nThis will:\n✓ Remove the file from your list\n✓ Delete all chat history for this file\n\nThis action cannot be undone.`
    
    if (window.confirm(confirmMessage)) {
      try {
        await deleteFile(fileId)
        onFileDeleted(fileId)
      } catch (error) {
        console.error('Error deleting file:', error)
        alert('Failed to delete file. Please try again.')
      }
    }
  }

  const handleDownload = async (e, file) => {
    e.stopPropagation()
    try {
      const blob = await downloadFile(file.id)
      const url = window.URL.createObjectURL(new Blob([blob]))
      const link = document.createElement('a')
      link.href = url
      link.download = file.filename
      document.body.appendChild(link)
      link.click()
      link.remove()
      window.URL.revokeObjectURL(url)
    } catch (error) {
      console.error('Error downloading file:', error)
      alert('Failed to download file. Please try again.')
    }
  }

  const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  }

  if (files.length === 0) {
    return (
      <div className="file-list">
        <h3>📁 Files</h3>
        <p className="no-files">No files uploaded yet</p>
      </div>
    )
  }

  return (
    <div className="file-list">
      <h3>📁 My Files</h3>
      <div className="files">
        {files.map((file) => (
          <div
            key={file.id}
            className={`file-item ${currentFile?.id === file.id ? 'active' : ''}`}
            onClick={() => onFileSelect(file)}
          >
            <div className="file-info">
              <div className="file-name">{file.filename}</div>
              <div className="file-date">{formatDate(file.uploaded_at)}</div>
            </div>
            <button
              className="delete-btn"
              onClick={(e) => handleDownload(e, file)}
              title="Download file"
            >
              ⬇️
            </button>
            <button
              className="delete-btn"
              onClick={(e) => handleDelete(e, file.id, file.filename)}
              title="Delete file and chat history"
            >
              🗑️
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}

export default FileList
