import React, { useEffect, useRef } from 'react'

function MessageList({ messages, currentFile, isLoading }) {
  const containerRef = useRef(null)

  useEffect(() => {
    if (containerRef.current) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight
    }
  }, [messages, isLoading])

  const formatText = (text) => {
    if (!text) return ''
    
    // Convert **bold** to <strong>
    let formatted = text.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    
    // Split into blocks (paragraphs, lists, etc.)
    const lines = formatted.split('\n')
    const blocks = []
    let currentList = null
    
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i].trim()
      
      if (!line) {
        // Empty line - close any open list
        if (currentList) {
          blocks.push(currentList)
          currentList = null
        }
        continue
      }
      
      // Check for numbered list (1. 2. 3. etc.)
      const numberedMatch = line.match(/^(\d+)\.\s+(.+)$/)
      if (numberedMatch) {
        if (!currentList || currentList.type !== 'ol') {
          if (currentList) blocks.push(currentList)
          currentList = { type: 'ol', items: [] }
        }
        currentList.items.push(numberedMatch[2])
        continue
      }
      
      // Check for bullet list (- * •)
      const bulletMatch = line.match(/^[-*•]\s+(.+)$/)
      if (bulletMatch) {
        if (!currentList || currentList.type !== 'ul') {
          if (currentList) blocks.push(currentList)
          currentList = { type: 'ul', items: [] }
        }
        currentList.items.push(bulletMatch[1])
        continue
      }
      
      // Regular paragraph
      if (currentList) {
        blocks.push(currentList)
        currentList = null
      }
      blocks.push({ type: 'p', content: line })
    }
    
    // Don't forget the last list if there is one
    if (currentList) {
      blocks.push(currentList)
    }
    
    // Convert blocks to HTML
    return blocks.map(block => {
      if (block.type === 'ol') {
        return `<ol>${block.items.map(item => `<li>${item}</li>`).join('')}</ol>`
      } else if (block.type === 'ul') {
        return `<ul>${block.items.map(item => `<li>${item}</li>`).join('')}</ul>`
      } else if (block.type === 'p') {
        return `<p>${block.content}</p>`
      }
      return ''
    }).join('')
  }

  if (!currentFile && messages.length === 0) {
    return (
      <div ref={containerRef} className="chat-container">
        <div className="welcome-message">
          <h2>👋 Welcome!</h2>
          <p>Upload a document to get started. Once uploaded, you can ask any questions about its content.</p>
        </div>
      </div>
    )
  }

  return (
    <div ref={containerRef} className="chat-container">
      {messages.map((msg, index) => {
        if (msg.type === 'history-pair') {
          return (
            <div key={index}>
              <div className="message user">
                <div className="message-content">
                  <p>{msg.question}</p>
                </div>
              </div>
              <div className="message bot">
                <div className="message-content">
                  {<div dangerouslySetInnerHTML={{ __html: formatText(msg.answer) }} />}
                </div>
              </div>
            </div>
          )
        }
        return (
          <div key={index} className={`message ${msg.type}`}>
            <div className="message-content">
              {msg.type === 'bot' ? (
                <div dangerouslySetInnerHTML={{ __html: formatText(msg.content) }} />
              ) : (
                <p>{msg.content}</p>
              )}
            </div>
          </div>
        )
      })}
      {isLoading && (
        <div className="message bot">
          <div className="message-content loading">
            <div className="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default MessageList
