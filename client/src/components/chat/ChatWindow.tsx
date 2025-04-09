import { useState } from 'react';
import { MessageList } from './MessageList';
import { MessageInput } from './MessageInput';
import { Message, chatService } from '../../services';

interface ChatWindowProps {
  initialMessages?: Message[];
  useRag?: boolean;
}

export function ChatWindow({ 
  initialMessages = [], 
  useRag = true 
}: ChatWindowProps) {
  const [messages, setMessages] = useState<Message[]>(initialMessages);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSendMessage = async (content: string) => {
    // Add user message to the conversation
    const userMessage: Message = { role: 'user', content };
    const updatedMessages = [...messages, userMessage];
    setMessages(updatedMessages);
    setIsLoading(true);
    setError(null);
    
    try {
      // Call the AI service
      const response = await chatService.chat(updatedMessages, { 
        use_rag: useRag 
      });
      
      // Add AI response to conversation
      const assistantMessage: Message = { 
        role: 'assistant', 
        content: response.response 
      };
      
      setMessages([...updatedMessages, assistantMessage]);
    } catch (err) {
      console.error('Error getting chat response:', err);
      setError('Failed to get a response. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-window">
      <div className="chat-header">
        <h2>AI Assistant</h2>
        <div className="chat-options">
          <label>
            <input 
              type="checkbox" 
              checked={useRag} 
              onChange={(e) => console.log('RAG toggled:', e.target.checked)} 
            />
            Use Knowledge Base
          </label>
        </div>
      </div>
      
      <div className="chat-messages">
        <MessageList messages={messages} isLoading={isLoading} />
      </div>
      
      {error && (
        <div className="chat-error">
          {error}
        </div>
      )}
      
      <div className="chat-input">
        <MessageInput 
          onSendMessage={handleSendMessage} 
          isLoading={isLoading} 
        />
      </div>
    </div>
  );
}