import React, { useState, useEffect, useRef, useCallback } from 'react';
import { useAuth } from '@/src/contexts/AuthContext';
import { useChat } from '../hooks/useChat';
import { ChatMessage, SendMessage } from '@/types';

interface ChatProps {
  conversationId?: number;
}

interface ConversationState {
  id?: number;
  title?: string;
  messages: ChatMessage[];
  isLoading: boolean;
  error?: string;
}

const Chat: React.FC<ChatProps> = ({ conversationId }) => {
  const { user } = useAuth();
  const userId = user?.id;

  // Show a message if user is not authenticated
  if (!user) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <p className="text-gray-600">Please log in to access the AI assistant</p>
        </div>
      </div>
    );
  }

  // Ensure userId is available
  const userId = user?.id;
  if (!userId) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <p className="text-gray-600">User information not available. Please try logging in again.</p>
        </div>
      </div>
    );
  }
  const [conversation, setConversation] = useState<ConversationState>({
    id: conversationId,
    messages: [],
    isLoading: true,
    error: undefined
  });
  const [inputMessage, setInputMessage] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { sendMessage, getMessages } = useChat();

  // Fetch conversation messages
  const fetchConversation = useCallback(async () => {
    if (!userId) {
      setConversation(prev => ({
        ...prev,
        isLoading: false,
        error: 'User not authenticated'
      }));
      return;
    }
    
    setConversation(prev => ({
      ...prev,
      isLoading: true,
      error: undefined
    }));

    try {
      const result = await getMessages(userId, conversationId);
      
      setConversation({
        id: result.conversation_id || conversationId,
        messages: result.messages || [],
        isLoading: false
      });
    } catch (error) {
      console.error('Error fetching conversation:', error);
      setConversation(prev => ({
        ...prev,
        isLoading: false,
        error: 'Failed to load conversation. Please try again.'
      }));
    }
  }, [userId, conversationId, getMessages]);

  // Initialize conversation when user is available
  useEffect(() => {
    if (userId) {
      fetchConversation();
    }
  }, [userId, fetchConversation]);

  // Scroll to bottom when messages change
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [conversation.messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputMessage.trim() || conversation.isLoading || !userId) return;

    // Add user message optimistically
    const userMessage: ChatMessage = {
      id: Date.now(), // Temporary ID
      role: 'user',
      content: inputMessage,
      created_at: new Date(),
    };

    setConversation(prev => ({
      ...prev,
      messages: [...prev.messages, userMessage],
      isLoading: true
    }));

    try {
      const result = await sendMessage(inputMessage, conversation.id);

      // Update with actual message IDs and add assistant response
      setConversation(prev => ({
        ...prev,
        id: result.conversation_id,
        messages: [
          ...prev.messages.filter(m => m.id !== userMessage.id), // Remove temp message
          {
            id: result.user_message_id,
            role: 'user',
            content: inputMessage,
            created_at: new Date(),
          },
          {
            id: result.assistant_message_id,
            role: 'assistant',
            content: result.assistant_response,
            created_at: new Date(),
          }
        ],
        isLoading: false
      }));

      setInputMessage('');
    } catch (error) {
      console.error('Error sending message:', error);
      setConversation(prev => ({
        ...prev,
        messages: prev.messages.filter(m => m.id !== userMessage.id), // Remove temp message
        isLoading: false,
        error: 'Failed to send message. Please try again.'
      }));
    }
  };

  if (conversation.isLoading && conversation.messages.length === 0) {
    return <div className="chat-container">Loading conversation...</div>;
  }

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h2>{conversation.title || 'Chat with your Todo Assistant'}</h2>
      </div>

      {conversation.error && (
        <div className="chat-error">
          {conversation.error}
        </div>
      )}

      <div className="chat-messages">
        {conversation.messages.map((message) => (
          <div
            key={message.id}
            className={`chat-message ${message.role === 'user' ? 'user-message' : 'assistant-message'}`}
          >
            <div className="message-content">
              {message.content}
            </div>
            <div className="message-timestamp">
              {new Date(message.created_at).toLocaleTimeString()}
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSubmit} className="chat-input-container">
        <input
          type="text"
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          placeholder="Type your message here..."
          className="chat-input"
          disabled={conversation.isLoading}
        />
        <button 
          type="submit" 
          className="chat-submit"
          disabled={conversation.isLoading || !inputMessage.trim()}
        >
          {conversation.isLoading ? 'Sending...' : 'Send'}
        </button>
      </form>
    </div>
  );
};

// Styles
const styles = {
  chatContainer: {
    display: 'flex',
    flexDirection: 'column',
    height: '100%',
    backgroundColor: '#f5f5f5',
    borderRadius: '8px',
    overflow: 'hidden',
  },
  chatHeader: {
    backgroundColor: '#6366f1',
    color: 'white',
    padding: '16px',
    borderBottom: '1px solid #e5e7eb',
  },
  chatMessages: {
    flex: 1,
    padding: '16px',
    overflowY: 'auto',
  },
  chatMessage: {
    marginBottom: '12px',
    '&:last-child': {
      marginBottom: 0,
    },
  },
  userMessage: {
    textAlign: 'right',
  },
  assistantMessage: {
    textAlign: 'left',
  },
  messageContent: {
    display: 'inline-block',
    padding: '12px 16px',
    borderRadius: '8px',
    maxWidth: '80%',
  },
  userMessageContent: {
    backgroundColor: '#3b82f6',
    color: 'white',
    textAlign: 'left',
  },
  assistantMessageContent: {
    backgroundColor: 'white',
    color: '#1f2937',
    border: '1px solid #e5e7eb',
  },
  messageTimestamp: {
    fontSize: '12px',
    color: '#6b7280',
    marginTop: '4px',
  },
  chatInputContainer: {
    display: 'flex',
    padding: '16px',
    borderTop: '1px solid #e5e7eb',
  },
  chatInput: {
    flex: 1,
    padding: '12px 16px',
    border: '1px solid #d1d5db',
    borderRadius: '8px 0 0 8px',
    fontSize: '16px',
    outline: 'none',
  },
  chatSubmit: {
    padding: '12px 24px',
    backgroundColor: '#6366f1',
    color: 'white',
    border: 'none',
    borderRadius: '0 8px 8px 0',
    cursor: 'pointer',
    fontSize: '16px',
    '&:hover': {
      backgroundColor: '#4f46e5',
    },
  },
};

export default Chat;

export { styles };