import React, { createContext, useContext, useState, ReactNode } from 'react';

export type UserRole = 'superadmin' | 'gestionnaire_informatique' | 'gestionnaire_bureau' | 'employe';

export interface User {
  id: string;
  username: string;
  email: string;
  name: string;
  role: UserRole;
  department?: string;
}

interface AuthContextType {
  user: User | null;
  login: (username: string, password: string) => Promise<boolean>;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

// Mock users database
const mockUsers: User[] = [
  {
    id: '1',
    username: 'superadmin',
    email: 'admin@parcinfo.ma',
    name: 'Admin Principal',
    role: 'superadmin',
    department: 'Direction IT'
  },
  {
    id: '2',
    username: 'gestionnaire.it',
    email: 'it.manager@parcinfo.ma',
    name: 'Ahmed Benali',
    role: 'gestionnaire_informatique',
    department: 'Service Informatique'
  },
  {
    id: '3',
    username: 'gestionnaire.bureau',
    email: 'bureau.manager@parcinfo.ma',
    name: 'Fatima Zahra',
    role: 'gestionnaire_bureau',
    department: 'Service Bureautique'
  },
  {
    id: '4',
    username: 'employe.dev',
    email: 'mohammed.alami@parcinfo.ma',
    name: 'Mohammed Alami',
    role: 'employe',
    department: 'Développement'
  }
];

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);

  const login = async (username: string, password: string): Promise<boolean> => {
    try {
      // Utiliser la nouvelle API de login
      const formData = new FormData();
      formData.append('username', username);
      formData.append('password', password);

      const response = await fetch('/api/login/', {
        method: 'POST',
        body: formData,
        credentials: 'include',
      });

      if (response.ok) {
        const data = await response.json();
        if (data.success) {
          // Définir directement l'utilisateur avec les données reçues
          setUser({
            id: data.user.id.toString(),
            username: data.user.username,
            email: data.user.email,
            name: `${data.user.first_name} ${data.user.last_name}`.trim() || data.user.username,
            role: data.user.role as UserRole,
            department: data.user.groups?.[0] || 'Service'
          });
          return true;
        }
      }
      return false;
    } catch (error) {
      console.error('Erreur de connexion:', error);
      return false;
    }
  };

  const fetchUserInfo = async () => {
    try {
      const response = await fetch('/api/user-info/', {
        credentials: 'include',
      });
      
      if (response.ok) {
        const userData = await response.json();
        setUser({
          id: userData.id.toString(),
          username: userData.username,
          email: userData.email,
          name: `${userData.first_name} ${userData.last_name}`.trim() || userData.username,
          role: userData.role as UserRole,
          department: userData.groups?.[0] || 'Service'
        });
      }
    } catch (error) {
      console.error('Erreur lors de la récupération des informations utilisateur:', error);
    }
  };

  const logout = async () => {
    try {
      await fetch('/accounts/logout/', {
        method: 'POST',
        credentials: 'include',
      });
    } catch (error) {
      console.error('Erreur lors de la déconnexion:', error);
    } finally {
      setUser(null);
    }
  };

  // Fonction pour récupérer le token CSRF
  const getCsrfToken = (): string => {
    const cookies = document.cookie.split(';');
    const csrfCookie = cookies.find(cookie => cookie.trim().startsWith('csrftoken='));
    return csrfCookie ? csrfCookie.split('=')[1] : '';
  };

  // Vérifier l'authentification au chargement de la page
  React.useEffect(() => {
    fetchUserInfo();
  }, []);

  const value: AuthContextType = {
    user,
    login,
    logout,
    isAuthenticated: !!user
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};