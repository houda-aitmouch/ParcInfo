import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from './ui/table';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Badge } from './ui/badge';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from './ui/dialog';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Label } from './ui/label';
import { Progress } from './ui/progress';
import { Avatar, AvatarFallback, AvatarImage } from './ui/avatar';
import { 
  Search, 
  Filter, 
  Plus, 
  Eye, 
  Edit, 
  Truck, 
  Package, 
  CheckCircle2,
  Clock,
  AlertTriangle,
  FileText,
  Download,
  Calendar,
  MapPin
} from 'lucide-react';
import { format, differenceInDays, isAfter, isBefore } from 'date-fns';
import { fr } from 'date-fns/locale';

interface Livraison {
  id: string;
  numeroCommande: string;
  typeLivraison: 'IT' | 'Bureau';
  fournisseur: string;
  statut: 'Programmée' | 'En transit' | 'Arrivée' | 'En cours de réception' | 'Livrée' | 'Retardée' | 'Partiellement livrée';
  datePrevue: Date;
  dateEffective?: Date;
  dateReception?: Date;
  responsableReception?: string;
  lieuLivraison: string;
  montantTotal: number;
  nombreArticles: number;
  articlesRecus?: number;
  conforme: boolean | null;
  pvReception: boolean;
  observations?: string;
  transporteur?: string;
  numeroSuivi?: string;
}

const mockLivraisons: Livraison[] = [
  {
    id: '1',
    numeroCommande: 'BC-2024-001',
    typeLivraison: 'IT',
    fournisseur: 'TechnoMaroc',
    statut: 'Livrée',
    datePrevue: new Date('2024-07-15'),
    dateEffective: new Date('2024-07-14'),
    dateReception: new Date('2024-07-14'),
    responsableReception: 'Ahmed Benali',
    lieuLivraison: 'Siège ADD - Magasin IT',
    montantTotal: 125000,
    nombreArticles: 15,
    articlesRecus: 15,
    conforme: true,
    pvReception: true,
    transporteur: 'DHL Express',
    numeroSuivi: 'DHL123456789',
    observations: 'Livraison conforme, tous les équipements testés'
  },
  {
    id: '2',
    numeroCommande: 'CT-2024-002',
    typeLivraison: 'IT',
    fournisseur: 'InfoSupply',
    statut: 'En transit',
    datePrevue: new Date('2024-07-25'),
    lieuLivraison: 'Siège ADD - Réception',
    montantTotal: 89500,
    nombreArticles: 8,
    conforme: null,
    pvReception: false,
    transporteur: 'Messagerie Express',
    numeroSuivi: 'ME2024789456'
  },
  {
    id: '3',
    numeroCommande: 'BC-BUR-2024-003',
    typeLivraison: 'Bureau',
    fournisseur: 'BureauExpert',
    statut: 'Retardée',
    datePrevue: new Date('2024-07-20'),
    lieuLivraison: 'Siège ADD - Hall principal',
    montantTotal: 45000,
    nombreArticles: 25,
    conforme: null,
    pvReception: false,
    transporteur: 'Transport Local',
    observations: 'Retard fournisseur - Nouveau délai : 28 juillet'
  },
  {
    id: '4',
    numeroCommande: 'MP-2024-001',
    typeLivraison: 'IT',
    fournisseur: 'DigitalPro',
    statut: 'Programmée',
    datePrevue: new Date('2024-07-30'),
    lieuLivraison: 'Data Center ADD',
    montantTotal: 156000,
    nombreArticles: 3,
    conforme: null,
    pvReception: false,
    transporteur: 'Transport Spécialisé IT',
    observations: 'Livraison serveurs - Installation programmée'
  },
  {
    id: '5',
    numeroCommande: 'BC-BUR-2024-005',
    typeLivraison: 'Bureau',
    fournisseur: 'MobilierPro',
    statut: 'Partiellement livrée',
    datePrevue: new Date('2024-07-18'),
    dateEffective: new Date('2024-07-18'),
    dateReception: new Date('2024-07-18'),
    responsableReception: 'Fatima Zahra',
    lieuLivraison: 'Siège ADD - 4ème étage',
    montantTotal: 67500,
    nombreArticles: 12,
    articlesRecus: 8,
    conforme: false,
    pvReception: true,
    transporteur: 'Mobilier Transport',
    observations: '4 articles manquants - En attente de complément'
  }
];

