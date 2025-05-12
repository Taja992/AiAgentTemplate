import React, { useState } from 'react';

interface MessageInputProps {
  onSendMessage: (message: string, options: {
    skipMemory: boolean,
    ragCollection: string | null
  }) => void;
  isLoading?: boolean;
  placeholder?: string;
  collections?: string[];
}

export function MessageInput({ 
  onSendMessage, 
  isLoading = false, 
  placeholder = 'Type your message...',
  collections = []
}: MessageInputProps) {
  const [message, setMessage] = useState('');
  const [skipMemory, setSkipMemory] = useState(false);
  const [selectedCollection, setSelectedCollection] = useState<string | null>(null);
  
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim() && !isLoading) {
      onSendMessage(message.trim(), {
        skipMemory,
        ragCollection: selectedCollection
      });
      setMessage('');
    }
  };
  
  return (
    <div className="message-input-wrapper">
      <div className="message-options">
        <div className="collection-selector">
          <label htmlFor="collection-select">Document collection:</label>
          <select 
            id="collection-select" 
            value={selectedCollection || "None"}
            onChange={(e) => setSelectedCollection(e.target.value === "None" ? null : e.target.value)}
            disabled={isLoading}
          >
            <option value="None">None</option>
            {collections.map(collection => (
              <option key={collection} value={collection}>{collection}</option>
            ))}
          </select>
        </div>
        
        <div className="memory-toggle">
          <input
            type="checkbox"
            id="skip-memory"
            checked={skipMemory}
            onChange={(e) => setSkipMemory(e.target.checked)}
            disabled={isLoading}
          />
          <label htmlFor="skip-memory">Skip memory</label>
        </div>
      </div>
      
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
    </div>
  );
}