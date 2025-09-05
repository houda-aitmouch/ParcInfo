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

  const callBackend = async (userMessage: string): Promise<ChatMessage> => {
    try {
      const res = await fetch('/chatbot/api/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: userMessage })
      });
      const data = await res.json();
      const content = data?.response || "Désolé, je n'ai pas pu traiter la demande.";
      return {
        id: Date.now().toString(),
        type: 'bot',
        content,
        timestamp: new Date(),
        quickActions: quickSuggestions
      };
    } catch (e) {
      return {
        id: Date.now().toString(),
        type: 'bot',
        content: "Une erreur est survenue. Veuillez réessayer.",
        timestamp: new Date(),
        quickActions: quickSuggestions
      };
    }
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
      const botResponse = await callBackend(inputValue);
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
            <img src={addLogo} alt="ADD" className="h-5 w-auto" />
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