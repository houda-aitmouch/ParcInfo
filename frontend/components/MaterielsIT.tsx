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
import { Textarea } from './ui/textarea';
import { Progress } from './ui/progress';
import { Avatar, AvatarFallback, AvatarImage } from './ui/avatar';
import { 
  Search, 
  Filter, 
  Plus, 
  Eye, 
  Edit, 
  Trash2, 
  Monitor, 
  Laptop, 
  Server, 
  Smartphone,
  User,
  MapPin,
  Calendar,
  AlertTriangle,
  CheckCircle,
  Settings,
  History
} from 'lucide-react';
import { format, differenceInDays, addMonths } from 'date-fns';
import { fr } from 'date-fns/locale';

interface MaterielIT {
  id: string;
  codeInventaire: string;
  numeroSerie: string;
  designation: string;
  marque: string;
  modele: string;
  type: 'Ordinateur Portable' | 'Ordinateur Fixe' | 'Serveur' | 'Écran' | 'Imprimante' | 'Réseau';
  statut: 'Opérationnel' | 'Panne' | 'Maintenance' | 'Stock' | 'Réformé';
  utilisateur?: string;
  lieu: string;
  etage?: string;
  bureau?: string;
  dateAchat: Date;
  prixAchat: number;
  fournisseur: string;
  numeroCommande: string;
  dureeGarantie: number;
  dateFinGarantie: Date;
  observations?: string;
}

const mockMaterielsIT: MaterielIT[] = [
  {
    id: '1',
    codeInventaire: 'INV-IT-2024-001',
    numeroSerie: 'DL75200123',
    designation: 'Ordinateur portable Dell Latitude 7520',
    marque: 'Dell',
    modele: 'Latitude 7520',
    type: 'Ordinateur Portable',
    statut: 'Opérationnel',
    utilisateur: 'Ahmed Benali',
    lieu: 'Siège ADD',
    etage: '3ème étage',
    bureau: 'Bureau 301',
    dateAchat: new Date('2023-03-15'),
    prixAchat: 12500,
    fournisseur: 'TechnoMaroc',
    numeroCommande: 'BC-2024-001',
    dureeGarantie: 36,
    dateFinGarantie: addMonths(new Date('2023-03-15'), 36),
    observations: 'Configuration développeur avec SSD 1TB'
  },
  {
    id: '2',
    codeInventaire: 'INV-IT-2024-002',
    numeroSerie: 'HP45040567',
    designation: 'Ordinateur portable HP ProBook 450',
    marque: 'HP',
    modele: 'ProBook 450',
    type: 'Ordinateur Portable',
    statut: 'Panne',
    utilisateur: 'Fatima Zahra',
    lieu: 'Siège ADD',
    etage: '2ème étage',
    bureau: 'Bureau 205',
    dateAchat: new Date('2022-11-20'),
    prixAchat: 8900,
    fournisseur: 'InfoSupply',
    numeroCommande: 'BC-2023-045',
    dureeGarantie: 24,
    dateFinGarantie: addMonths(new Date('2022-11-20'), 24),
    observations: 'Problème disque dur - En attente SAV'
  },
  {
    id: '3',
    codeInventaire: 'INV-IT-2024-003',
    numeroSerie: 'MBP2023789',
    designation: 'MacBook Pro M2 13 pouces',
    marque: 'Apple',
    modele: 'MacBook Pro M2',
    type: 'Ordinateur Portable',
    statut: 'Opérationnel',
    utilisateur: 'Mohammed Alami',
    lieu: 'Siège ADD',
    etage: '4ème étage',
    bureau: 'Bureau 401',
    dateAchat: new Date('2023-08-10'),
    prixAchat: 16800,
    fournisseur: 'DigitalPro',
    numeroCommande: 'CT-2024-002',
    dureeGarantie: 24,
    dateFinGarantie: addMonths(new Date('2023-08-10'), 24)
  },
  {
    id: '4',
    codeInventaire: 'INV-IT-2024-004',
    numeroSerie: 'SRV-HPE-001',
    designation: 'Serveur HPE ProLiant DL360',
    marque: 'HPE',
    modele: 'ProLiant DL360',
    type: 'Serveur',
    statut: 'Opérationnel',
    lieu: 'Data Center ADD',
    etage: 'Sous-sol',
    bureau: 'Salle serveur A',
    dateAchat: new Date('2023-01-20'),
    prixAchat: 45000,
    fournisseur: 'TechnoMaroc',
    numeroCommande: 'MP-2024-001',
    dureeGarantie: 60,
    dateFinGarantie: addMonths(new Date('2023-01-20'), 60),
    observations: 'Serveur principal bases de données'
  },
  {
    id: '5',
    codeInventaire: 'INV-IT-2024-005',
    numeroSerie: 'MON-DELL-27',
    designation: 'Écran Dell UltraSharp 27 pouces',
    marque: 'Dell',
    modele: 'UltraSharp U2723QE',
    type: 'Écran',
    statut: 'Stock',
    lieu: 'Magasin IT',
    etage: 'Rez-de-chaussée',
    bureau: 'Stock-001',
    dateAchat: new Date('2024-06-15'),
    prixAchat: 3200,
    fournisseur: 'InfoSupply',
    numeroCommande: 'BC-2024-078',
    dureeGarantie: 36,
    dateFinGarantie: addMonths(new Date('2024-06-15'), 36)
  }
];

