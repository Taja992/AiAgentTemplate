import { ChatWindow } from '../components/chat';
import '../components/chat/chat.css'; // Import the CSS

export function ChatPage() {
  return (
    <div className="chat-page">
      <h1>AI Agent Chat</h1>
      <p className="chat-description">
        Ask questions and get intelligent responses from our AI assistant.
      </p>
      <ChatWindow />
    </div>
  );
}