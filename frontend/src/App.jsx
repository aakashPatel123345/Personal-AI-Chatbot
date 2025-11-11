import { useState, useRef, useEffect } from 'react'
import './App.css'

function App() {
  const [message, setMessage] = useState("")
  const [chatHistory, setChatHistory] = useState([])
  const textareaRef = useRef(null)

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`
    }
  }, [message])

  const handleSubmit = async (e) => {
    e.preventDefault()

    if (!message.trim()) { // Don't send empty messages
      return
    } 

    // Add user's message to chat history
    const userMessage = { role: "user", content: message }
    setChatHistory(prev => [...prev, userMessage])

    // Clear input
    const currentMessage = message
    setMessage("")

    try {
      // POST message to backend
      const res = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: currentMessage }),
      })

      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`)
      }

      const data = await res.json()

      // Add the AI response into the chat history
      const aiMessage = { role: "assistant", content: data.response }
      setChatHistory(prev => [...prev, aiMessage])
    } catch (error) {
      console.error("Error sending message:", error)
      // We can add the error to our chat history
      const errorMessage = { role: "assistant", content: "Sorry, I encountered an error. Please try again." }
      setChatHistory(prev => [...prev, errorMessage])
    }
  }

  return (
    <div className="main_container">
      <div className="messages_container">
        {chatHistory.map((msg, index) => (
          <div key={index} className={`message ${msg.role}`}>
            <div className="message_content">
              <div className="message_avatar">
                {msg.role === 'user' ? 'U' : 'A'}
              </div>
              <div className="message_text">
                <p>{msg.content}</p>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Input Form */}
      <form onSubmit={handleSubmit} className="input_form">
        <div className="input_wrapper">
          <textarea
            ref={textareaRef}
            className='input_chat'
            placeholder='Message...'
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSubmit(e);
              }
            }}
            rows={1}
          />
          <button type="submit" className="submit_button" disabled={!message.trim()}>
            Send
          </button>
        </div>
      </form>
    </div>
  )
}

export default App
