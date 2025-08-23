import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Button } from './ui/button';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from './ui/table';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Progress } from './ui/progress';
import { 
  Package, 
  Truck, 
  FileText, 
  AlertTriangle, 
  TrendingUp, 
  Users, 
  DollarSign,
  Monitor,
  Printer,
  CheckCircle,
  Clock,
  XCircle,
  Calendar
} from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, LineChart, Line } from 'recharts';

const COLORS = ['#2563eb', '#7c3aed', '#dc2626', '#059669', '#d97706'];

// Mock data
const monthlyCommandesData = [
  { name: 'Jan', IT: 24, Bureau: 18 },
  { name: 'Fév', IT: 28, Bureau: 22 },
  { name: 'Mar', IT: 32, Bureau: 25 },
  { name: 'Avr', IT: 29, Bureau: 20 },
  { name: 'Mai', IT: 35, Bureau: 28 },
  { name: 'Jun', IT: 31, Bureau: 24 },
  { name: 'Jul', IT: 27, Bureau: 19 }
];

const livraisonsStatusData = [
  { name: 'Livrées', value: 156, color: '#059669' },
  { name: 'En cours', value: 23, color: '#d97706' },
  { name: 'En retard', value: 8, color: '#dc2626' },
  { name: 'Programmées', value: 45, color: '#2563eb' }
];

const budgetData = [
  { name: 'Jan', budget: 120000, depense: 95000 },
  { name: 'Fév', budget: 120000, depense: 110000 },
  { name: 'Mar', budget: 120000, depense: 87000 },
  { name: 'Avr', budget: 120000, depense: 102000 },
  { name: 'Mai', budget: 120000, depense: 95000 },
  { name: 'Jun', budget: 120000, depense: 118000 },
  { name: 'Jul', budget: 120000, depense: 89000 }
];

const recentActivities = [
  {
    id: '1',
    type: 'commande',
    description: 'Nouvelle commande BC-2024-089 créée',
    user: 'Ahmed Benali',
    time: 'Il y a 2h',
    status: 'success'
  },
  {
    id: '2',
    type: 'livraison',
    description: 'Livraison CT-2024-012 terminée',
    user: 'Système',
    time: 'Il y a 3h',
    status: 'success'
  },
  {
    id: '3',
    type: 'demande',
    description: 'Demande DEQ-2024-156 approuvée',
    user: 'Fatima Zahra',
    time: 'Il y a 4h',
    status: 'info'
  },
  {
    id: '4',
    type: 'alerte',
    description: 'Garantie Dell Latitude expire dans 7 jours',
    user: 'Système',
    time: 'Il y a 6h',
    status: 'warning'
  }
];

