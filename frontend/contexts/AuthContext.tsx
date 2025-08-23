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
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    const foundUser = mockUsers.find(u => u.username === username);
    if (foundUser && password === 'admin123') {
      setUser(foundUser);
      return true;
    }
    return false;
  };

  const logout = () => {
    setUser(null);
  };

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