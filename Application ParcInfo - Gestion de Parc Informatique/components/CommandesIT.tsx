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
import { Calendar } from './ui/calendar';
import { Popover, PopoverContent, PopoverTrigger } from './ui/popover';
import { CalendarIcon, Search, Filter, Plus, Eye, Edit, Trash2, FileText, Download } from 'lucide-react';
import { format } from 'date-fns';
import { fr } from 'date-fns/locale';

interface Commande {
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
}

const mockCommandes: Commande[] = [
  {
    id: '1',
    numero: 'BC-2024-001',
    dateCommande: new Date('2024-07-15'),
    fournisseur: 'TechnoMaroc',
    modePassation: 'BC',
    montantHT: 125000,
    numeroFacture: 'F-2024-001',
    dateReception: new Date('2024-07-20'),
    statut: 'Payé',
    dureeGarantie: 24,
    uniteGarantie: 'mois'
  },
  {
    id: '2',
    numero: 'CT-2024-002',
    dateCommande: new Date('2024-07-18'),
    fournisseur: 'InfoSupply',
    modePassation: 'Contrat',
    montantHT: 89500,
    numeroFacture: 'F-2024-002',
    statut: 'Facturé',
    dureeGarantie: 36,
    uniteGarantie: 'mois'
  },
  {
    id: '3',
    numero: 'MP-2024-001',
    dateCommande: new Date('2024-07-20'),
    fournisseur: 'DigitalPro',
    modePassation: 'Marché',
    montantHT: 156000,
    statut: 'Commandé',
    dureeGarantie: 24,
    uniteGarantie: 'mois'
  }
];

const mockFournisseurs = [
  'TechnoMaroc', 'InfoSupply', 'DigitalPro', 'CompuSoft', 'TechVision'
];

