import React, { useState, useRef, useEffect } from 'react'
import { askQuestion, getFileHistory } from '../services/api'
import MessageList from './MessageList'

function ChatSection({ currentFile, messages, onNewMessage }) {
  const [question, setQuestion] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [allMessages, setAllMessages] = useState([])
  const inputRef = useRef(null)

  useEffect(() => {
    if (currentFile && currentFile.id) {
      loadChatHistory(currentFile.id)
      if (inputRef.current) {
        inputRef.current.focus()
      }
    } else {
      setAllMessages(messages)
    }
  }, [currentFile, messages])

  const loadChatHistory = async (fileId) => {
    try {
      const history = await getFileHistory(fileId)
      const formattedMessages = history.map(item => ({
        type: 'history-pair',
        question: item.question,
        answer: item.answer
      }))
      setAllMessages(formattedMessages)
    } catch (error) {
      console.error('Error loading chat history:', error)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!question.trim() || isLoading || !currentFile) return

    const currentQuestion = question
    setQuestion('')
    
    // Show user's question immediately
    const userMessage = { type: 'user', content: currentQuestion }
    setAllMessages(prev => [...prev, userMessage])
    
    setIsLoading(true)

    try {
      const response = await askQuestion(currentQuestion, currentFile.id)
      
      // Display the bot's response immediately
      const botMessage = { type: 'bot', content: response.answer }
      setAllMessages(prev => [...prev, botMessage])
      
      // Database save happens automatically in the backend
    } catch (error) {
      const errorMessage = { 
        type: 'bot', 
        content: `Error: ${error.message}` 
      }
      setAllMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  return (
    <section className="chat-section">
      <MessageList 
        messages={allMessages} 
        currentFile={currentFile}
        isLoading={isLoading}
      />
      
      <div className="input-section">
        <input 
          ref={inputRef}
          type="text" 
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder={currentFile ? `Ask about ${currentFile.filename}...` : "Select a file to start chatting..."}
          disabled={!currentFile || isLoading}
        />
        <button 
          onClick={handleSubmit}
          disabled={!currentFile || isLoading || !question.trim()}
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <line x1="22" y1="2" x2="11" y2="13"></line>
            <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
          </svg>
        </button>
      </div>
    </section>
  )
}

export default ChatSection
