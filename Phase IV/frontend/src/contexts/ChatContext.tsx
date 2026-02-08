import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import axios from 'axios';

interface ChatContextType {
  user: any;
  isAuthenticated: boolean;
  messages: any[];
  loading: boolean;
  error: string | null;
  sendMessage: (content: string, conversationId?: number) => Promise<any>;
  getMessages: (userId: number, conversationId?: number) => Promise<any>;
}

const ChatContext = createContext<ChatContextType | undefined>(undefined);

interface ChatProviderProps {
  children: ReactNode;
  user?: any;
  isAuthenticated?: boolean;
}

export const ChatProvider: React.FC<ChatProviderProps> = ({ children, user, isAuthenticated = false }) => {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (isAuthenticated && user) {
      // Initialize chat when user is authenticated
    }
  }, [isAuthenticated, user]);

  const sendMessage = async (content: string, conversationId?: number) => {
    // Check if user is authenticated
    const userId = user?.id;
    if (!userId) {
      const errorObj = {
        status: "failed",
        error: "Authentication required",
        recovery_suggestion: "Please log in to use the chat functionality"
      };
      setError(errorObj.recovery_suggestion);
      throw new Error(errorObj.recovery_suggestion);
    }

    setLoading(true);
    setError(null);

    try {
      const response = await axios.post(`/api/${userId}/chat`, {
        content,
        conversation_id: conversationId,
      }, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token') || ''}`,
        },
      });

      setMessages(prev => [...prev, ...response.data.conversation_history]);
      return response.data;
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Failed to send message';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const getMessages = async (userId: number, conversationId?: number) => {
    if (!userId) {
      const errorObj = {
        status: "failed",
        error: "User ID is required",
        recovery_suggestion: "Please log in to access your messages"
      };
      setError(errorObj.recovery_suggestion);
      throw new Error(errorObj.recovery_suggestion);
    }

    setLoading(true);
    setError(null);

    try {
      if (conversationId) {
        // Get specific conversation with messages
        const response = await axios.get(`/conversations/${conversationId}/with-messages`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token') || ''}`,
          },
        });

        setMessages(response.data.messages || []);
        return response.data;
      } else {
        // Get all conversations for the user (which includes messages)
        const response = await axios.get(`/conversations`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token') || ''}`,
          },
        });

        // Flatten all messages from all conversations
        const allMessages = [];
        for (const conv of response.data) {
          // Get messages for each conversation
          try {
            const convResponse = await axios.get(`/conversations/${conv.id}/with-messages`, {
              headers: {
                Authorization: `Bearer ${localStorage.getItem('token') || ''}`,
              },
            });
            allMessages.push(...(convResponse.data.messages || []));
          } catch (convErr) {
            console.error(`Error fetching messages for conversation ${conv.id}:`, convErr);
            // Continue with other conversations
          }
        }

        setMessages(allMessages);
        return { messages: allMessages, conversation_id: null };
      }
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Failed to fetch messages';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const value: ChatContextType = {
    user: user || null,
    isAuthenticated: isAuthenticated || false,
    messages,
    loading,
    error,
    sendMessage,
    getMessages,
  };

  return (
    <ChatContext.Provider value={value}>
      {children}
    </ChatContext.Provider>
  );
};

export const useChat = () => {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error('useChat must be used within a ChatProvider');
  }
  return context;
};