export const CommandesIT: React.FC = () => {
  const [commandes, setCommandes] = useState<Commande[]>(mockCommandes);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [modeFilter, setModeFilter] = useState('all');
  const [selectedCommande, setSelectedCommande] = useState<Commande | null>(null);
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);
  const [newCommande, setNewCommande] = useState<Partial<Commande>>({
    modePassation: 'BC',
    dureeGarantie: 24,
    uniteGarantie: 'mois',
    statut: 'En attente'
  });

  const filteredCommandes = commandes.filter(cmd => {
    const matchesSearch = cmd.numero.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         cmd.fournisseur.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = statusFilter === 'all' || cmd.statut === statusFilter;
    const matchesMode = modeFilter === 'all' || cmd.modePassation === modeFilter;
    
    return matchesSearch && matchesStatus && matchesMode;
  });

  const getStatusBadge = (statut: string) => {
    switch (statut) {
      case 'En attente':
        return <Badge variant="secondary">En attente</Badge>;
      case 'Commandé':
        return <Badge variant="default">Commandé</Badge>;
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

  const getModeBadge = (mode: string) => {
    switch (mode) {
      case 'BC':
        return <Badge variant="outline">Bon de Commande</Badge>;
      case 'Contrat':
        return <Badge variant="default">Contrat</Badge>;
      case 'Marché':
        return <Badge variant="secondary">Marché Public</Badge>;
      default:
        return <Badge variant="outline">{mode}</Badge>;
    }
  };

  const handleCreateCommande = () => {
    const numeroPrefix = newCommande.modePassation === 'BC' ? 'BC' : 
                        newCommande.modePassation === 'Contrat' ? 'CT' : 'MP';
    const numero = `${numeroPrefix}-2024-${String(commandes.length + 1).padStart(3, '0')}`;
    
    const commande: Commande = {
      id: String(Date.now()),
      numero,
      dateCommande: new Date(),
      fournisseur: newCommande.fournisseur || '',
      modePassation: newCommande.modePassation || 'BC',
      montantHT: newCommande.montantHT || 0,
      statut: 'En attente',
      dureeGarantie: newCommande.dureeGarantie || 24,
      uniteGarantie: newCommande.uniteGarantie || 'mois'
    };

    setCommandes([...commandes, commande]);
    setIsCreateDialogOpen(false);
    setNewCommande({
      modePassation: 'BC',
      dureeGarantie: 24,
      uniteGarantie: 'mois',
      statut: 'En attente'
    });
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
            Commandes Informatiques
          </h1>
          <p className="text-gray-600">Gestion des bons de commande, contrats et marchés IT</p>
        </div>
        
        <Dialog open={isCreateDialogOpen} onOpenChange={setIsCreateDialogOpen}>
          <DialogTrigger asChild>
            <Button className="gap-2 bg-gradient-to-r from-blue-600 to-indigo-600">
              <Plus className="w-4 h-4" />
              Nouvelle Commande
            </Button>
          </DialogTrigger>
          <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
            <DialogHeader>
              <DialogTitle>Créer une nouvelle commande</DialogTitle>
              <DialogDescription>
                Remplissez les informations de la commande informatique
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
                <Label htmlFor="fournisseur">Fournisseur</Label>
                <Select value={newCommande.fournisseur} onValueChange={(value) => 
                  setNewCommande({...newCommande, fournisseur: value})
                }>
                  <SelectTrigger>
                    <SelectValue placeholder="Sélectionner un fournisseur" />
                  </SelectTrigger>
                  <SelectContent>
                    {mockFournisseurs.map(fournisseur => (
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

              <div className="space-y-2">
                <Label>Durée de garantie</Label>
                <div className="flex gap-2">
                  <Input
                    type="number"
                    value={newCommande.dureeGarantie || ''}
                    onChange={(e) => setNewCommande({...newCommande, dureeGarantie: Number(e.target.value)})}
                    placeholder="24"
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
              <Button onClick={handleCreateCommande} className="bg-gradient-to-r from-blue-600 to-indigo-600">
                Créer la commande
              </Button>
            </div>
          </DialogContent>
        </Dialog>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Commandes totales</p>
                <p className="text-2xl font-bold">{commandes.length}</p>
              </div>
              <FileText className="w-8 h-8 text-blue-600" />
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">En attente</p>
                <p className="text-2xl font-bold text-orange-600">
                  {commandes.filter(c => c.statut === 'En attente').length}
                </p>
              </div>
              <Badge variant="secondary" className="text-lg p-2">!</Badge>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Montant total</p>
                <p className="text-2xl font-bold">
                  {commandes.reduce((sum, c) => sum + c.montantHT, 0).toLocaleString()} DH
                </p>
              </div>
              <div className="text-green-600 font-bold text-lg">💰</div>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Payées</p>
                <p className="text-2xl font-bold text-green-600">
                  {commandes.filter(c => c.statut === 'Payé').length}
                </p>
              </div>
              <Badge variant="default" className="bg-green-500 text-lg p-2">✓</Badge>
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
            
            <Select value={modeFilter} onValueChange={setModeFilter}>
              <SelectTrigger className="w-40">
                <SelectValue placeholder="Mode" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Tous les modes</SelectItem>
                <SelectItem value="BC">Bon de Commande</SelectItem>
                <SelectItem value="Contrat">Contrat</SelectItem>
                <SelectItem value="Marché">Marché Public</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      {/* Table */}
      <Card>
        <CardHeader>
          <CardTitle>Liste des commandes ({filteredCommandes.length})</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>N° Commande</TableHead>
                <TableHead>Date</TableHead>
                <TableHead>Fournisseur</TableHead>
                <TableHead>Mode</TableHead>
                <TableHead>Montant HT</TableHead>
                <TableHead>N° Facture</TableHead>
                <TableHead>Réception</TableHead>
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
                  <TableCell>{getModeBadge(commande.modePassation)}</TableCell>
                  <TableCell>{commande.montantHT.toLocaleString()} DH</TableCell>
                  <TableCell className="font-mono text-sm">
                    {commande.numeroFacture || '-'}
                  </TableCell>
                  <TableCell>
                    {commande.dateReception 
                      ? format(commande.dateReception, 'dd MMM yyyy', { locale: fr })
                      : '-'
                    }
                  </TableCell>
                  <TableCell>{getStatusBadge(commande.statut)}</TableCell>
                  <TableCell>
                    <div className="flex gap-1">
                      <Dialog>
                        <DialogTrigger asChild>
                          <Button 
                            variant="ghost" 
                            size="icon"
                            onClick={() => setSelectedCommande(commande)}
                          >
                            <Eye className="w-4 h-4" />
                          </Button>
                        </DialogTrigger>
                        <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
                          <DialogHeader>
                            <DialogTitle>Détail de la commande {commande.numero}</DialogTitle>
                          </DialogHeader>
                          
                          {selectedCommande && (
                            <Tabs defaultValue="general" className="w-full">
                              <TabsList className="grid w-full grid-cols-4">
                                <TabsTrigger value="general">Général</TabsTrigger>
                                <TabsTrigger value="lignes">Lignes</TabsTrigger>
                                <TabsTrigger value="materiels">Matériels</TabsTrigger>
                                <TabsTrigger value="documents">Documents</TabsTrigger>
                              </TabsList>
                              
                              <TabsContent value="general" className="space-y-4">
                                <div className="grid grid-cols-2 gap-4">
                                  <div>
                                    <Label>Numéro de commande</Label>
                                    <p className="font-medium">{selectedCommande.numero}</p>
                                  </div>
                                  <div>
                                    <Label>Mode de passation</Label>
                                    <p>{getModeBadge(selectedCommande.modePassation)}</p>
                                  </div>
                                  <div>
                                    <Label>Fournisseur</Label>
                                    <p className="font-medium">{selectedCommande.fournisseur}</p>
                                  </div>
                                  <div>
                                    <Label>Statut</Label>
                                    <p>{getStatusBadge(selectedCommande.statut)}</p>
                                  </div>
                                  <div>
                                    <Label>Date de commande</Label>
                                    <p>{format(selectedCommande.dateCommande, 'dd MMMM yyyy', { locale: fr })}</p>
                                  </div>
                                  <div>
                                    <Label>Montant HT</Label>
                                    <p className="font-bold text-lg">{selectedCommande.montantHT.toLocaleString()} DH</p>
                                  </div>
                                  <div>
                                    <Label>Garantie</Label>
                                    <p>{selectedCommande.dureeGarantie} {selectedCommande.uniteGarantie}</p>
                                  </div>
                                  <div>
                                    <Label>N° Facture</Label>
                                    <p className="font-mono">{selectedCommande.numeroFacture || 'Non renseigné'}</p>
                                  </div>
                                </div>
                              </TabsContent>
                              
                              <TabsContent value="lignes">
                                <p className="text-gray-500">Lignes de commande à venir...</p>
                              </TabsContent>
                              
                              <TabsContent value="materiels">
                                <p className="text-gray-500">Matériels associés à venir...</p>
                              </TabsContent>
                              
                              <TabsContent value="documents">
                                <div className="space-y-2">
                                  <Button variant="outline" className="w-full justify-start gap-2">
                                    <Download className="w-4 h-4" />
                                    Télécharger le bon de commande
                                  </Button>
                                  <Button variant="outline" className="w-full justify-start gap-2">
                                    <Download className="w-4 h-4" />
                                    Télécharger la facture
                                  </Button>
                                </div>
                              </TabsContent>
                            </Tabs>
                          )}
                        </DialogContent>
                      </Dialog>
                      
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