const mockUtilisateurs = [
  'Ahmed Benali', 'Fatima Zahra', 'Mohammed Alami', 'Khadija Larbi', 'Youssef Tazi', 'Laila Bennani'
];

const mockLieux = [
  'Siège ADD', 'Annexe Rabat', 'Bureau Casablanca', 'Data Center ADD', 'Magasin IT'
];

export const MaterielsIT: React.FC = () => {
  const [materiels, setMateriels] = useState<MaterielIT[]>(mockMaterielsIT);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [typeFilter, setTypeFilter] = useState('all');
  const [lieuFilter, setLieuFilter] = useState('all');
  const [selectedMateriel, setSelectedMateriel] = useState<MaterielIT | null>(null);
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);
  const [isDetailDialogOpen, setIsDetailDialogOpen] = useState(false);

  const filteredMateriels = materiels.filter(mat => {
    const matchesSearch = mat.codeInventaire.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         mat.designation.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         mat.numeroSerie.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         (mat.utilisateur && mat.utilisateur.toLowerCase().includes(searchTerm.toLowerCase()));
    const matchesStatus = statusFilter === 'all' || mat.statut === statusFilter;
    const matchesType = typeFilter === 'all' || mat.type === typeFilter;
    const matchesLieu = lieuFilter === 'all' || mat.lieu === lieuFilter;
    
    return matchesSearch && matchesStatus && matchesType && matchesLieu;
  });

  const getStatutBadge = (statut: string) => {
    switch (statut) {
      case 'Opérationnel':
        return <Badge className="bg-green-500">Opérationnel</Badge>;
      case 'Panne':
        return <Badge variant="destructive">Panne</Badge>;
      case 'Maintenance':
        return <Badge className="bg-orange-500">Maintenance</Badge>;
      case 'Stock':
        return <Badge variant="secondary">Stock</Badge>;
      case 'Réformé':
        return <Badge variant="outline" className="border-red-300 text-red-600">Réformé</Badge>;
      default:
        return <Badge variant="outline">{statut}</Badge>;
    }
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'Ordinateur Portable':
        return <Laptop className="w-4 h-4" />;
      case 'Ordinateur Fixe':
        return <Monitor className="w-4 h-4" />;
      case 'Serveur':
        return <Server className="w-4 h-4" />;
      case 'Écran':
        return <Monitor className="w-4 h-4" />;
      case 'Imprimante':
        return <Monitor className="w-4 h-4" />;
      default:
        return <Monitor className="w-4 h-4" />;
    }
  };

  const getGarantieStatus = (dateFinGarantie: Date) => {
    const joursRestants = differenceInDays(dateFinGarantie, new Date());
    if (joursRestants < 0) {
      return { type: 'expired', label: 'Expirée', color: 'text-red-600', days: Math.abs(joursRestants) };
    } else if (joursRestants <= 30) {
      return { type: 'warning', label: 'Expire bientôt', color: 'text-orange-600', days: joursRestants };
    } else {
      return { type: 'active', label: 'Sous garantie', color: 'text-green-600', days: joursRestants };
    }
  };

  const handleViewDetails = (materiel: MaterielIT) => {
    setSelectedMateriel(materiel);
    setIsDetailDialogOpen(true);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 bg-clip-text text-transparent">
            Matériels Informatiques
          </h1>
          <p className="text-gray-600">Inventaire et gestion des équipements informatiques ADD</p>
        </div>
        
        <Button className="gap-2 bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600">
          <Plus className="w-4 h-4" />
          Ajouter Matériel
        </Button>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
        <Card className="bg-gradient-to-br from-blue-50 to-indigo-50 border-blue-200">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-blue-600">Total équipements</p>
                <p className="text-2xl font-bold text-blue-800">{materiels.length}</p>
              </div>
              <Monitor className="w-8 h-8 text-blue-600" />
            </div>
          </CardContent>
        </Card>
        
        <Card className="bg-gradient-to-br from-green-50 to-emerald-50 border-green-200">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-green-600">Opérationnels</p>
                <p className="text-2xl font-bold text-green-800">
                  {materiels.filter(m => m.statut === 'Opérationnel').length}
                </p>
              </div>
              <CheckCircle className="w-8 h-8 text-green-600" />
            </div>
          </CardContent>
        </Card>
        
        <Card className="bg-gradient-to-br from-red-50 to-pink-50 border-red-200">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-red-600">En panne</p>
                <p className="text-2xl font-bold text-red-800">
                  {materiels.filter(m => m.statut === 'Panne').length}
                </p>
              </div>
              <AlertTriangle className="w-8 h-8 text-red-600" />
            </div>
          </CardContent>
        </Card>
        
        <Card className="bg-gradient-to-br from-orange-50 to-amber-50 border-orange-200">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-orange-600">Garantie expire</p>
                <p className="text-2xl font-bold text-orange-800">
                  {materiels.filter(m => {
                    const status = getGarantieStatus(m.dateFinGarantie);
                    return status.type === 'warning';
                  }).length}
                </p>
              </div>
              <Calendar className="w-8 h-8 text-orange-600" />
            </div>
          </CardContent>
        </Card>
        
        <Card className="bg-gradient-to-br from-purple-50 to-violet-50 border-purple-200">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-purple-600">Valeur totale</p>
                <p className="text-2xl font-bold text-purple-800">
                  {(materiels.reduce((sum, m) => sum + m.prixAchat, 0) / 1000).toFixed(0)}K DH
                </p>
              </div>
              <div className="text-purple-600 font-bold text-lg">💰</div>
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
                placeholder="Rechercher par code, désignation, série ou utilisateur..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-80"
              />
            </div>
            
            <Select value={statusFilter} onValueChange={setStatusFilter}>
              <SelectTrigger className="w-40">
                <SelectValue placeholder="Statut" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Tous les statuts</SelectItem>
                <SelectItem value="Opérationnel">Opérationnel</SelectItem>
                <SelectItem value="Panne">Panne</SelectItem>
                <SelectItem value="Maintenance">Maintenance</SelectItem>
                <SelectItem value="Stock">Stock</SelectItem>
                <SelectItem value="Réformé">Réformé</SelectItem>
              </SelectContent>
            </Select>
            
            <Select value={typeFilter} onValueChange={setTypeFilter}>
              <SelectTrigger className="w-48">
                <SelectValue placeholder="Type" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Tous les types</SelectItem>
                <SelectItem value="Ordinateur Portable">Ordinateur Portable</SelectItem>
                <SelectItem value="Ordinateur Fixe">Ordinateur Fixe</SelectItem>
                <SelectItem value="Serveur">Serveur</SelectItem>
                <SelectItem value="Écran">Écran</SelectItem>
                <SelectItem value="Imprimante">Imprimante</SelectItem>
                <SelectItem value="Réseau">Réseau</SelectItem>
              </SelectContent>
            </Select>

            <Select value={lieuFilter} onValueChange={setLieuFilter}>
              <SelectTrigger className="w-40">
                <SelectValue placeholder="Lieu" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Tous les lieux</SelectItem>
                {mockLieux.map(lieu => (
                  <SelectItem key={lieu} value={lieu}>{lieu}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      {/* Table */}
      <Card>
        <CardHeader>
          <CardTitle>Inventaire des matériels IT ({filteredMateriels.length})</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Code inventaire</TableHead>
                <TableHead>Équipement</TableHead>
                <TableHead>N° Série</TableHead>
                <TableHead>Statut</TableHead>
                <TableHead>Utilisateur</TableHead>
                <TableHead>Lieu</TableHead>
                <TableHead>Garantie</TableHead>
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredMateriels.map((materiel) => {
                const garantieStatus = getGarantieStatus(materiel.dateFinGarantie);
                return (
                  <TableRow key={materiel.id}>
                    <TableCell className="font-mono text-sm font-medium">
                      {materiel.codeInventaire}
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center gap-3">
                        {getTypeIcon(materiel.type)}
                        <div>
                          <div className="font-medium">{materiel.designation}</div>
                          <div className="text-sm text-gray-500">{materiel.marque} {materiel.modele}</div>
                        </div>
                      </div>
                    </TableCell>
                    <TableCell className="font-mono text-sm">{materiel.numeroSerie}</TableCell>
                    <TableCell>{getStatutBadge(materiel.statut)}</TableCell>
                    <TableCell>
                      {materiel.utilisateur ? (
                        <div className="flex items-center gap-2">
                          <Avatar className="w-6 h-6">
                            <AvatarFallback className="text-xs">
                              {materiel.utilisateur.split(' ').map(n => n[0]).join('')}
                            </AvatarFallback>
                          </Avatar>
                          <span className="text-sm">{materiel.utilisateur}</span>
                        </div>
                      ) : (
                        <span className="text-gray-400 text-sm">Non affecté</span>
                      )}
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center gap-1 text-sm">
                        <MapPin className="w-3 h-3 text-gray-400" />
                        <div>
                          <div>{materiel.lieu}</div>
                          {materiel.bureau && (
                            <div className="text-xs text-gray-500">{materiel.bureau}</div>
                          )}
                        </div>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className={`text-sm ${garantieStatus.color}`}>
                        <div>{garantieStatus.label}</div>
                        <div className="text-xs text-gray-500">
                          {garantieStatus.type === 'expired' ? 
                            `Expirée depuis ${garantieStatus.days}j` :
                            `${garantieStatus.days} jours`
                          }
                        </div>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="flex gap-1">
                        <Button 
                          variant="ghost" 
                          size="icon"
                          onClick={() => handleViewDetails(materiel)}
                        >
                          <Eye className="w-4 h-4" />
                        </Button>
                        <Button variant="ghost" size="icon">
                          <Edit className="w-4 h-4" />
                        </Button>
                        <Button variant="ghost" size="icon">
                          <Settings className="w-4 h-4" />
                        </Button>
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
              {selectedMateriel && getTypeIcon(selectedMateriel.type)}
              Détail du matériel {selectedMateriel?.codeInventaire}
            </DialogTitle>
          </DialogHeader>
          
          {selectedMateriel && (
            <Tabs defaultValue="general" className="w-full">
              <TabsList className="grid w-full grid-cols-4">
                <TabsTrigger value="general">Général</TabsTrigger>
                <TabsTrigger value="affectation">Affectation</TabsTrigger>
                <TabsTrigger value="garantie">Garantie</TabsTrigger>
                <TabsTrigger value="historique">Historique</TabsTrigger>
              </TabsList>
              
              <TabsContent value="general" className="space-y-6">
                <div className="grid grid-cols-2 gap-6">
                  <div className="space-y-4">
                    <div>
                      <Label className="text-sm text-gray-500">Code inventaire</Label>
                      <p className="font-mono font-medium">{selectedMateriel.codeInventaire}</p>
                    </div>
                    <div>
                      <Label className="text-sm text-gray-500">Numéro de série</Label>
                      <p className="font-mono">{selectedMateriel.numeroSerie}</p>
                    </div>
                    <div>
                      <Label className="text-sm text-gray-500">Désignation</Label>
                      <p className="font-medium">{selectedMateriel.designation}</p>
                    </div>
                    <div>
                      <Label className="text-sm text-gray-500">Marque & Modèle</Label>
                      <p>{selectedMateriel.marque} {selectedMateriel.modele}</p>
                    </div>
                    <div>
                      <Label className="text-sm text-gray-500">Type</Label>
                      <div className="flex items-center gap-2">
                        {getTypeIcon(selectedMateriel.type)}
                        <span>{selectedMateriel.type}</span>
                      </div>
                    </div>
                  </div>
                  
                  <div className="space-y-4">
                    <div>
                      <Label className="text-sm text-gray-500">Statut</Label>
                      <div>{getStatutBadge(selectedMateriel.statut)}</div>
                    </div>
                    <div>
                      <Label className="text-sm text-gray-500">Date d'achat</Label>
                      <p>{format(selectedMateriel.dateAchat, 'dd MMMM yyyy', { locale: fr })}</p>
                    </div>
                    <div>
                      <Label className="text-sm text-gray-500">Prix d'achat</Label>
                      <p className="font-bold text-lg">{selectedMateriel.prixAchat.toLocaleString()} DH</p>
                    </div>
                    <div>
                      <Label className="text-sm text-gray-500">Fournisseur</Label>
                      <p>{selectedMateriel.fournisseur}</p>
                    </div>
                    <div>
                      <Label className="text-sm text-gray-500">N° Commande</Label>
                      <p className="font-mono">{selectedMateriel.numeroCommande}</p>
                    </div>
                  </div>
                </div>
                
                {selectedMateriel.observations && (
                  <div>
                    <Label className="text-sm text-gray-500">Observations</Label>
                    <p className="mt-1 p-3 bg-gray-50 rounded-lg">{selectedMateriel.observations}</p>
                  </div>
                )}
              </TabsContent>
              
              <TabsContent value="affectation" className="space-y-4">
                <div className="grid grid-cols-2 gap-6">
                  <div className="space-y-4">
                    <div>
                      <Label className="text-sm text-gray-500">Utilisateur affecté</Label>
                      {selectedMateriel.utilisateur ? (
                        <div className="flex items-center gap-3 mt-2">
                          <Avatar>
                            <AvatarFallback>
                              {selectedMateriel.utilisateur.split(' ').map(n => n[0]).join('')}
                            </AvatarFallback>
                          </Avatar>
                          <div>
                            <p className="font-medium">{selectedMateriel.utilisateur}</p>
                            <p className="text-sm text-gray-500">Développeur Senior</p>
                          </div>
                        </div>
                      ) : (
                        <p className="text-gray-400">Non affecté</p>
                      )}
                    </div>
                  </div>
                  
                  <div className="space-y-4">
                    <div>
                      <Label className="text-sm text-gray-500">Localisation</Label>
                      <div className="space-y-2 mt-2">
                        <div className="flex items-center gap-2">
                          <MapPin className="w-4 h-4 text-gray-400" />
                          <span>{selectedMateriel.lieu}</span>
                        </div>
                        {selectedMateriel.etage && (
                          <div className="text-sm text-gray-600 ml-6">{selectedMateriel.etage}</div>
                        )}
                        {selectedMateriel.bureau && (
                          <div className="text-sm text-gray-600 ml-6">{selectedMateriel.bureau}</div>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              </TabsContent>
              
              <TabsContent value="garantie" className="space-y-4">
                {(() => {
                  const garantieStatus = getGarantieStatus(selectedMateriel.dateFinGarantie);
                  const progressValue = Math.max(0, Math.min(100, 
                    100 - (differenceInDays(selectedMateriel.dateFinGarantie, selectedMateriel.dateAchat) - garantieStatus.days) / 
                    differenceInDays(selectedMateriel.dateFinGarantie, selectedMateriel.dateAchat) * 100
                  ));
                  
                  return (
                    <div className="space-y-6">
                      <div className="grid grid-cols-2 gap-6">
                        <div>
                          <Label className="text-sm text-gray-500">Durée de garantie</Label>
                          <p className="text-lg font-medium">{selectedMateriel.dureeGarantie} mois</p>
                        </div>
                        <div>
                          <Label className="text-sm text-gray-500">Date de fin de garantie</Label>
                          <p className="text-lg font-medium">
                            {format(selectedMateriel.dateFinGarantie, 'dd MMMM yyyy', { locale: fr })}
                          </p>
                        </div>
                      </div>
                      
                      <div>
                        <div className="flex items-center justify-between mb-2">
                          <Label className="text-sm text-gray-500">Statut de la garantie</Label>
                          <Badge className={
                            garantieStatus.type === 'active' ? 'bg-green-500' :
                            garantieStatus.type === 'warning' ? 'bg-orange-500' : 'bg-red-500'
                          }>
                            {garantieStatus.label}
                          </Badge>
                        </div>
                        <Progress value={progressValue} className="h-3" />
                        <p className="text-sm text-gray-600 mt-2">
                          {garantieStatus.type === 'expired' ? 
                            `Garantie expirée depuis ${garantieStatus.days} jours` :
                            `${garantieStatus.days} jours restants`
                          }
                        </p>
                      </div>
                      
                      {garantieStatus.type === 'warning' && (
                        <div className="p-4 bg-orange-50 border border-orange-200 rounded-lg">
                          <div className="flex items-center gap-2">
                            <AlertTriangle className="w-5 h-5 text-orange-600" />
                            <span className="font-medium text-orange-800">Attention</span>
                          </div>
                          <p className="text-sm text-orange-700 mt-1">
                            La garantie de cet équipement expire dans moins de 30 jours. 
                            Pensez à renouveler ou planifier un remplacement.
                          </p>
                        </div>
                      )}
                    </div>
                  );
                })()}
              </TabsContent>
              
              <TabsContent value="historique" className="space-y-4">
                <div className="space-y-4">
                  <div className="flex items-center gap-3 p-3 bg-blue-50 rounded-lg">
                    <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                    <div className="flex-1">
                      <p className="text-sm font-medium">Matériel créé dans l'inventaire</p>
                      <p className="text-xs text-gray-500">
                        {format(selectedMateriel.dateAchat, 'dd MMMM yyyy à HH:mm', { locale: fr })} • Système
                      </p>
                    </div>
                  </div>
                  
                  {selectedMateriel.utilisateur && (
                    <div className="flex items-center gap-3 p-3 bg-green-50 rounded-lg">
                      <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                      <div className="flex-1">
                        <p className="text-sm font-medium">Affecté à {selectedMateriel.utilisateur}</p>
                        <p className="text-xs text-gray-500">
                          15 mars 2024 à 14:30 • Ahmed Benali (Gestionnaire IT)
                        </p>
                      </div>
                    </div>
                  )}
                  
                  {selectedMateriel.statut === 'Panne' && (
                    <div className="flex items-center gap-3 p-3 bg-red-50 rounded-lg">
                      <div className="w-2 h-2 bg-red-500 rounded-full"></div>
                      <div className="flex-1">
                        <p className="text-sm font-medium">Signalement de panne</p>
                        <p className="text-xs text-gray-500">
                          20 juillet 2024 à 09:15 • {selectedMateriel.utilisateur}
                        </p>
                        <p className="text-xs text-gray-600 mt-1">
                          {selectedMateriel.observations}
                        </p>
                      </div>
                    </div>
                  )}
                </div>
              </TabsContent>
            </Tabs>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
};