export const Dashboard: React.FC = () => {
  const { user } = useAuth();

  const getKPICards = () => {
    const baseCards = [
      {
        title: 'Équipements Totaux',
        value: '1,247',
        change: '+5.2%',
        changeType: 'positive' as const,
        icon: <Package className="w-5 h-5" />,
        description: 'Actifs en service'
      },
      {
        title: 'Livraisons ce mois',
        value: '23',
        change: '+12%',
        changeType: 'positive' as const,
        icon: <Truck className="w-5 h-5" />,
        description: '8 en retard'
      },
      {
        title: 'Demandes en attente',
        value: '15',
        change: '-8%',
        changeType: 'negative' as const,
        icon: <FileText className="w-5 h-5" />,
        description: 'À traiter rapidement'
      },
      {
        title: 'Alertes garantie',
        value: '12',
        change: '+3',
        changeType: 'warning' as const,
        icon: <AlertTriangle className="w-5 h-5" />,
        description: 'Expirent sous 30j'
      }
    ];

    if (user?.role === 'superadmin') {
      return [...baseCards, {
        title: 'Budget annuel',
        value: '1.2M DH',
        change: '73% utilisé',
        changeType: 'neutral' as const,
        icon: <DollarSign className="w-5 h-5" />,
        description: 'Reste 324K DH'
      }];
    }

    return baseCards;
  };

  const getRoleSpecificContent = () => {
    switch (user?.role) {
      case 'employe':
        return {
          title: 'Mon Espace',
          description: 'Vue d\'ensemble de vos équipements et demandes',
          showBudget: false,
          showUsers: false
        };
      case 'gestionnaire_informatique':
        return {
          title: 'Gestion Informatique',
          description: 'Suivi des équipements et commandes IT',
          showBudget: true,
          showUsers: false
        };
      case 'gestionnaire_bureau':
        return {
          title: 'Gestion Bureautique',
          description: 'Suivi des équipements et commandes bureautiques',
          showBudget: true,
          showUsers: false
        };
      case 'superadmin':
        return {
          title: 'Administration Générale',
          description: 'Vue d\'ensemble complète du système',
          showBudget: true,
          showUsers: true
        };
      default:
        return {
          title: 'Tableau de Bord',
          description: 'Vue d\'ensemble',
          showBudget: false,
          showUsers: false
        };
    }
  };

  const roleContent = getRoleSpecificContent();
  const kpiCards = getKPICards();

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="space-y-2">
        <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
          {roleContent.title}
        </h1>
        <p className="text-gray-600">{roleContent.description}</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 xl:grid-cols-5 gap-4">
        {kpiCards.map((card, index) => (
          <Card key={index} className="hover:shadow-lg transition-shadow">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div className="space-y-1">
                  <p className="text-sm text-gray-600">{card.title}</p>
                  <p className="text-2xl font-bold">{card.value}</p>
                  <div className="flex items-center gap-2">
                    <Badge 
                      variant={
                        card.changeType === 'positive' ? 'default' :
                        card.changeType === 'negative' ? 'destructive' :
                        card.changeType === 'warning' ? 'secondary' : 'outline'
                      }
                      className="text-xs"
                    >
                      {card.change}
                    </Badge>
                  </div>
                  <p className="text-xs text-gray-500">{card.description}</p>
                </div>
                <div className="w-12 h-12 bg-gradient-to-br from-blue-100 to-indigo-100 rounded-lg flex items-center justify-center">
                  {card.icon}
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Main Content Tabs */}
      <Tabs defaultValue="overview" className="space-y-4">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="overview">Vue d'ensemble</TabsTrigger>
          <TabsTrigger value="equipment">Équipements</TabsTrigger>
          <TabsTrigger value="activity">Activité</TabsTrigger>
          {roleContent.showBudget && <TabsTrigger value="budget">Budget</TabsTrigger>}
        </TabsList>

        <TabsContent value="overview" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Commandes mensuelles */}
            <Card>
              <CardHeader>
                <CardTitle>Commandes par mois</CardTitle>
                <CardDescription>Évolution des commandes IT et bureautiques</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={monthlyCommandesData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="IT" fill="#2563eb" name="Informatique" />
                    <Bar dataKey="Bureau" fill="#7c3aed" name="Bureautique" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            {/* Statut des livraisons */}
            <Card>
              <CardHeader>
                <CardTitle>Statut des livraisons</CardTitle>
                <CardDescription>Répartition des livraisons par statut</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={livraisonsStatusData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, value }) => `${name}: ${value}`}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {livraisonsStatusData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>

          {/* Activité récente */}
          <Card>
            <CardHeader>
              <CardTitle>Activité récente</CardTitle>
              <CardDescription>Dernières actions sur la plateforme</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {recentActivities.map((activity) => (
                  <div key={activity.id} className="flex items-center gap-4 p-3 rounded-lg hover:bg-gray-50">
                    <div className={`w-2 h-2 rounded-full ${
                      activity.status === 'success' ? 'bg-green-500' :
                      activity.status === 'warning' ? 'bg-orange-500' :
                      activity.status === 'info' ? 'bg-blue-500' : 'bg-gray-400'
                    }`} />
                    <div className="flex-1">
                      <p className="text-sm font-medium">{activity.description}</p>
                      <p className="text-xs text-gray-500">Par {activity.user} • {activity.time}</p>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="equipment" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Monitor className="w-5 h-5" />
                  Équipements IT
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>Ordinateurs portables</span>
                    <span>245</span>
                  </div>
                  <Progress value={82} className="h-2" />
                </div>
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>Ordinateurs fixes</span>
                    <span>156</span>
                  </div>
                  <Progress value={65} className="h-2" />
                </div>
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>Serveurs</span>
                    <span>12</span>
                  </div>
                  <Progress value={75} className="h-2" />
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Printer className="w-5 h-5" />
                  Équipements Bureau
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>Imprimantes</span>
                    <span>89</span>
                  </div>
                  <Progress value={71} className="h-2" />
                </div>
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>Scanners</span>
                    <span>34</span>
                  </div>
                  <Progress value={55} className="h-2" />
                </div>
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>Projecteurs</span>
                    <span>28</span>
                  </div>
                  <Progress value={90} className="h-2" />
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>État des garanties</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
                  <div>
                    <p className="text-sm font-medium text-green-800">Sous garantie</p>
                    <p className="text-2xl font-bold text-green-600">892</p>
                  </div>
                  <CheckCircle className="w-8 h-8 text-green-600" />
                </div>
                <div className="flex items-center justify-between p-3 bg-orange-50 rounded-lg">
                  <div>
                    <p className="text-sm font-medium text-orange-800">Expire bientôt</p>
                    <p className="text-2xl font-bold text-orange-600">45</p>
                  </div>
                  <Clock className="w-8 h-8 text-orange-600" />
                </div>
                <div className="flex items-center justify-between p-3 bg-red-50 rounded-lg">
                  <div>
                    <p className="text-sm font-medium text-red-800">Expirée</p>
                    <p className="text-2xl font-bold text-red-600">123</p>
                  </div>
                  <XCircle className="w-8 h-8 text-red-600" />
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="activity" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Journal d'activité</CardTitle>
              <CardDescription>Toutes les actions récentes sur la plateforme</CardDescription>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Action</TableHead>
                    <TableHead>Utilisateur</TableHead>
                    <TableHead>Date/Heure</TableHead>
                    <TableHead>Statut</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {recentActivities.map((activity) => (
                    <TableRow key={activity.id}>
                      <TableCell>{activity.description}</TableCell>
                      <TableCell>{activity.user}</TableCell>
                      <TableCell>{activity.time}</TableCell>
                      <TableCell>
                        <Badge variant={
                          activity.status === 'success' ? 'default' :
                          activity.status === 'warning' ? 'secondary' : 'outline'
                        }>
                          {activity.status === 'success' ? 'Succès' :
                           activity.status === 'warning' ? 'Attention' : 'Info'}
                        </Badge>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </TabsContent>

        {roleContent.showBudget && (
          <TabsContent value="budget" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <Card className="lg:col-span-2">
                <CardHeader>
                  <CardTitle>Évolution budgétaire</CardTitle>
                  <CardDescription>Budget vs dépenses mensuelles</CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={budgetData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="name" />
                      <YAxis />
                      <Tooltip formatter={(value) => [`${value} DH`, '']} />
                      <Line type="monotone" dataKey="budget" stroke="#2563eb" name="Budget" strokeDasharray="5 5" />
                      <Line type="monotone" dataKey="depense" stroke="#dc2626" name="Dépenses" />
                    </LineChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Résumé budgétaire</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-600">Budget annuel</span>
                      <span className="font-medium">1,200,000 DH</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-600">Dépensé</span>
                      <span className="font-medium text-red-600">876,000 DH</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-600">Restant</span>
                      <span className="font-medium text-green-600">324,000 DH</span>
                    </div>
                    <Progress value={73} className="h-3" />
                    <p className="text-xs text-gray-500">73% du budget utilisé</p>
                  </div>

                  <div className="pt-4 border-t">
                    <h4 className="font-medium mb-3">Répartition par catégorie</h4>
                    <div className="space-y-3">
                      <div className="flex justify-between items-center">
                        <span className="text-sm">Équipements IT</span>
                        <span className="text-sm font-medium">65%</span>
                      </div>
                      <Progress value={65} className="h-2" />
                      
                      <div className="flex justify-between items-center">
                        <span className="text-sm">Équipements Bureau</span>
                        <span className="text-sm font-medium">25%</span>
                      </div>
                      <Progress value={25} className="h-2" />
                      
                      <div className="flex justify-between items-center">
                        <span className="text-sm">Maintenance</span>
                        <span className="text-sm font-medium">10%</span>
                      </div>
                      <Progress value={10} className="h-2" />
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        )}
      </Tabs>
    </div>
  );
};