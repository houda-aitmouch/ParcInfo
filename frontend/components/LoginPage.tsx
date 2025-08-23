import React, { useState } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Alert, AlertDescription } from './ui/alert';
import { Loader2, Shield, Users, Database, Zap } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import addLogo from '../assets/add.png';

interface LoginPageProps {
  onLogin: () => void;
}

export const LoginPage: React.FC<LoginPageProps> = ({ onLogin }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const { login } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      const success = await login(username, password);
      if (success) {
        onLogin();
      } else {
        setError('Identifiants incorrects. Veuillez réessayer.');
      }
    } catch (err) {
      setError('Une erreur est survenue lors de la connexion.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDemoLogin = async (demoUsername: string) => {
    setUsername(demoUsername);
    setPassword('admin123');
    setIsLoading(true);
    setError('');

    try {
      const success = await login(demoUsername, 'admin123');
      if (success) {
        onLogin();
      }
    } catch (err) {
      setError('Une erreur est survenue lors de la connexion.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 flex items-center justify-center p-4">
      <div className="w-full max-w-6xl grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
        
        {/* Left side - Branding & Info */}
        <div className="space-y-8 text-center lg:text-left">
          <div className="space-y-6">
            {/* Logo officiel #ADD */}
            <div className="flex justify-center lg:justify-start">
              <div className="bg-white/80 backdrop-blur-sm rounded-2xl p-6 shadow-lg">
                <img 
                  src={addLogo} 
                  alt="Agence de Développement du Digital" 
                  className="h-16 w-auto"
                />
              </div>
            </div>
            
            <div className="space-y-4">
              <h1 className="text-4xl lg:text-5xl font-bold text-gray-900 leading-tight">
                Gestion Intelligente
                <br />
                <span className="bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 bg-clip-text text-transparent">
                  de Parc IT
                </span>
              </h1>
              
              <p className="text-lg text-gray-600 max-w-md mx-auto lg:mx-0">
                Plateforme officielle de l'ADD pour la gestion complète des équipements informatiques et bureautiques avec IA intégrée.
              </p>

              {/* Badge institutionnel */}
              <div className="inline-flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-blue-100 to-purple-100 rounded-full">
                <Shield className="w-4 h-4 text-blue-600" />
                <span className="text-sm font-medium text-gray-800">Plateforme Gouvernementale Sécurisée</span>
              </div>
            </div>
          </div>

          {/* Features */}
          <div className="grid grid-cols-2 gap-4 max-w-md mx-auto lg:mx-0">
            <div className="flex items-center gap-3 p-3 bg-white/60 backdrop-blur-sm rounded-lg border border-blue-100">
              <Shield className="w-5 h-5 text-blue-600" />
              <span className="text-sm font-medium text-gray-700">Sécurisé SSL</span>
            </div>
            <div className="flex items-center gap-3 p-3 bg-white/60 backdrop-blur-sm rounded-lg border border-purple-100">
              <Users className="w-5 h-5 text-purple-600" />
              <span className="text-sm font-medium text-gray-700">Multi-rôles</span>
            </div>
            <div className="flex items-center gap-3 p-3 bg-white/60 backdrop-blur-sm rounded-lg border border-indigo-100">
              <Database className="w-5 h-5 text-indigo-600" />
              <span className="text-sm font-medium text-gray-700">Traçabilité</span>
            </div>
            <div className="flex items-center gap-3 p-3 bg-white/60 backdrop-blur-sm rounded-lg border border-orange-100">
              <Zap className="w-5 h-5 text-orange-600" />
              <span className="text-sm font-medium text-gray-700">IA Intégrée</span>
            </div>
          </div>

          {/* Stats institutionnelles */}
          <div className="grid grid-cols-3 gap-4 max-w-sm mx-auto lg:mx-0">
            <div className="text-center p-3 bg-white/40 backdrop-blur-sm rounded-lg">
              <div className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">1,250+</div>
              <div className="text-sm text-gray-600">Équipements</div>
            </div>
            <div className="text-center p-3 bg-white/40 backdrop-blur-sm rounded-lg">
              <div className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-indigo-600 bg-clip-text text-transparent">150+</div>
              <div className="text-sm text-gray-600">Agents</div>
            </div>
            <div className="text-center p-3 bg-white/40 backdrop-blur-sm rounded-lg">
              <div className="text-2xl font-bold bg-gradient-to-r from-indigo-600 to-blue-600 bg-clip-text text-transparent">99.9%</div>
              <div className="text-sm text-gray-600">Disponibilité</div>
            </div>
          </div>

          {/* Informations de contact institutionnel */}
          <div className="text-center lg:text-left text-sm text-gray-500">
            <p>Service support : support@add.gov.ma</p>
            <p>Environnement de démonstration - ADD 2024</p>
          </div>
        </div>

        {/* Right side - Login Form */}
        <div className="w-full max-w-md mx-auto">
          <Card className="shadow-xl border-0 bg-white/95 backdrop-blur-sm">
            <CardHeader className="space-y-1 text-center">
              <CardTitle className="text-2xl">Connexion Sécurisée</CardTitle>
              <CardDescription>
                Accédez à votre espace de gestion ADD
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="username">Nom d'utilisateur</Label>
                  <Input
                    id="username"
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder="votre.nom@add.gov.ma"
                    required
                    disabled={isLoading}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="password">Mot de passe</Label>
                  <Input
                    id="password"
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="••••••••"
                    required
                    disabled={isLoading}
                  />
                </div>

                {error && (
                  <Alert variant="destructive">
                    <AlertDescription>{error}</AlertDescription>
                  </Alert>
                )}

                <Button 
                  type="submit" 
                  className="w-full bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 hover:from-blue-700 hover:via-purple-700 hover:to-indigo-700" 
                  disabled={isLoading}
                >
                  {isLoading && <Loader2 className="w-4 h-4 mr-2 animate-spin" />}
                  Se connecter
                </Button>
              </form>

              <div className="relative">
                <div className="absolute inset-0 flex items-center">
                  <span className="w-full border-t" />
                </div>
                <div className="relative flex justify-center text-xs uppercase">
                  <span className="bg-background px-2 text-muted-foreground">
                    Comptes de démonstration ADD
                  </span>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => handleDemoLogin('superadmin')}
                  disabled={isLoading}
                  className="h-auto p-3 flex flex-col gap-1 border-blue-200 hover:bg-blue-50"
                >
                  <span className="font-medium">Superadmin</span>
                  <span className="text-xs text-gray-500">Tous droits</span>
                  <span className="text-xs text-blue-600">superadmin</span>
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => handleDemoLogin('gestionnaire.it')}
                  disabled={isLoading}
                  className="h-auto p-3 flex flex-col gap-1 border-purple-200 hover:bg-purple-50"
                >
                  <span className="font-medium">IT Manager</span>
                  <span className="text-xs text-gray-500">Informatique</span>
                  <span className="text-xs text-purple-600">gestionnaire.it</span>
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => handleDemoLogin('gestionnaire.bureau')}
                  disabled={isLoading}
                  className="h-auto p-3 flex flex-col gap-1 border-indigo-200 hover:bg-indigo-50"
                >
                  <span className="font-medium">Bureau Manager</span>
                  <span className="text-xs text-gray-500">Bureautique</span>
                  <span className="text-xs text-indigo-600">gestionnaire.bureau</span>
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => handleDemoLogin('employe.dev')}
                  disabled={isLoading}
                  className="h-auto p-3 flex flex-col gap-1 border-orange-200 hover:bg-orange-50"
                >
                  <span className="font-medium">Employé</span>
                  <span className="text-xs text-gray-500">Consultation</span>
                  <span className="text-xs text-orange-600">employe.dev</span>
                </Button>
              </div>

              <div className="space-y-2 text-center">
                <p className="text-xs text-gray-500">
                  Mot de passe démo : <code className="bg-gray-100 px-1 rounded">admin123</code>
                </p>
                <p className="text-xs text-gray-400">
                  🔒 Données de démonstration - Environnement sécurisé ADD
                </p>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};