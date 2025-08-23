import React, { useState } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Avatar, AvatarFallback, AvatarImage } from './ui/avatar';
import { Badge } from './ui/badge';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from './ui/dropdown-menu';
import { 
  LayoutDashboard, 
  Package, 
  Truck, 
  FileText, 
  Building2, 
  Users, 
  Settings, 
  Search, 
  Bell, 
  LogOut,
  Menu,
  Monitor,
  Printer,
  HelpCircle
} from 'lucide-react';
import { useAuth, UserRole } from '../contexts/AuthContext';
import { Chatbot } from './Chatbot';
import addLogo from '../assets/add.png';

interface AppLayoutProps {
  children: React.ReactNode;
  currentPage: string;
  onNavigate: (page: string) => void;
}

interface MenuItem {
  id: string;
  label: string;
  icon: React.ReactNode;
  roles: UserRole[];
  badge?: string;
}

const menuItems: MenuItem[] = [
  {
    id: 'dashboard',
    label: 'Tableau de bord',
    icon: <LayoutDashboard className="w-5 h-5" />,
    roles: ['superadmin', 'gestionnaire_informatique', 'gestionnaire_bureau', 'employe']
  },
  {
    id: 'commandes-it',
    label: 'Commandes IT',
    icon: <Monitor className="w-5 h-5" />,
    roles: ['superadmin', 'gestionnaire_informatique'],
    badge: '3'
  },
  {
    id: 'commandes-bureau',
    label: 'Commandes Bureau',
    icon: <Printer className="w-5 h-5" />,
    roles: ['superadmin', 'gestionnaire_bureau'],
    badge: '2'
  },
  {
    id: 'materiels-it',
    label: 'Matériels IT',
    icon: <Monitor className="w-5 h-5" />,
    roles: ['superadmin', 'gestionnaire_informatique', 'employe']
  },
  {
    id: 'materiels-bureau',
    label: 'Matériels Bureau',
    icon: <Printer className="w-5 h-5" />,
    roles: ['superadmin', 'gestionnaire_bureau', 'employe']
  },
  {
    id: 'livraisons',
    label: 'Livraisons',
    icon: <Truck className="w-5 h-5" />,
    roles: ['superadmin', 'gestionnaire_informatique', 'gestionnaire_bureau', 'employe']
  },
  {
    id: 'demandes',
    label: 'Demandes équipement',
    icon: <FileText className="w-5 h-5" />,
    roles: ['superadmin', 'gestionnaire_informatique', 'gestionnaire_bureau', 'employe'],
    badge: '5'
  },
  {
    id: 'fournisseurs',
    label: 'Fournisseurs',
    icon: <Building2 className="w-5 h-5" />,
    roles: ['superadmin', 'gestionnaire_informatique', 'gestionnaire_bureau']
  },
  {
    id: 'utilisateurs',
    label: 'Utilisateurs & permissions',
    icon: <Users className="w-5 h-5" />,
    roles: ['superadmin']
  }
];

