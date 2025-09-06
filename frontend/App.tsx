import React, { useState } from 'react';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import { LoginPage } from './components/LoginPage';
import { AppLayout } from './components/AppLayout';
import { Dashboard } from './components/Dashboard';
import { CommandesIT } from './components/CommandesIT';
import { CommandesBureau } from './components/CommandesBureau';
import { MaterielsIT } from './components/MaterielsIT';
import { MaterielsBureau } from './components/MaterielsBureau';
import { Livraisons } from './components/Livraisons';
import { Demandes } from './components/Demandes';
import { Fournisseurs } from './components/Fournisseurs';
import { Utilisateurs } from './components/Utilisateurs';
import { Profile } from './components/Profile';
import { Toaster } from './components/ui/sonner';

const AppContent: React.FC = () => {
  const { isAuthenticated, user } = useAuth();
  const [currentPage, setCurrentPage] = useState('dashboard');
  const [isLoading, setIsLoading] = useState(true);

  // Vérifier les paramètres URL pour la redirection automatique
  React.useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const role = urlParams.get('role');
    const authenticated = urlParams.get('authenticated');
    
    if (authenticated === 'true' && role) {
      // L'utilisateur vient d'être authentifié, rediriger selon le rôle
      let defaultPage = 'dashboard';
      
      switch (role) {
        case 'superadmin':
          defaultPage = 'dashboard';
          break;
        case 'gestionnaire_info':
          defaultPage = 'commandes-it';
          break;
        case 'gestionnaire_bureau':
          defaultPage = 'commandes-bureau';
          break;
        case 'employe':
          defaultPage = 'demandes';
          break;
        default:
          defaultPage = 'dashboard';
      }
      
      setCurrentPage(defaultPage);
      setIsLoading(false);
      
      // Nettoyer l'URL
      window.history.replaceState({}, document.title, window.location.pathname);
    } else if (isAuthenticated && user) {
      // Rediriger selon le rôle de l'utilisateur connecté
      let defaultPage = 'dashboard';
      
      switch (user.role) {
        case 'superadmin':
          defaultPage = 'dashboard';
          break;
        case 'gestionnaire_informatique':
          defaultPage = 'commandes-it';
          break;
        case 'gestionnaire_bureau':
          defaultPage = 'commandes-bureau';
          break;
        case 'employe':
          defaultPage = 'demandes';
          break;
        default:
          defaultPage = 'dashboard';
      }
      
      setCurrentPage(defaultPage);
      setIsLoading(false);
    } else {
      setIsLoading(false);
    }
  }, [isAuthenticated, user]);

  // Afficher un loader pendant la vérification
  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Chargement...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <LoginPage onLogin={() => setCurrentPage('dashboard')} />;
  }

  const renderCurrentPage = () => {
    switch (currentPage) {
      case 'dashboard':
        return <Dashboard />;
      case 'commandes-it':
        return <CommandesIT />;
      case 'commandes-bureau':
        return <CommandesBureau />;
      case 'materiels-it':
        return <MaterielsIT />;
      case 'materiels-bureau':
        return <MaterielsBureau />;
      case 'livraisons':
        return <Livraisons />;
      case 'demandes':
        return <Demandes />;
      case 'fournisseurs':
        return <Fournisseurs />;
      case 'utilisateurs':
        return <Utilisateurs />;
      case 'profile':
        return <Profile />;
      default:
        return <Dashboard />;
    }
  };

  return (
    <AppLayout currentPage={currentPage} onNavigate={setCurrentPage}>
      {renderCurrentPage()}
    </AppLayout>
  );
};

const App: React.FC = () => {
  return (
    <AuthProvider>
      <AppContent />
      <Toaster />
    </AuthProvider>
  );
};

export default App;