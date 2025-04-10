import { useState, useEffect } from 'react';
import { MessageList } from './MessageList';
import { MessageInput } from './MessageInput';
import { Message, chatService, documentService } from '../../services';

interface ChatWindowProps {
  initialMessages?: Message[];
}

export function ChatWindow({ 
  initialMessages = []
}: ChatWindowProps) {
  const [messages, setMessages] = useState<Message[]>(initialMessages);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [collections, setCollections] = useState<string[]>([]);

  // Fetch available collections on component mount
  useEffect(() => {
    const fetchCollections = async () => {
      try {
        const collectionsData = await documentService.getCollections();
        // Sort collections alphabetically
        setCollections(collectionsData.sort());
      } catch (err) {
        console.error('Failed to fetch collections:', err);
        setError('Failed to load document collections');
      }
    };
    
    fetchCollections();
  }, []);

  const handleSendMessage = async (
    content: string, 
    options: { skipMemory: boolean, ragCollection: string | null }
  ) => {
    // Add user message to the conversation UI
    const userMessage: Message = { role: 'user', content };
    const updatedMessages = [...messages, userMessage];
    setMessages(updatedMessages);
    setIsLoading(true);
    setError(null);
    
    try {
      // When skipMemory is true, only send the current message
      // When false, send the entire conversation history
      const messagesToSend = options.skipMemory 
        ? [userMessage]  // Just send the current message for stateless requests
        : updatedMessages; // Send full history for normal requests
      
      // Call the AI service with the appropriate messages
      const response = await chatService.chat(messagesToSend, { 
        skip_memory: options.skipMemory,
        use_rag: !!options.ragCollection,
        rag_collection: options.ragCollection || undefined
      });
      
      // Add AI response to conversation UI (always maintain visual history)
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
          collections={collections}
        />
      </div>
    </div>
  );
}