export const AppLayout: React.FC<AppLayoutProps> = ({ children, currentPage, onNavigate }) => {
  const { user, logout } = useAuth();
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [isChatbotOpen, setIsChatbotOpen] = useState(false);

  const allowedMenuItems = menuItems.filter(item => 
    user && item.roles.includes(user.role)
  );

  const getRoleBadge = (role: UserRole) => {
    switch (role) {
      case 'superadmin':
        return <Badge className="bg-gradient-to-r from-red-500 to-pink-500">Superadmin</Badge>;
      case 'gestionnaire_informatique':
        return <Badge className="bg-gradient-to-r from-blue-500 to-cyan-500">IT Manager</Badge>;
      case 'gestionnaire_bureau':
        return <Badge className="bg-gradient-to-r from-purple-500 to-violet-500">Bureau Manager</Badge>;
      case 'employe':
        return <Badge variant="outline" className="border-orange-300 text-orange-600">Employé</Badge>;
      default:
        return null;
    }
  };

  const getInitials = (name: string) => {
    return name.split(' ').map(n => n[0]).join('').toUpperCase();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      {/* Header */}
      <header className="sticky top-0 z-40 w-full border-b bg-white/95 backdrop-blur supports-[backdrop-filter]:bg-white/60">
        <div className="flex h-16 items-center px-4 gap-4">
          {/* Mobile menu button */}
          <Button
            variant="ghost"
            size="icon"
            className="lg:hidden"
            onClick={() => setIsSidebarOpen(!isSidebarOpen)}
          >
            <Menu className="h-5 w-5" />
          </Button>

          {/* Logo ADD officiel */}
          <div className="flex items-center gap-3">
            <img 
              src={addLogo} 
              alt="ADD" 
              className="h-8 w-auto"
            />
            <div className="hidden sm:block">
              <div className="text-sm font-semibold bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 bg-clip-text text-transparent">
                ParcInfo
              </div>
              <div className="text-xs text-gray-500">
                Agence de Développement du Digital
              </div>
            </div>
          </div>

          {/* Search */}
          <div className="flex-1 max-w-md mx-4 hidden md:block">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
              <Input 
                placeholder="Rechercher équipements, commandes..." 
                className="pl-10 bg-gray-50/50 border-gray-200"
              />
            </div>
          </div>

          <div className="flex items-center gap-2">
            {/* Notifications */}
            <Button variant="ghost" size="icon" className="relative hover:bg-blue-50">
              <Bell className="w-5 h-5" />
              <span className="absolute -top-1 -right-1 w-3 h-3 bg-gradient-to-r from-red-500 to-pink-500 rounded-full text-xs text-white flex items-center justify-center">
                3
              </span>
            </Button>

            {/* Chatbot toggle */}
            <Button 
              variant="ghost" 
              size="icon"
              onClick={() => setIsChatbotOpen(!isChatbotOpen)}
              className={isChatbotOpen ? 'bg-blue-100 text-blue-600' : 'hover:bg-purple-50'}
            >
              <HelpCircle className="w-5 h-5" />
            </Button>

            {/* User menu */}
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" className="h-10 gap-2 px-3 hover:bg-gray-50">
                  <Avatar className="w-8 h-8">
                    <AvatarImage src="" />
                    <AvatarFallback className="bg-gradient-to-br from-blue-600 via-purple-600 to-indigo-600 text-white">
                      {user ? getInitials(user.name) : 'U'}
                    </AvatarFallback>
                  </Avatar>
                  <div className="hidden md:flex flex-col items-start">
                    <span className="text-sm font-medium">{user?.name}</span>
                    <span className="text-xs text-gray-500">{user?.department}</span>
                  </div>
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="w-56">
                <DropdownMenuLabel className="flex flex-col gap-1">
                  <span>{user?.name}</span>
                  <span className="text-xs text-gray-500">{user?.email}</span>
                  <div className="flex items-center gap-2 mt-1">
                    {user && getRoleBadge(user.role)}
                  </div>
                </DropdownMenuLabel>
                <DropdownMenuSeparator />
                <DropdownMenuItem onClick={() => onNavigate('profile')} className="cursor-pointer">
                  <Settings className="w-4 h-4 mr-2" />
                  Profil & paramètres
                </DropdownMenuItem>
                <DropdownMenuSeparator />
                <DropdownMenuItem onClick={logout} className="text-red-600 cursor-pointer">
                  <LogOut className="w-4 h-4 mr-2" />
                  Déconnexion
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        </div>
      </header>

      <div className="flex">
        {/* Sidebar */}
        <aside className={`
          fixed inset-y-0 left-0 z-30 w-64 bg-white/95 backdrop-blur border-r transform transition-transform duration-200 ease-in-out lg:translate-x-0 lg:static lg:inset-0
          ${isSidebarOpen ? 'translate-x-0' : '-translate-x-full'}
        `}>
          <div className="flex flex-col h-full pt-16 lg:pt-0">
            {/* Sidebar Header */}
            <div className="p-4 border-b border-gray-100 lg:hidden">
              <div className="flex items-center gap-3">
                <img 
                  src={addLogo} 
                  alt="ADD" 
                  className="h-6 w-auto"
                />
                <div>
                  <div className="text-sm font-semibold bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 bg-clip-text text-transparent">
                    ParcInfo
                  </div>
                  <div className="text-xs text-gray-500">
                    ADD
                  </div>
                </div>
              </div>
            </div>

            <nav className="flex-1 px-3 py-4 space-y-1">
              {allowedMenuItems.map((item) => (
                <Button
                  key={item.id}
                  variant={currentPage === item.id ? "default" : "ghost"}
                  className={`w-full justify-start gap-3 h-11 ${
                    currentPage === item.id 
                      ? 'bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 text-white shadow-lg' 
                      : 'hover:bg-gradient-to-r hover:from-blue-50 hover:to-purple-50 hover:text-blue-700'
                  }`}
                  onClick={() => {
                    onNavigate(item.id);
                    setIsSidebarOpen(false);
                  }}
                >
                  {item.icon}
                  <span className="flex-1 text-left">{item.label}</span>
                  {item.badge && (
                    <Badge 
                      variant="secondary" 
                      className={`ml-auto ${
                        currentPage === item.id 
                          ? 'bg-white/20 text-white' 
                          : 'bg-blue-100 text-blue-600'
                      }`}
                    >
                      {item.badge}
                    </Badge>
                  )}
                </Button>
              ))}
            </nav>

            {/* Footer ADD */}
            <div className="p-4 border-t border-gray-100">
              <div className="text-center">
                <p className="text-xs text-gray-500">
                  © 2024 Agence de Développement du Digital
                </p>
                <p className="text-xs text-gray-400">
                  Version 1.0.0 - Environment Demo
                </p>
              </div>
            </div>
          </div>
        </aside>

        {/* Mobile overlay */}
        {isSidebarOpen && (
          <div 
            className="fixed inset-0 z-20 bg-black/50 lg:hidden"
            onClick={() => setIsSidebarOpen(false)}
          />
        )}

        {/* Main content */}
        <main className="flex-1 lg:pl-0">
          <div className="p-6">
            {children}
          </div>
        </main>

        {/* Chatbot */}
        <Chatbot isOpen={isChatbotOpen} onClose={() => setIsChatbotOpen(false)} />
      </div>
    </div>
  );
};