export const Livraisons: React.FC = () => {
  const [livraisons, setLivraisons] = useState<Livraison[]>(mockLivraisons);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [typeFilter, setTypeFilter] = useState('all');
  const [selectedLivraison, setSelectedLivraison] = useState<Livraison | null>(null);
  const [isDetailDialogOpen, setIsDetailDialogOpen] = useState(false);

  const filteredLivraisons = livraisons.filter(liv => {
    const matchesSearch = liv.numeroCommande.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         liv.fournisseur.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         (liv.numeroSuivi && liv.numeroSuivi.toLowerCase().includes(searchTerm.toLowerCase()));
    const matchesStatus = statusFilter === 'all' || liv.statut === statusFilter;
    const matchesType = typeFilter === 'all' || liv.typeLivraison === typeFilter;
    
    return matchesSearch && matchesStatus && matchesType;
  });

  const getStatutBadge = (statut: string, datePrevue: Date) => {
    const isLate = statut === 'Programmée' && isBefore(datePrevue, new Date());
    
    switch (statut) {
      case 'Programmée':
        return <Badge variant={isLate ? "destructive" : "secondary"}>
          {isLate ? 'En retard' : 'Programmée'}
        </Badge>;
      case 'En transit':
        return <Badge className="bg-blue-500">En transit</Badge>;
      case 'Arrivée':
        return <Badge className="bg-orange-500">Arrivée</Badge>;
      case 'En cours de réception':
        return <Badge className="bg-purple-500">En réception</Badge>;
      case 'Livrée':
        return <Badge className="bg-green-500">Livrée</Badge>;
      case 'Retardée':
        return <Badge variant="destructive">Retardée</Badge>;
      case 'Partiellement livrée':
        return <Badge className="bg-yellow-500">Partielle</Badge>;
      default:
        return <Badge variant="outline">{statut}</Badge>;
    }
  };

  const getTypeBadge = (type: string) => {
    return type === 'IT' ? 
      <Badge variant="outline" className="border-blue-200 text-blue-700">IT</Badge> :
      <Badge variant="outline" className="border-purple-200 text-purple-700">Bureau</Badge>;
  };

  const getConformeStatus = (conforme: boolean | null, statut: string) => {
    if (conforme === null || !['Livrée', 'Partiellement livrée'].includes(statut)) {
      return <span className="text-gray-400 text-sm">N/A</span>;
    }
    return conforme ? 
      <Badge className="bg-green-100 text-green-800 border-green-200">Conforme</Badge> :
      <Badge className="bg-red-100 text-red-800 border-red-200">Non conforme</Badge>;
  };

  const getDelaiStatus = (datePrevue: Date, dateEffective?: Date) => {
    if (dateEffective) {
      const joursAvance = differenceInDays(datePrevue, dateEffective);
      if (joursAvance > 0) {
        return { type: 'early', text: `${joursAvance}j d'avance`, color: 'text-green-600' };
      } else if (joursAvance < 0) {
        return { type: 'late', text: `${Math.abs(joursAvance)}j de retard`, color: 'text-red-600' };
      } else {
        return { type: 'ontime', text: 'À temps', color: 'text-green-600' };
      }
    } else {
      const joursRestants = differenceInDays(datePrevue, new Date());
      if (joursRestants < 0) {
        return { type: 'overdue', text: `${Math.abs(joursRestants)}j de retard`, color: 'text-red-600' };
      } else if (joursRestants === 0) {
        return { type: 'today', text: "Aujourd'hui", color: 'text-orange-600' };
      } else {
        return { type: 'upcoming', text: `Dans ${joursRestants}j`, color: 'text-blue-600' };
      }
    }
  };

  const handleViewDetails = (livraison: Livraison) => {
    setSelectedLivraison(livraison);
    setIsDetailDialogOpen(true);
  };

  const getProgressPercentage = (statut: string) => {
    switch (statut) {
      case 'Programmée': return 10;
      case 'En transit': return 50;
      case 'Arrivée': return 75;
      case 'En cours de réception': return 90;
      case 'Livrée': return 100;
      case 'Partiellement livrée': return 85;
      case 'Retardée': return 25;
      default: return 0;
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold bg-gradient-to-r from-green-600 via-emerald-600 to-teal-600 bg-clip-text text-transparent">
            Livraisons
          </h1>
          <p className="text-gray-600">Suivi et gestion des livraisons d'équipements ADD</p>
        </div>
        
        <Button className="gap-2 bg-gradient-to-r from-green-600 via-emerald-600 to-teal-600">
          <Plus className="w-4 h-4" />
          Programmer Livraison
        </Button>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="bg-gradient-to-br from-blue-50 to-cyan-50 border-blue-200">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-blue-600">Total livraisons</p>
                <p className="text-2xl font-bold text-blue-800">{livraisons.length}</p>
              </div>
              <Package className="w-8 h-8 text-blue-600" />
            </div>
          </CardContent>
        </Card>
        
        <Card className="bg-gradient-to-br from-orange-50 to-red-50 border-orange-200">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-orange-600">En transit</p>
                <p className="text-2xl font-bold text-orange-800">
                  {livraisons.filter(l => l.statut === 'En transit').length}
                </p>
              </div>
              <Truck className="w-8 h-8 text-orange-600" />
            </div>
          </CardContent>
        </Card>
        
        <Card className="bg-gradient-to-br from-red-50 to-pink-50 border-red-200">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-red-600">En retard</p>
                <p className="text-2xl font-bold text-red-800">
                  {livraisons.filter(l => {
                    const delai = getDelaiStatus(l.datePrevue, l.dateEffective);
                    return delai.type === 'overdue' || l.statut === 'Retardée';
                  }).length}
                </p>
              </div>
              <AlertTriangle className="w-8 h-8 text-red-600" />
            </div>
          </CardContent>
        </Card>
        
        <Card className="bg-gradient-to-br from-green-50 to-emerald-50 border-green-200">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-green-600">Livrées</p>
                <p className="text-2xl font-bold text-green-800">
                  {livraisons.filter(l => l.statut === 'Livrée').length}
                </p>
              </div>
              <CheckCircle2 className="w-8 h-8 text-green-600" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Filters */}
      <Card>
        <CardContent className="p-4">
          <div className="flex flex-wrap gap-4 items-center">
            <div className="flex items-center gap-2">
              <Search className="w-4 h-4 text-gray-400" />
              <Input
                placeholder="Rechercher par commande, fournisseur ou suivi..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-80"
              />
            </div>
            
            <Select value={statusFilter} onValueChange={setStatusFilter}>
              <SelectTrigger className="w-48">
                <SelectValue placeholder="Statut" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Tous les statuts</SelectItem>
                <SelectItem value="Programmée">Programmée</SelectItem>
                <SelectItem value="En transit">En transit</SelectItem>
                <SelectItem value="Arrivée">Arrivée</SelectItem>
                <SelectItem value="En cours de réception">En réception</SelectItem>
                <SelectItem value="Livrée">Livrée</SelectItem>
                <SelectItem value="Retardée">Retardée</SelectItem>
                <SelectItem value="Partiellement livrée">Partielle</SelectItem>
              </SelectContent>
            </Select>
            
            <Select value={typeFilter} onValueChange={setTypeFilter}>
              <SelectTrigger className="w-32">
                <SelectValue placeholder="Type" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Tous</SelectItem>
                <SelectItem value="IT">IT</SelectItem>
                <SelectItem value="Bureau">Bureau</SelectItem>
              </SelectContent>
            </Select>

            <Button variant="outline" className="gap-2">
              <Filter className="w-4 h-4" />
              Filtres avancés
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Table */}
      <Card>
        <CardHeader>
          <CardTitle>Suivi des livraisons ({filteredLivraisons.length})</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>N° Commande</TableHead>
                <TableHead>Fournisseur</TableHead>
                <TableHead>Type</TableHead>
                <TableHead>Statut</TableHead>
                <TableHead>Date prévue</TableHead>
                <TableHead>Délai</TableHead>
                <TableHead>Conforme</TableHead>
                <TableHead>PV</TableHead>
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredLivraisons.map((livraison) => {
                const delaiStatus = getDelaiStatus(livraison.datePrevue, livraison.dateEffective);
                return (
                  <TableRow key={livraison.id}>
                    <TableCell className="font-mono font-medium">
                      {livraison.numeroCommande}
                    </TableCell>
                    <TableCell>{livraison.fournisseur}</TableCell>
                    <TableCell>{getTypeBadge(livraison.typeLivraison)}</TableCell>
                    <TableCell>{getStatutBadge(livraison.statut, livraison.datePrevue)}</TableCell>
                    <TableCell>
                      <div>
                        <div className="text-sm">
                          {format(livraison.datePrevue, 'dd MMM yyyy', { locale: fr })}
                        </div>
                        {livraison.dateEffective && (
                          <div className="text-xs text-gray-500">
                            Reçu le {format(livraison.dateEffective, 'dd MMM', { locale: fr })}
                          </div>
                        )}
                      </div>
                    </TableCell>
                    <TableCell>
                      <span className={`text-sm ${delaiStatus.color}`}>
                        {delaiStatus.text}
                      </span>
                    </TableCell>
                    <TableCell>
                      {getConformeStatus(livraison.conforme, livraison.statut)}
                    </TableCell>
                    <TableCell>
                      {livraison.pvReception ? 
                        <CheckCircle2 className="w-4 h-4 text-green-600" /> :
                        <Clock className="w-4 h-4 text-gray-400" />
                      }
                    </TableCell>
                    <TableCell>
                      <div className="flex gap-1">
                        <Button 
                          variant="ghost" 
                          size="icon"
                          onClick={() => handleViewDetails(livraison)}
                        >
                          <Eye className="w-4 h-4" />
                        </Button>
                        <Button variant="ghost" size="icon">
                          <Edit className="w-4 h-4" />
                        </Button>
                        {livraison.pvReception && (
                          <Button variant="ghost" size="icon">
                            <Download className="w-4 h-4" />
                          </Button>
                        )}
                      </div>
                    </TableCell>
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      {/* Detail Dialog */}
      <Dialog open={isDetailDialogOpen} onOpenChange={setIsDetailDialogOpen}>
        <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-3">
              <Truck className="w-5 h-5" />
              Détail de la livraison {selectedLivraison?.numeroCommande}
            </DialogTitle>
          </DialogHeader>
          
          {selectedLivraison && (
            <Tabs defaultValue="general" className="w-full">
              <TabsList className="grid w-full grid-cols-4">
                <TabsTrigger value="general">Général</TabsTrigger>
                <TabsTrigger value="suivi">Suivi</TabsTrigger>
                <TabsTrigger value="reception">Réception</TabsTrigger>
                <TabsTrigger value="documents">Documents</TabsTrigger>
              </TabsList>
              
              <TabsContent value="general" className="space-y-6">
                <div className="grid grid-cols-2 gap-6">
                  <div className="space-y-4">
                    <div>
                      <Label className="text-sm text-gray-500">N° Commande</Label>
                      <p className="font-mono font-medium">{selectedLivraison.numeroCommande}</p>
                    </div>
                    <div>
                      <Label className="text-sm text-gray-500">Fournisseur</Label>
                      <p className="font-medium">{selectedLivraison.fournisseur}</p>
                    </div>
                    <div>
                      <Label className="text-sm text-gray-500">Type de livraison</Label>
                      <div>{getTypeBadge(selectedLivraison.typeLivraison)}</div>
                    </div>
                    <div>
                      <Label className="text-sm text-gray-500">Lieu de livraison</Label>
                      <div className="flex items-center gap-2">
                        <MapPin className="w-4 h-4 text-gray-400" />
                        <span>{selectedLivraison.lieuLivraison}</span>
                      </div>
                    </div>
                    <div>
                      <Label className="text-sm text-gray-500">Transporteur</Label>
                      <p>{selectedLivraison.transporteur || 'Non spécifié'}</p>
                    </div>
                  </div>
                  
                  <div className="space-y-4">
                    <div>
                      <Label className="text-sm text-gray-500">Statut</Label>
                      <div>{getStatutBadge(selectedLivraison.statut, selectedLivraison.datePrevue)}</div>
                    </div>
                    <div>
                      <Label className="text-sm text-gray-500">Montant total</Label>
                      <p className="font-bold text-lg">{selectedLivraison.montantTotal.toLocaleString()} DH</p>
                    </div>
                    <div>
                      <Label className="text-sm text-gray-500">Articles</Label>
                      <p>{selectedLivraison.nombreArticles} articles
                        {selectedLivraison.articlesRecus && 
                          ` (${selectedLivraison.articlesRecus} reçus)`
                        }
                      </p>
                    </div>
                    <div>
                      <Label className="text-sm text-gray-500">Date prévue</Label>
                      <p>{format(selectedLivraison.datePrevue, 'dd MMMM yyyy', { locale: fr })}</p>
                    </div>
                    {selectedLivraison.numeroSuivi && (
                      <div>
                        <Label className="text-sm text-gray-500">N° de suivi</Label>
                        <p className="font-mono">{selectedLivraison.numeroSuivi}</p>
                      </div>
                    )}
                  </div>
                </div>
                
                {selectedLivraison.observations && (
                  <div>
                    <Label className="text-sm text-gray-500">Observations</Label>
                    <p className="mt-1 p-3 bg-gray-50 rounded-lg">{selectedLivraison.observations}</p>
                  </div>
                )}
              </TabsContent>
              
              <TabsContent value="suivi" className="space-y-4">
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <Label className="text-sm text-gray-500">Progression de la livraison</Label>
                    <span className="text-sm font-medium">{getProgressPercentage(selectedLivraison.statut)}%</span>
                  </div>
                  <Progress value={getProgressPercentage(selectedLivraison.statut)} className="h-3" />
                  
                  <div className="space-y-3 mt-6">
                    <div className="flex items-center gap-3 p-3 bg-blue-50 rounded-lg">
                      <div className={`w-3 h-3 rounded-full ${
                        ['Programmée', 'En transit', 'Arrivée', 'En cours de réception', 'Livrée', 'Partiellement livrée'].includes(selectedLivraison.statut) 
                          ? 'bg-blue-500' : 'bg-gray-300'
                      }`}></div>
                      <div className="flex-1">
                        <p className="text-sm font-medium">Commande programmée</p>
                        <p className="text-xs text-gray-500">
                          {format(selectedLivraison.datePrevue, 'dd MMMM yyyy', { locale: fr })}
                        </p>
                      </div>
                    </div>
                    
                    {['En transit', 'Arrivée', 'En cours de réception', 'Livrée', 'Partiellement livrée'].includes(selectedLivraison.statut) && (
                      <div className="flex items-center gap-3 p-3 bg-orange-50 rounded-lg">
                        <div className="w-3 h-3 bg-orange-500 rounded-full"></div>
                        <div className="flex-1">
                          <p className="text-sm font-medium">En transit</p>
                          <p className="text-xs text-gray-500">
                            Par {selectedLivraison.transporteur}
                            {selectedLivraison.numeroSuivi && ` • ${selectedLivraison.numeroSuivi}`}
                          </p>
                        </div>
                      </div>
                    )}
                    
                    {['Arrivée', 'En cours de réception', 'Livrée', 'Partiellement livrée'].includes(selectedLivraison.statut) && (
                      <div className="flex items-center gap-3 p-3 bg-purple-50 rounded-lg">
                        <div className="w-3 h-3 bg-purple-500 rounded-full"></div>
                        <div className="flex-1">
                          <p className="text-sm font-medium">Arrivée sur site</p>
                          <p className="text-xs text-gray-500">
                            {selectedLivraison.lieuLivraison}
                          </p>
                        </div>
                      </div>
                    )}
                    
                    {['Livrée', 'Partiellement livrée'].includes(selectedLivraison.statut) && (
                      <div className="flex items-center gap-3 p-3 bg-green-50 rounded-lg">
                        <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                        <div className="flex-1">
                          <p className="text-sm font-medium">Réception terminée</p>
                          <p className="text-xs text-gray-500">
                            {selectedLivraison.dateReception && 
                              `${format(selectedLivraison.dateReception, 'dd MMMM yyyy à HH:mm', { locale: fr })}`
                            } • Par {selectedLivraison.responsableReception}
                          </p>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </TabsContent>
              
              <TabsContent value="reception" className="space-y-4">
                <div className="grid grid-cols-2 gap-6">
                  <div className="space-y-4">
                    <div>
                      <Label className="text-sm text-gray-500">Responsable réception</Label>
                      <p>{selectedLivraison.responsableReception || 'Non assigné'}</p>
                    </div>
                    <div>
                      <Label className="text-sm text-gray-500">Date de réception</Label>
                      <p>{selectedLivraison.dateReception ? 
                        format(selectedLivraison.dateReception, 'dd MMMM yyyy à HH:mm', { locale: fr }) :
                        'Non reçu'}</p>
                    </div>
                    <div>
                      <Label className="text-sm text-gray-500">Articles reçus</Label>
                      <p>{selectedLivraison.articlesRecus || 0} / {selectedLivraison.nombreArticles}</p>
                      {selectedLivraison.articlesRecus && (
                        <Progress 
                          value={(selectedLivraison.articlesRecus / selectedLivraison.nombreArticles) * 100} 
                          className="h-2 mt-2" 
                        />
                      )}
                    </div>
                  </div>
                  
                  <div className="space-y-4">
                    <div>
                      <Label className="text-sm text-gray-500">Conformité</Label>
                      <div className="mt-1">
                        {getConformeStatus(selectedLivraison.conforme, selectedLivraison.statut)}
                      </div>
                    </div>
                    <div>
                      <Label className="text-sm text-gray-500">PV de réception</Label>
                      <div className="flex items-center gap-2 mt-1">
                        {selectedLivraison.pvReception ? (
                          <>
                            <CheckCircle2 className="w-4 h-4 text-green-600" />
                            <span className="text-sm text-green-600">Signé</span>
                          </>
                        ) : (
                          <>
                            <Clock className="w-4 h-4 text-gray-400" />
                            <span className="text-sm text-gray-500">En attente</span>
                          </>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
                
                {selectedLivraison.conforme === false && (
                  <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
                    <div className="flex items-center gap-2">
                      <AlertTriangle className="w-5 h-5 text-red-600" />
                      <span className="font-medium text-red-800">Non-conformité détectée</span>
                    </div>
                    <p className="text-sm text-red-700 mt-1">
                      {selectedLivraison.observations || 'Détails de la non-conformité à renseigner'}
                    </p>
                  </div>
                )}
              </TabsContent>
              
              <TabsContent value="documents" className="space-y-4">
                <div className="space-y-2">
                  <Button variant="outline" className="w-full justify-start gap-2">
                    <FileText className="w-4 h-4" />
                    Bon de commande {selectedLivraison.numeroCommande}
                  </Button>
                  <Button variant="outline" className="w-full justify-start gap-2">
                    <FileText className="w-4 h-4" />
                    Bon de livraison fournisseur
                  </Button>
                  {selectedLivraison.pvReception && (
                    <Button variant="outline" className="w-full justify-start gap-2">
                      <Download className="w-4 h-4" />
                      PV de réception signé
                    </Button>
                  )}
                  <Button variant="outline" className="w-full justify-start gap-2">
                    <FileText className="w-4 h-4" />
                    Facture fournisseur
                  </Button>
                </div>
              </TabsContent>
            </Tabs>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
};