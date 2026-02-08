import { useContext } from 'react';
import { ChatContext } from '../contexts/ChatContext';

// Create the hook that uses the context
export const useChat = () => {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error('useChat must be used within a ChatProvider');
  }
  return context;
};

export { ChatContext };