'use client';

import React from 'react';
import { AuthProvider } from '@/src/components/auth/AuthProvider';
import { ToastProvider } from '@/src/components/ui/ToastContext';
import { ChatProvider } from '@/src/contexts/ChatContext';
import { useAuth } from '@/src/contexts/AuthContext';

interface ClientProvidersProps {
  children: React.ReactNode;
}

const ChatProviderWrapper: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user, isAuthenticated } = useAuth();
  return <ChatProvider user={user} isAuthenticated={isAuthenticated}>{children}</ChatProvider>;
};

const ClientProviders: React.FC<ClientProvidersProps> = ({ children }) => {
  return (
    <AuthProvider>
      <ToastProvider>
        <ChatProviderWrapper>
          {children}
        </ChatProviderWrapper>
      </ToastProvider>
    </AuthProvider>
  );
};

export default ClientProviders;
