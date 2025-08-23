import React, { useState } from "react";
import { AuthProvider, useAuth } from "./contexts/AuthContext";
import { LoginPage } from "./components/LoginPage";
import { AppLayout } from "./components/AppLayout";
import { Dashboard } from "./components/Dashboard";
import { CommandesIT } from "./components/CommandesIT";
import { CommandesBureau } from "./components/CommandesBureau";
import { MaterielsIT } from "./components/MaterielsIT";
import { MaterielsBureau } from "./components/MaterielsBureau";
import { Livraisons } from "./components/Livraisons";
import { Demandes } from "./components/Demandes";
import { Fournisseurs } from "./components/Fournisseurs";
import { Utilisateurs } from "./components/Utilisateurs";
import { Profile } from "./components/Profile";
import { Toaster } from "./components/ui/sonner";

const AppContent: React.FC = () => {
  const { isAuthenticated } = useAuth();
  const [currentPage, setCurrentPage] = useState("dashboard");

  if (!isAuthenticated) {
    return (
      <LoginPage onLogin={() => setCurrentPage("dashboard")} />
    );
  }

  const renderCurrentPage = () => {
    switch (currentPage) {
      case "dashboard":
        return <Dashboard />;
      case "commandes-it":
        return <CommandesIT />;
      case "commandes-bureau":
        return <CommandesBureau />;
      case "materiels-it":
        return <MaterielsIT />;
      case "materiels-bureau":
        return <MaterielsBureau />;
      case "livraisons":
        return <Livraisons />;
      case "demandes":
        return <Demandes />;
      case "fournisseurs":
        return <Fournisseurs />;
      case "utilisateurs":
        return <Utilisateurs />;
      case "profile":
        return <Profile />;
      default:
        return <Dashboard />;
    }
  };

  return (
    <AppLayout
      currentPage={currentPage}
      onNavigate={setCurrentPage}
    >
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