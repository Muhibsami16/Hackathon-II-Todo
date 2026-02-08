'use client';

import React from 'react';
import { AuthProvider } from '@/src/components/auth/AuthProvider';
import { ToastProvider } from '@/src/components/ui/ToastContext';

interface ClientProvidersProps {
  children: React.ReactNode;
}

const ClientProviders: React.FC<ClientProvidersProps> = ({ children }) => {
  return (
    <AuthProvider>
      <ToastProvider>
        {children}
      </ToastProvider>
    </AuthProvider>
  );
};

export default ClientProviders;
