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
import { Search, Filter, Plus, Eye, Edit, Trash2, FileText, Download, Printer } from 'lucide-react';
import { format } from 'date-fns';
import { fr } from 'date-fns/locale';

interface CommandeBureau {
  id: string;
  numero: string;
  dateCommande: Date;
  fournisseur: string;
  modePassation: 'BC' | 'Contrat' | 'Marché';
  montantHT: number;
  numeroFacture?: string;
  dateReception?: Date;
  statut: 'En attente' | 'Commandé' | 'Reçu' | 'Facturé' | 'Payé';
  dureeGarantie: number;
  uniteGarantie: 'mois' | 'années';
  typeEquipement: 'Imprimante' | 'Scanner' | 'Photocopieur' | 'Mobilier' | 'Fournitures';
}

const mockCommandesBureau: CommandeBureau[] = [
  {
    id: '1',
    numero: 'BC-BUR-2024-001',
    dateCommande: new Date('2024-07-10'),
    fournisseur: 'BureauExpert',
    modePassation: 'BC',
    montantHT: 45000,
    numeroFacture: 'FB-2024-001',
    dateReception: new Date('2024-07-15'),
    statut: 'Payé',
    dureeGarantie: 12,
    uniteGarantie: 'mois',
    typeEquipement: 'Imprimante'
  },
  {
    id: '2',
    numero: 'CT-BUR-2024-002',
    dateCommande: new Date('2024-07-12'),
    fournisseur: 'OfficeSupply',
    modePassation: 'Contrat',
    montantHT: 67500,
    numeroFacture: 'FB-2024-002',
    statut: 'Facturé',
    dureeGarantie: 24,
    uniteGarantie: 'mois',
    typeEquipement: 'Photocopieur'
  },
  {
    id: '3',
    numero: 'MP-BUR-2024-001',
    dateCommande: new Date('2024-07-18'),
    fournisseur: 'MobilierPro',
    modePassation: 'Marché',
    montantHT: 89000,
    statut: 'Commandé',
    dureeGarantie: 60,
    uniteGarantie: 'mois',
    typeEquipement: 'Mobilier'
  }
];

const mockFournisseursBureau = [
  'BureauExpert', 'OfficeSupply', 'MobilierPro', 'PrintSolutions', 'FournituresPlus'
];

