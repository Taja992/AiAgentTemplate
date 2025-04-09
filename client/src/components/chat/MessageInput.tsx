import React, { useState } from 'react';

interface MessageInputProps {
  onSendMessage: (message: string) => void;
  isLoading?: boolean;
  placeholder?: string;
}

export function MessageInput({ 
  onSendMessage, 
  isLoading = false, 
  placeholder = 'Type your message...'
}: MessageInputProps) {
  const [message, setMessage] = useState('');
  
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim() && !isLoading) {
      onSendMessage(message.trim());
      setMessage('');
    }
  };
  
  return (
    <form className="message-input-container" onSubmit={handleSubmit}>
      <input
        type="text"
        className="message-input"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder={placeholder}
        disabled={isLoading}
      />
      <button 
        type="submit" 
        className="send-button"
        disabled={isLoading || !message.trim()}
      >
        {isLoading ? '...' : 'Send'}
      </button>
    </form>
  );
}