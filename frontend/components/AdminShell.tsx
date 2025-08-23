import React from 'react';
import { AuthProvider } from '../contexts/AuthContext';
import { AppLayout } from './AppLayout';
import { Dashboard } from './Dashboard';
import { Toaster } from './ui/sonner';

export const AdminDashboardShell: React.FC = () => {
  return (
    <AuthProvider>
      <AppLayout currentPage="dashboard" onNavigate={() => {}}>
        <Dashboard />
      </AppLayout>
      <Toaster />
    </AuthProvider>
  );
};


