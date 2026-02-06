'use client';

import React from 'react';
import ClientProviders from '@/src/components/providers/ClientProviders';

interface RootWrapperProps {
  children: React.ReactNode;
}

const RootWrapper: React.FC<RootWrapperProps> = ({ children }) => {
  return <ClientProviders>{children}</ClientProviders>;
};

export default RootWrapper;
