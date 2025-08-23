import React, { useState, useRef, useEffect } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Badge } from './ui/badge';
import { ScrollArea } from './ui/scroll-area';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { X, Send, Bot, User, Search, Package, Truck, AlertCircle } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import addLogo from '../assets/add.png';

interface ChatMessage {
  id: string;
  type: 'user' | 'bot';
  content: string;
  timestamp: Date;
  sources?: string[];
  quickActions?: string[];
}

interface ChatbotProps {
  isOpen: boolean;
  onClose: () => void;
}

const quickSuggestions = [
  "Matériels sous garantie ce mois",
  "Livraisons en retard",
  "Commandes en attente",
  "Fournisseurs actifs",
  "Demandes non traitées"
];

export const Chatbot: React.FC<ChatbotProps> = ({ isOpen, onClose }) => {
  const { user } = useAuth();
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (isOpen && messages.length === 0) {
      // Welcome message
      const welcomeMessage: ChatMessage = {
        id: '1',
        type: 'bot',
        content: `Bonjour ${user?.name} ! 👋

Je suis l'assistant IA de l'Agence de Développement du Digital pour la gestion du parc informatique. 

Comment puis-je vous aider aujourd'hui ?`,
        timestamp: new Date(),
        quickActions: quickSuggestions
      };
      setMessages([welcomeMessage]);
    }
  }, [isOpen, user, messages.length]);

  const simulateBotResponse = async (userMessage: string): Promise<ChatMessage> => {
    // Simulate AI processing time
    await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 2000));

    let response = '';
    let sources: string[] = [];

    if (userMessage.toLowerCase().includes('garantie')) {
      response = `📊 **Rapport de garanties - ADD**

J'ai analysé votre parc informatique et trouvé **15 équipements** dont la garantie expire dans les 30 prochains jours :

🔴 **Priorité Haute :**
• Dell Latitude 7520 (INV-2024-001) - Expire le 25 août 2024
• HP ProBook 450 (INV-2024-002) - Expire le 20 août 2024

🟡 **Attention :**
• MacBook Pro M2 (INV-2024-003) - Expire le 10 septembre 2024
• Surface Pro 9 (INV-2024-004) - Expire le 15 septembre 2024

💡 **Recommandations ADD :**
• Planifier le renouvellement ou extension de garantie
• Contacter les fournisseurs agréés
• Budgétiser les remplacements éventuels

Voulez-vous que je génère un rapport détaillé ou programme des alertes automatiques ?`;
      sources = ['Base matériels ADD', 'Contrats fournisseurs', 'Système de monitoring'];
    } else if (userMessage.toLowerCase().includes('livraison')) {
      response = `🚚 **État des livraisons - Plateforme ADD**

**Situation actuelle :**

🔴 **En retard (3 commandes) :**
• Commande BC-2024-015 - Retard de 5 jours (TechnoMaroc)
• Commande CT-2024-008 - Retard de 2 jours (InfoSupply)
• Commande MP-2024-003 - Retard de 1 jour (DigitalPro)

🟡 **Prévues cette semaine (7 commandes) :**
• BC-2024-018 - Prévue demain (25 PC portables)
• BC-2024-019 - Prévue vendredi (imprimantes multifonctions)

✅ **Livrées récemment (12 cette semaine)**

📞 **Actions suggérées :**
• Contacter les fournisseurs en retard
• Programmer les réceptions prévues
• Mettre à jour le planning logistique

Souhaitez-vous que je contacte automatiquement les fournisseurs concernés ?`;
      sources = ['Module livraisons ADD', 'Planning fournisseurs', 'Système de suivi'];
    } else if (userMessage.toLowerCase().includes('commande')) {
      response = `📋 **Tableau de bord commandes - ADD**

**Résumé financier 2024 :**
• 💰 Budget total : 1,200,000 DH
• 💸 Engagé : 876,000 DH (73%)
• 💳 Disponible : 324,000 DH

**Commandes en cours :**
📊 **Par statut :**
• ⏳ En attente de validation : 12 commandes
• 🚀 En cours de livraison : 8 commandes  
• ✅ Livrées ce mois : 23 commandes

📋 **Actions prioritaires :**
• 3 factures à valider (montant : 45,800 DH)
• 2 PV de réception en attente
• 1 commande urgente à traiter

**Performance fournisseurs :**
• 🥇 TechnoMaroc : 98% de ponctualité
• 🥈 InfoSupply : 87% de conformité
• 🥉 DigitalPro : 92% satisfaction

Voulez-vous consulter une commande spécifique ou analyser un fournisseur ?`;
      sources = ['Module commandes ADD', 'Base fournisseurs', 'Système comptable'];
    } else if (userMessage.toLowerCase().includes('fournisseur')) {
      response = `🏢 **Annuaire fournisseurs ADD - 2024**

**Fournisseurs actifs (certifiés ADD) :**

🏆 **Top performance :**
1. **TechnoMaroc** - Partenaire privilégié
   • 25 commandes (287,500 DH)
   • Taux de livraison : 98%
   • Note satisfaction : 4.8/5

2. **InfoSupply** - Fournisseur agréé
   • 18 commandes (156,800 DH)
   • Taux de livraison : 87%
   • Note satisfaction : 4.2/5

3. **DigitalPro** - Partenaire technique
   • 12 commandes (98,200 DH)
   • Taux de livraison : 92%
   • Note satisfaction : 4.5/5

📈 **Statistiques globales :**
• Fournisseurs actifs : 15
• Taux moyen de ponctualité : 89%
• Économies réalisées : 125,000 DH
• Certifications ADD : 100%

🔍 **Services disponibles :**
• Évaluation qualité automatique
• Suivi performance temps réel
• Gestion contractuelle intégrée

Besoin d'informations détaillées sur un fournisseur particulier ?`;
      sources = ['Registre fournisseurs ADD', 'Évaluations qualité', 'Base contractuelle'];
    } else if (userMessage.toLowerCase().includes('demande')) {
      response = `📝 **Gestionnaire de demandes ADD**

**Demandes d'équipement en attente :**

⏳ **Non traitées (5 demandes) :**
• DEQ-2024-045 - Ordinateur portable (Mohammed A., Développement)
• DEQ-2024-046 - Écran 24" (Fatima Z., Comptabilité)  
• DEQ-2024-047 - Souris ergonomique (Ahmed B., RH)
• DEQ-2024-048 - Imprimante laser (Rachid M., Communication)
• DEQ-2024-049 - Tablette iPad (Khadija L., Direction)

✅ **Traitées cette semaine (8 demandes) :**
• DEQ-2024-042 - Approuvée, en cours de commande
• DEQ-2024-043 - Matériel affecté et livré
• DEQ-2024-044 - Budget validé, commande lancée

📊 **Statistiques mensuelles :**
• Demandes reçues : 47
• Taux d'approbation : 85%
• Délai moyen de traitement : 3.2 jours
• Budget consommé : 89,500 DH

🎯 **Actions recommandées :**
• Prioriser les demandes urgentes
• Vérifier la disponibilité budgétaire
• Optimiser les délais de traitement

Voulez-vous traiter une demande spécifique ou consulter le budget disponible ?`;
      sources = ['Module demandes ADD', 'Stock disponible', 'Budget alloué'];
    } else {
      response = `🤖 **Assistant IA ADD - Services disponibles**

Je peux vous accompagner dans la gestion de votre parc informatique :

🔍 **Recherche & Analyse :**
• État des équipements et garanties
• Suivi des commandes et livraisons  
• Analyse des performances fournisseurs
• Gestion des demandes utilisateurs
• Tableaux de bord personnalisés

💡 **Actions intelligentes :**
• Génération de rapports automatiques
• Alertes préventives personnalisées
• Optimisation des achats et budgets
• Prédictions de maintenance
• Recommandations d'amélioration

🎯 **Spécialités ADD :**
• Conformité aux procédures gouvernementales
• Suivi budgétaire en temps réel
• Gestion multi-sites et services
• Traçabilité complète des actifs

📞 **Support technique :**
• Disponible 24h/7j
• Base de connaissances intégrée
• Escalade vers équipes spécialisées

Posez-moi une question spécifique ou choisissez une suggestion ci-dessous ! 👇`;
    }

    return {
      id: Date.now().toString(),
      type: 'bot',
      content: response,
      timestamp: new Date(),
      sources,
      quickActions: quickSuggestions.filter(s => !userMessage.toLowerCase().includes(s.toLowerCase().split(' ')[0]))
    };
  };

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      type: 'user',
      content: inputValue,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const botResponse = await simulateBotResponse(inputValue);
      setMessages(prev => [...prev, botResponse]);
    } catch (error) {
      const errorMessage: ChatMessage = {
        id: Date.now().toString(),
        type: 'bot',
        content: 'Désolé, je rencontre une difficulté technique temporaire. L\'équipe ADD a été notifiée. Veuillez réessayer dans quelques instants.',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleQuickAction = (action: string) => {
    setInputValue(action);
    handleSendMessage();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-y-0 right-0 z-50 w-96 bg-white border-l shadow-xl">
      <div className="flex flex-col h-full">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 text-white">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-white/20 rounded-lg flex items-center justify-center">
              <Bot className="w-4 h-4" />
            </div>
            <div>
              <h3 className="font-medium">Assistant IA ADD</h3>
              <p className="text-xs text-blue-100">Intelligence Artificielle Gouvernementale</p>
            </div>
          </div>
          <Button variant="ghost" size="icon" onClick={onClose} className="text-white hover:bg-white/20">
            <X className="w-4 h-4" />
          </Button>
        </div>

        {/* ADD Badge */}
        <div className="px-4 py-2 bg-gradient-to-r from-blue-50 to-purple-50 border-b">
          <div className="flex items-center gap-2">
            <img src={addLogo} alt="ADD" className="h-4 w-auto" />
            <span className="text-xs text-gray-600">Agence de Développement du Digital</span>
          </div>
        </div>

        {/* Messages */}
        <ScrollArea className="flex-1 p-4">
          <div className="space-y-4">
            {messages.map((message) => (
              <div key={message.id} className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-[80%] space-y-2 ${message.type === 'user' ? 'order-2' : 'order-1'}`}>
                  <div className={`flex items-center gap-2 ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
                    {message.type === 'bot' && (
                      <div className="w-6 h-6 bg-gradient-to-br from-blue-600 via-purple-600 to-indigo-600 rounded-full flex items-center justify-center">
                        <Bot className="w-3 h-3 text-white" />
                      </div>
                    )}
                    <span className="text-xs text-gray-500">
                      {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </span>
                    {message.type === 'user' && (
                      <div className="w-6 h-6 bg-gradient-to-br from-gray-400 to-gray-500 rounded-full flex items-center justify-center">
                        <User className="w-3 h-3 text-white" />
                      </div>
                    )}
                  </div>
                  
                  <div className={`p-3 rounded-lg whitespace-pre-wrap ${
                    message.type === 'user' 
                      ? 'bg-gradient-to-br from-blue-600 via-purple-600 to-indigo-600 text-white' 
                      : 'bg-gradient-to-br from-gray-50 to-gray-100 text-gray-900 border'
                  }`}>
                    {message.content}
                  </div>

                  {message.sources && message.sources.length > 0 && (
                    <div className="flex flex-wrap gap-1">
                      {message.sources.map((source, index) => (
                        <Badge key={index} variant="outline" className="text-xs border-blue-200 text-blue-700">
                          <Search className="w-3 h-3 mr-1" />
                          {source}
                        </Badge>
                      ))}
                    </div>
                  )}

                  {message.quickActions && message.quickActions.length > 0 && (
                    <div className="space-y-2">
                      <p className="text-xs text-gray-500">💡 Actions rapides :</p>
                      <div className="flex flex-wrap gap-1">
                        {message.quickActions.slice(0, 3).map((action, index) => (
                          <Button
                            key={index}
                            variant="outline"
                            size="sm"
                            className="text-xs h-7 border-blue-200 hover:bg-blue-50 hover:text-blue-700"
                            onClick={() => handleQuickAction(action)}
                          >
                            {action}
                          </Button>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            ))}

            {isLoading && (
              <div className="flex justify-start">
                <div className="flex items-center gap-2">
                  <div className="w-6 h-6 bg-gradient-to-br from-blue-600 via-purple-600 to-indigo-600 rounded-full flex items-center justify-center">
                    <Bot className="w-3 h-3 text-white" />
                  </div>
                  <div className="bg-gradient-to-br from-gray-50 to-gray-100 border p-3 rounded-lg">
                    <div className="flex gap-1">
                      <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse"></div>
                      <div className="w-2 h-2 bg-purple-400 rounded-full animate-pulse" style={{ animationDelay: '0.2s' }}></div>
                      <div className="w-2 h-2 bg-indigo-400 rounded-full animate-pulse" style={{ animationDelay: '0.4s' }}></div>
                    </div>
                  </div>
                </div>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>
        </ScrollArea>

        {/* Input */}
        <div className="p-4 border-t bg-gradient-to-r from-gray-50 to-blue-50">
          <div className="flex gap-2">
            <Input
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Posez votre question à l'IA ADD..."
              disabled={isLoading}
              onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
              className="flex-1 border-blue-200 focus:border-blue-400"
            />
            <Button 
              onClick={handleSendMessage} 
              disabled={!inputValue.trim() || isLoading}
              className="bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 hover:from-blue-700 hover:via-purple-700 hover:to-indigo-700"
            >
              <Send className="w-4 h-4" />
            </Button>
          </div>
          <p className="text-xs text-gray-500 mt-2 text-center">
            🔒 IA sécurisée ADD - Données confidentielles protégées
          </p>
        </div>
      </div>
    </div>
  );
};