export const CommandesBureau: React.FC = () => {
  const [commandes, setCommandes] = useState<CommandeBureau[]>(mockCommandesBureau);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [typeFilter, setTypeFilter] = useState('all');
  const [selectedCommande, setSelectedCommande] = useState<CommandeBureau | null>(null);
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);
  const [newCommande, setNewCommande] = useState<Partial<CommandeBureau>>({
    modePassation: 'BC',
    dureeGarantie: 12,
    uniteGarantie: 'mois',
    statut: 'En attente',
    typeEquipement: 'Imprimante'
  });

  const filteredCommandes = commandes.filter(cmd => {
    const matchesSearch = cmd.numero.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         cmd.fournisseur.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = statusFilter === 'all' || cmd.statut === statusFilter;
    const matchesType = typeFilter === 'all' || cmd.typeEquipement === typeFilter;
    
    return matchesSearch && matchesStatus && matchesType;
  });

  const getStatusBadge = (statut: string) => {
    switch (statut) {
      case 'En attente':
        return <Badge variant="secondary">En attente</Badge>;
      case 'Commandé':
        return <Badge className="bg-purple-500">Commandé</Badge>;
      case 'Reçu':
        return <Badge variant="outline">Reçu</Badge>;
      case 'Facturé':
        return <Badge className="bg-orange-500">Facturé</Badge>;
      case 'Payé':
        return <Badge className="bg-green-500">Payé</Badge>;
      default:
        return <Badge variant="outline">{statut}</Badge>;
    }
  };

  const getTypeBadge = (type: string) => {
    const colors = {
      'Imprimante': 'bg-blue-100 text-blue-800',
      'Scanner': 'bg-green-100 text-green-800', 
      'Photocopieur': 'bg-purple-100 text-purple-800',
      'Mobilier': 'bg-orange-100 text-orange-800',
      'Fournitures': 'bg-gray-100 text-gray-800'
    };
    return <Badge className={colors[type as keyof typeof colors] || 'bg-gray-100 text-gray-800'}>{type}</Badge>;
  };

  const handleCreateCommande = () => {
    const numeroPrefix = newCommande.modePassation === 'BC' ? 'BC-BUR' : 
                        newCommande.modePassation === 'Contrat' ? 'CT-BUR' : 'MP-BUR';
    const numero = `${numeroPrefix}-2024-${String(commandes.length + 1).padStart(3, '0')}`;
    
    const commande: CommandeBureau = {
      id: String(Date.now()),
      numero,
      dateCommande: new Date(),
      fournisseur: newCommande.fournisseur || '',
      modePassation: newCommande.modePassation || 'BC',
      montantHT: newCommande.montantHT || 0,
      statut: 'En attente',
      dureeGarantie: newCommande.dureeGarantie || 12,
      uniteGarantie: newCommande.uniteGarantie || 'mois',
      typeEquipement: newCommande.typeEquipement || 'Imprimante'
    };

    setCommandes([...commandes, commande]);
    setIsCreateDialogOpen(false);
    setNewCommande({
      modePassation: 'BC',
      dureeGarantie: 12,
      uniteGarantie: 'mois',
      statut: 'En attente',
      typeEquipement: 'Imprimante'
    });
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold bg-gradient-to-r from-purple-600 via-pink-600 to-rose-600 bg-clip-text text-transparent">
            Commandes Bureautiques
          </h1>
          <p className="text-gray-600">Gestion des bons de commande, contrats et marchés bureautiques</p>
        </div>
        
        <Dialog open={isCreateDialogOpen} onOpenChange={setIsCreateDialogOpen}>
          <DialogTrigger asChild>
            <Button className="gap-2 bg-gradient-to-r from-purple-600 via-pink-600 to-rose-600">
              <Plus className="w-4 h-4" />
              Nouvelle Commande
            </Button>
          </DialogTrigger>
          <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
            <DialogHeader>
              <DialogTitle>Créer une nouvelle commande bureautique</DialogTitle>
              <DialogDescription>
                Remplissez les informations de la commande bureautique
              </DialogDescription>
            </DialogHeader>
            
            <div className="grid grid-cols-2 gap-4 py-4">
              <div className="space-y-2">
                <Label htmlFor="mode">Mode de passation</Label>
                <Select value={newCommande.modePassation} onValueChange={(value) => 
                  setNewCommande({...newCommande, modePassation: value as 'BC' | 'Contrat' | 'Marché'})
                }>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="BC">Bon de Commande</SelectItem>
                    <SelectItem value="Contrat">Contrat</SelectItem>
                    <SelectItem value="Marché">Marché Public</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="typeEquipement">Type d'équipement</Label>
                <Select value={newCommande.typeEquipement} onValueChange={(value) => 
                  setNewCommande({...newCommande, typeEquipement: value as any})
                }>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="Imprimante">Imprimante</SelectItem>
                    <SelectItem value="Scanner">Scanner</SelectItem>
                    <SelectItem value="Photocopieur">Photocopieur</SelectItem>
                    <SelectItem value="Mobilier">Mobilier</SelectItem>
                    <SelectItem value="Fournitures">Fournitures</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="fournisseur">Fournisseur</Label>
                <Select value={newCommande.fournisseur} onValueChange={(value) => 
                  setNewCommande({...newCommande, fournisseur: value})
                }>
                  <SelectTrigger>
                    <SelectValue placeholder="Sélectionner un fournisseur" />
                  </SelectTrigger>
                  <SelectContent>
                    {mockFournisseursBureau.map(fournisseur => (
                      <SelectItem key={fournisseur} value={fournisseur}>{fournisseur}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="montant">Montant HT (DH)</Label>
                <Input
                  type="number"
                  value={newCommande.montantHT || ''}
                  onChange={(e) => setNewCommande({...newCommande, montantHT: Number(e.target.value)})}
                  placeholder="0"
                />
              </div>

              <div className="col-span-2 space-y-2">
                <Label>Durée de garantie</Label>
                <div className="flex gap-2">
                  <Input
                    type="number"
                    value={newCommande.dureeGarantie || ''}
                    onChange={(e) => setNewCommande({...newCommande, dureeGarantie: Number(e.target.value)})}
                    placeholder="12"
                    className="w-20"
                  />
                  <Select value={newCommande.uniteGarantie} onValueChange={(value) => 
                    setNewCommande({...newCommande, uniteGarantie: value as 'mois' | 'années'})
                  }>
                    <SelectTrigger className="w-24">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="mois">mois</SelectItem>
                      <SelectItem value="années">années</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div className="col-span-2 space-y-2">
                <Label htmlFor="description">Description / Notes</Label>
                <Textarea
                  placeholder="Description des équipements ou notes complémentaires..."
                  className="min-h-20"
                />
              </div>
            </div>

            <div className="flex justify-end gap-2">
              <Button variant="outline" onClick={() => setIsCreateDialogOpen(false)}>
                Annuler
              </Button>
              <Button onClick={handleCreateCommande} className="bg-gradient-to-r from-purple-600 via-pink-600 to-rose-600">
                Créer la commande
              </Button>
            </div>
          </DialogContent>
        </Dialog>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="bg-gradient-to-br from-purple-50 to-pink-50 border-purple-200">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-purple-600">Commandes totales</p>
                <p className="text-2xl font-bold text-purple-800">{commandes.length}</p>
              </div>
              <Printer className="w-8 h-8 text-purple-600" />
            </div>
          </CardContent>
        </Card>
        
        <Card className="bg-gradient-to-br from-orange-50 to-red-50 border-orange-200">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-orange-600">En attente</p>
                <p className="text-2xl font-bold text-orange-800">
                  {commandes.filter(c => c.statut === 'En attente').length}
                </p>
              </div>
              <Badge variant="secondary" className="text-lg p-2 bg-orange-100 text-orange-600">!</Badge>
            </div>
          </CardContent>
        </Card>
        
        <Card className="bg-gradient-to-br from-green-50 to-emerald-50 border-green-200">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-green-600">Montant total</p>
                <p className="text-2xl font-bold text-green-800">
                  {commandes.reduce((sum, c) => sum + c.montantHT, 0).toLocaleString()} DH
                </p>
              </div>
              <div className="text-green-600 font-bold text-lg">💰</div>
            </div>
          </CardContent>
        </Card>
        
        <Card className="bg-gradient-to-br from-blue-50 to-indigo-50 border-blue-200">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-blue-600">Payées</p>
                <p className="text-2xl font-bold text-blue-800">
                  {commandes.filter(c => c.statut === 'Payé').length}
                </p>
              </div>
              <Badge variant="default" className="bg-blue-500 text-lg p-2">✓</Badge>
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
                placeholder="Rechercher par numéro ou fournisseur..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-64"
              />
            </div>
            
            <Select value={statusFilter} onValueChange={setStatusFilter}>
              <SelectTrigger className="w-40">
                <SelectValue placeholder="Statut" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Tous les statuts</SelectItem>
                <SelectItem value="En attente">En attente</SelectItem>
                <SelectItem value="Commandé">Commandé</SelectItem>
                <SelectItem value="Reçu">Reçu</SelectItem>
                <SelectItem value="Facturé">Facturé</SelectItem>
                <SelectItem value="Payé">Payé</SelectItem>
              </SelectContent>
            </Select>
            
            <Select value={typeFilter} onValueChange={setTypeFilter}>
              <SelectTrigger className="w-40">
                <SelectValue placeholder="Type" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Tous les types</SelectItem>
                <SelectItem value="Imprimante">Imprimante</SelectItem>
                <SelectItem value="Scanner">Scanner</SelectItem>
                <SelectItem value="Photocopieur">Photocopieur</SelectItem>
                <SelectItem value="Mobilier">Mobilier</SelectItem>
                <SelectItem value="Fournitures">Fournitures</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      {/* Table */}
      <Card>
        <CardHeader>
          <CardTitle>Liste des commandes bureautiques ({filteredCommandes.length})</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>N° Commande</TableHead>
                <TableHead>Date</TableHead>
                <TableHead>Fournisseur</TableHead>
                <TableHead>Type</TableHead>
                <TableHead>Montant HT</TableHead>
                <TableHead>N° Facture</TableHead>
                <TableHead>Statut</TableHead>
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredCommandes.map((commande) => (
                <TableRow key={commande.id}>
                  <TableCell className="font-medium">{commande.numero}</TableCell>
                  <TableCell>
                    {format(commande.dateCommande, 'dd MMM yyyy', { locale: fr })}
                  </TableCell>
                  <TableCell>{commande.fournisseur}</TableCell>
                  <TableCell>{getTypeBadge(commande.typeEquipement)}</TableCell>
                  <TableCell>{commande.montantHT.toLocaleString()} DH</TableCell>
                  <TableCell className="font-mono text-sm">
                    {commande.numeroFacture || '-'}
                  </TableCell>
                  <TableCell>{getStatusBadge(commande.statut)}</TableCell>
                  <TableCell>
                    <div className="flex gap-1">
                      <Button variant="ghost" size="icon">
                        <Eye className="w-4 h-4" />
                      </Button>
                      <Button variant="ghost" size="icon">
                        <Edit className="w-4 h-4" />
                      </Button>
                      <Button variant="ghost" size="icon">
                        <Trash2 className="w-4 h-4" />
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
};