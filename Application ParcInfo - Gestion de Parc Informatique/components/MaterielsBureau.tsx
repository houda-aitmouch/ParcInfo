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
  Plus, 
  Eye, 
  Edit, 
  Printer, 
  ScanLine,
  User,
  MapPin,
  Calendar,
  AlertTriangle,
  CheckCircle,
  Settings,
  Armchair,
  FileText
} from 'lucide-react';
import { format, differenceInDays, addMonths } from 'date-fns';
import { fr } from 'date-fns/locale';

interface MaterielBureau {
  id: string;
  codeInventaire: string;
  numeroSerie?: string;
  designation: string;
  marque: string;
  modele: string;
  type: 'Imprimante' | 'Scanner' | 'Photocopieur' | 'Mobilier' | 'Fournitures' | 'Projecteur';
  statut: 'Opérationnel' | 'Panne' | 'Maintenance' | 'Stock' | 'Réformé';
  utilisateur?: string;
  service?: string;
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

const mockMaterielsBureau: MaterielBureau[] = [
  {
    id: '1',
    codeInventaire: 'INV-BUR-2024-001',
    numeroSerie: 'HP-LJ-P3015',
    designation: 'Imprimante laser HP LaserJet P3015',
    marque: 'HP',
    modele: 'LaserJet P3015',
    type: 'Imprimante',
    statut: 'Opérationnel',
    utilisateur: 'Service Comptabilité',
    service: 'Comptabilité',
    lieu: 'Siège ADD',
    etage: '1er étage',
    bureau: 'Salle commune',
    dateAchat: new Date('2023-05-15'),
    prixAchat: 4500,
    fournisseur: 'BureauExpert',
    numeroCommande: 'BC-BUR-2023-015',
    dureeGarantie: 24,
    dateFinGarantie: addMonths(new Date('2023-05-15'), 24),
    observations: 'Imprimante partagée pour le service comptabilité'
  },
  {
    id: '2',
    codeInventaire: 'INV-BUR-2024-002',
    numeroSerie: 'EP-SC-T3100',
    designation: 'Scanner Epson ScanSmart',
    marque: 'Epson',
    modele: 'ScanSmart T3100',
    type: 'Scanner',
    statut: 'Opérationnel',
    utilisateur: 'Fatima Zahra',
    service: 'RH',
    lieu: 'Siège ADD',
    etage: '2ème étage',
    bureau: 'Bureau RH-201',
    dateAchat: new Date('2023-09-10'),
    prixAchat: 2800,
    fournisseur: 'OfficeSupply',
    numeroCommande: 'BC-BUR-2023-045',
    dureeGarantie: 12,
    dateFinGarantie: addMonths(new Date('2023-09-10'), 12)
  },
  {
    id: '3',
    codeInventaire: 'INV-BUR-2024-003',
    designation: 'Photocopieur multifonction Canon',
    marque: 'Canon',
    modele: 'imageRUNNER ADVANCE C3520i',
    type: 'Photocopieur',
    statut: 'Maintenance',
    service: 'Général',
    lieu: 'Siège ADD',
    etage: 'Rez-de-chaussée',
    bureau: 'Hall principal',
    dateAchat: new Date('2022-12-20'),
    prixAchat: 25000,
    fournisseur: 'MobilierPro',
    numeroCommande: 'CT-BUR-2022-008',
    dureeGarantie: 36,
    dateFinGarantie: addMonths(new Date('2022-12-20'), 36),
    observations: 'En cours de réparation - Problème tambour'
  },
  {
    id: '4',
    codeInventaire: 'INV-BUR-2024-004',
    designation: 'Bureau ergonomique réglable',
    marque: 'Steelcase',
    modele: 'Series 1 Sit-to-Stand',
    type: 'Mobilier',
    statut: 'Opérationnel',
    utilisateur: 'Mohammed Alami',
    service: 'Développement',
    lieu: 'Siège ADD',
    etage: '4ème étage',
    bureau: 'Bureau 401',
    dateAchat: new Date('2024-01-15'),
    prixAchat: 8500,
    fournisseur: 'MobilierPro',
    numeroCommande: 'BC-BUR-2024-001',
    dureeGarantie: 60,
    dateFinGarantie: addMonths(new Date('2024-01-15'), 60),
    observations: 'Bureau avec hauteur réglable électriquement'
  },
  {
    id: '5',
    codeInventaire: 'INV-BUR-2024-005',
    numeroSerie: 'EP-EB-2247U',
    designation: 'Projecteur Epson EB-2247U',
    marque: 'Epson',
    modele: 'EB-2247U',
    type: 'Projecteur',
    statut: 'Stock',
    lieu: 'Magasin Bureautique',
    etage: 'Rez-de-chaussée',
    bureau: 'Stock-BUR-001',
    dateAchat: new Date('2024-06-20'),
    prixAchat: 12000,
    fournisseur: 'BureauExpert',
    numeroCommande: 'BC-BUR-2024-078',
    dureeGarantie: 24,
    dateFinGarantie: addMonths(new Date('2024-06-20'), 24),
    observations: 'Projecteur portable pour salles de réunion'
  }
];

export const MaterielsBureau: React.FC = () => {
  const [materiels, setMateriels] = useState<MaterielBureau[]>(mockMaterielsBureau);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [typeFilter, setTypeFilter] = useState('all');
  const [serviceFilter, setServiceFilter] = useState('all');
  const [selectedMateriel, setSelectedMateriel] = useState<MaterielBureau | null>(null);
  const [isDetailDialogOpen, setIsDetailDialogOpen] = useState(false);

  const services = ['Comptabilité', 'RH', 'Développement', 'Direction', 'Communication', 'Général'];

  const filteredMateriels = materiels.filter(mat => {
    const matchesSearch = mat.codeInventaire.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         mat.designation.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         (mat.numeroSerie && mat.numeroSerie.toLowerCase().includes(searchTerm.toLowerCase())) ||
                         (mat.utilisateur && mat.utilisateur.toLowerCase().includes(searchTerm.toLowerCase()));
    const matchesStatus = statusFilter === 'all' || mat.statut === statusFilter;
    const matchesType = typeFilter === 'all' || mat.type === typeFilter;
    const matchesService = serviceFilter === 'all' || mat.service === serviceFilter;
    
    return matchesSearch && matchesStatus && matchesType && matchesService;
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
      case 'Imprimante':
        return <Printer className="w-4 h-4" />;
      case 'Scanner':
        return <ScanLine className="w-4 h-4" />;
      case 'Photocopieur':
        return <FileText className="w-4 h-4" />;
      case 'Mobilier':
        return <Armchair className="w-4 h-4" />;
      case 'Projecteur':
        return <Settings className="w-4 h-4" />;
      default:
        return <Settings className="w-4 h-4" />;
    }
  };

  const getTypeBadge = (type: string) => {
    const colors = {
      'Imprimante': 'bg-blue-100 text-blue-800 border-blue-200',
      'Scanner': 'bg-green-100 text-green-800 border-green-200',
      'Photocopieur': 'bg-purple-100 text-purple-800 border-purple-200',
      'Mobilier': 'bg-orange-100 text-orange-800 border-orange-200',
      'Projecteur': 'bg-pink-100 text-pink-800 border-pink-200',
      'Fournitures': 'bg-gray-100 text-gray-800 border-gray-200'
    };
    return <Badge variant="outline" className={colors[type as keyof typeof colors] || 'bg-gray-100 text-gray-800'}>{type}</Badge>;
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

  const handleViewDetails = (materiel: MaterielBureau) => {
    setSelectedMateriel(materiel);
    setIsDetailDialogOpen(true);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold bg-gradient-to-r from-purple-600 via-pink-600 to-rose-600 bg-clip-text text-transparent">
            Matériels Bureautiques
          </h1>
          <p className="text-gray-600">Inventaire et gestion des équipements bureautiques ADD</p>
        </div>
        
        <Button className="gap-2 bg-gradient-to-r from-purple-600 via-pink-600 to-rose-600">
          <Plus className="w-4 h-4" />
          Ajouter Matériel
        </Button>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
        <Card className="bg-gradient-to-br from-purple-50 to-pink-50 border-purple-200">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-purple-600">Total équipements</p>
                <p className="text-2xl font-bold text-purple-800">{materiels.length}</p>
              </div>
              <Printer className="w-8 h-8 text-purple-600" />
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
                <p className="text-sm text-red-600">En maintenance</p>
                <p className="text-2xl font-bold text-red-800">
                  {materiels.filter(m => m.statut === 'Maintenance' || m.statut === 'Panne').length}
                </p>
              </div>
              <Settings className="w-8 h-8 text-red-600" />
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
        
        <Card className="bg-gradient-to-br from-blue-50 to-cyan-50 border-blue-200">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-blue-600">Valeur totale</p>
                <p className="text-2xl font-bold text-blue-800">
                  {(materiels.reduce((sum, m) => sum + m.prixAchat, 0) / 1000).toFixed(0)}K DH
                </p>
              </div>
              <div className="text-blue-600 font-bold text-lg">💰</div>
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
                placeholder="Rechercher par code, désignation ou utilisateur..."
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
                <SelectItem value="Imprimante">Imprimante</SelectItem>
                <SelectItem value="Scanner">Scanner</SelectItem>
                <SelectItem value="Photocopieur">Photocopieur</SelectItem>
                <SelectItem value="Mobilier">Mobilier</SelectItem>
                <SelectItem value="Projecteur">Projecteur</SelectItem>
                <SelectItem value="Fournitures">Fournitures</SelectItem>
              </SelectContent>
            </Select>

            <Select value={serviceFilter} onValueChange={setServiceFilter}>
              <SelectTrigger className="w-40">
                <SelectValue placeholder="Service" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Tous les services</SelectItem>
                {services.map(service => (
                  <SelectItem key={service} value={service}>{service}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      {/* Table */}
      <Card>
        <CardHeader>
          <CardTitle>Inventaire des matériels bureautiques ({filteredMateriels.length})</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Code inventaire</TableHead>
                <TableHead>Équipement</TableHead>
                <TableHead>Type</TableHead>
                <TableHead>Statut</TableHead>
                <TableHead>Affectation</TableHead>
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
                    <TableCell>{getTypeBadge(materiel.type)}</TableCell>
                    <TableCell>{getStatutBadge(materiel.statut)}</TableCell>
                    <TableCell>
                      {materiel.utilisateur ? (
                        <div>
                          <div className="font-medium text-sm">{materiel.utilisateur}</div>
                          {materiel.service && (
                            <div className="text-xs text-gray-500">{materiel.service}</div>
                          )}
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
              <TabsList className="grid w-full grid-cols-3">
                <TabsTrigger value="general">Général</TabsTrigger>
                <TabsTrigger value="affectation">Affectation</TabsTrigger>
                <TabsTrigger value="garantie">Garantie</TabsTrigger>
              </TabsList>
              
              <TabsContent value="general" className="space-y-6">
                <div className="grid grid-cols-2 gap-6">
                  <div className="space-y-4">
                    <div>
                      <Label className="text-sm text-gray-500">Code inventaire</Label>
                      <p className="font-mono font-medium">{selectedMateriel.codeInventaire}</p>
                    </div>
                    {selectedMateriel.numeroSerie && (
                      <div>
                        <Label className="text-sm text-gray-500">Numéro de série</Label>
                        <p className="font-mono">{selectedMateriel.numeroSerie}</p>
                      </div>
                    )}
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
                      <Label className="text-sm text-gray-500">Affectation</Label>
                      {selectedMateriel.utilisateur ? (
                        <div className="mt-2">
                          <p className="font-medium">{selectedMateriel.utilisateur}</p>
                          {selectedMateriel.service && (
                            <p className="text-sm text-gray-500">Service {selectedMateriel.service}</p>
                          )}
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
                          </p>
                        </div>
                      )}
                    </div>
                  );
                })()}
              </TabsContent>
            </Tabs>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
};