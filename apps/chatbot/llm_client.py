import json
import logging
import requests
import re
from typing import List, Dict, Optional, Any
from django.conf import settings
from datetime import datetime

logger = logging.getLogger(__name__)


class OllamaClient:
    """Client for Ollama/LLaMA 3 integration with RAG context"""
    
    def __init__(self):
        self.base_url = getattr(settings, 'OLLAMA_URL', 'http://localhost:11434')
        self.model = getattr(settings, 'OLLAMA_MODEL', 'llama3')
        self.timeout = getattr(settings, 'OLLAMA_TIMEOUT', 30)
        self.max_tokens = getattr(settings, 'OLLAMA_MAX_TOKENS', 1000)
        self.temperature = getattr(settings, 'OLLAMA_TEMPERATURE', 0.7)
        
    def is_available(self) -> bool:
        """Check if Ollama service is available"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception as e:
            logger.warning(f"Ollama not available: {e}")
            return False
    
    def list_models(self) -> List[str]:
        """List available models in Ollama"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=10)
            if response.status_code == 200:
                data = response.json()
                return [model['name'] for model in data.get('models', [])]
            return []
        except Exception as e:
            logger.error(f"Error listing models: {e}")
            return []
    
    def generate_response(self, prompt: str, context: List[Dict] = None) -> str:
        """Generate response using LLaMA 3 with RAG context"""
        try:
            # Build enhanced prompt with context
            enhanced_prompt = self._build_rag_prompt(prompt, context or [])
            
            payload = {
                "model": self.model,
                "prompt": enhanced_prompt,
                "stream": False,
                "options": {
                    "temperature": self.temperature,
                    "num_predict": self.max_tokens,
                    "top_p": 0.9,
                    "top_k": 40
                }
            }
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                return self._clean_response(result.get('response', ''))
            else:
                logger.error(f"Ollama API error: {response.status_code} - {response.text}")
                return "Désolé, le service LLM n'est pas disponible actuellement."
                
        except requests.exceptions.Timeout:
            logger.error("Ollama request timeout")
            return "La génération de réponse a pris trop de temps. Veuillez réessayer."
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "Une erreur est survenue lors de la génération de la réponse."
    
    def _build_rag_prompt(self, query: str, context: List[Dict]) -> str:
        """Build enhanced prompt with RAG context and strong anti-hallucination rules"""
        system_prompt = """Tu es un assistant IA spécialisé dans la gestion du parc informatique et bureautique.

RÈGLES STRICTES ANTI-HALLUCINATIONS :
1. UTILISE UNIQUEMENT LES DONNÉES DU CONTEXTE FOURNI. NE PAS INVENTER OU AJOUTER D'INFORMATIONS EXTÉRIEURES.
2. SI LE CONTEXTE NE CONTIENT PAS LA RÉPONSE EXACTE, RÉPONDS : "Information non disponible dans les données actuelles."
3. NE PAS GÉNÉRALISER OU INFÉRER AU-DELÀ DU CONTEXTE. PAS D'OPINIONS PERSONNELLES.
4. RÉPONDS DE MANIÈRE DÉTAILLÉE ET STRUCTURÉE : Maximum 400 mots pour les questions complexes.
5. STRUCTURE : Utilise des puces (•) pour les listes, tableaux Markdown pour les données structurées, sections avec ##.
6. SI DONNÉES NUMÉRIQUES : Fournis des chiffres précis sans arrondis approximatifs.
7. MONNAIE : Utilise TOUJOURS "DH HT" (Dirhams Hors Taxes) pour tous les montants, jamais d'euros (€).
8. FIN DE RÉPONSE : Ne pas ajouter de mention de source.
8. CONTEXTE RICHE : Utilise TOUS les détails disponibles dans le contexte pour une réponse complète.
9. RELATIONS : Explique les liens entre les entités (fournisseurs, commandes, matériels, etc.).
10. DATES : Inclus toujours les dates pertinentes pour donner du contexte temporel.
11. ANALYSES COMPLEXES : Pour les questions multi-tables, organise la réponse par entité ou critère.
12. RECOMMANDATIONS : Si demandé, propose des actions basées sur les données disponibles.

FORMAT DE RÉPONSE EXEMPLES :
- Comptage : "Total : X éléments. Détails : • Item1 • Item2"
- Recherche : "Matériel trouvé : Code XXX, Statut YYY, Localisation ZZZ"
- Statistique : "| Catégorie | Valeur |\n|----------|--------|\n| Total PC | 42 |"
- Relation : "Fournisseur X a livré Y commandes, dont Z en retard"
- Analyse complexe : "## Analyse par fournisseur\n### Fournisseur A\n• Commandes : X\n• Livraisons : Y\n### Fournisseur B\n..."
- Inconnu : "Information non disponible dans les données actuelles."

CONTEXTE DISPONIBLE : Utilise TOUS les champs et relations disponibles pour une réponse exhaustive et structurée."""

        if context:
            # Filter and prioritize context (amélioré pour une meilleure pertinence)
            relevant_context = self._filter_relevant_context(query, context)
            
            if relevant_context:
                context_text = "\n".join([
                    f"• {item.get('content', '')} (Score de pertinence : {item.get('score', 0):.2f})" 
                    for item in relevant_context[:5]  # Top 5 pour plus de contexte sans surcharge
                ])
                
                prompt = f"""{system_prompt}

CONTEXTE STRICT (NE PAS UTILISER AUTRE CHOSE) :
{context_text}

QUESTION UTILISATEUR : {query}

RÉPONSE BASÉE EXCLUSIVEMENT SUR LE CONTEXTE :"""
            else:
                prompt = f"""{system_prompt}

QUESTION : {query}

RÉPONSE : Information non disponible dans les données actuelles."""
        else:
            prompt = f"""{system_prompt}

QUESTION : {query}

RÉPONSE : Aucune donnée disponible pour répondre à cette question."""
        
        return prompt
    
    def _filter_relevant_context(self, query: str, context: List[Dict]) -> List[Dict]:
        """Enhanced context filtering with intelligent relevance scoring"""
        query_lower = query.lower()
        
        # Enhanced keywords mapping for better relevance
        keyword_filters = {
            'serveur': ['serveur', 'server', 'srv'],
            'pc': ['pc', 'ordinateur', 'computer', 'poste'],
            'imprimante': ['imprimante', 'printer', 'impression'],
            'fournisseur': ['fournisseur', 'supplier', 'vendeur'],
            'commande': ['commande', 'order', 'achat'],
            'livraison': ['livraison', 'delivery', 'reception'],
            'materiel': ['materiel', 'equipement', 'equipment', 'hardware'],
            'utilisateur': ['utilisateur', 'user', 'employe', 'employee'],
            'date': ['date', 'jour', 'mois', 'annee', 'year', 'month'],
            'statut': ['statut', 'status', 'etat', 'state'],
            'retard': ['retard', 'delay', 'en retard', 'late'],
            'garantie': ['garantie', 'warranty', 'garantie'],
            'facture': ['facture', 'invoice', 'bill'],
            'prix': ['prix', 'cout', 'montant', 'price', 'cost', 'amount']
        }
        
        # Calculate relevance score for each context item
        scored_context = []
        
        for item in context:
            score = 0.0
            content = item.get('content', '').lower()
            metadata = item.get('metadata', {})
            
            # Base score from RAG
            score += item.get('score', 0) * 0.4
            
            # Keyword matching score
            for category, keywords in keyword_filters.items():
                if any(keyword in query_lower for keyword in keywords):
                    if any(keyword in content for keyword in keywords):
                        score += 0.3
                        break
            
            # Exact query match bonus
            query_words = query_lower.split()
            for word in query_words:
                if len(word) > 3 and word in content:
                    score += 0.1
            
            # Metadata relevance
            if metadata.get('strategy') == 'exact':
                score += 0.2
            elif metadata.get('strategy') == 'semantic':
                score += 0.1
            
            # Content length bonus (prefer detailed content)
            if len(content) > 200:
                score += 0.1
            
            scored_context.append((item, score))
        
        # Sort by score and return top results
        scored_context.sort(key=lambda x: x[1], reverse=True)
        
        # Return top 5 most relevant items
        return [item for item, score in scored_context[:5]]
    
    def _clean_response(self, response: str) -> str:
        """Clean and format LLM response"""
        if not response:
            return "Je n'ai pas pu générer une réponse appropriée."
        
        response = response.strip()
        
        # Remove redundant system acknowledgments
        prefixes_to_remove = [
            "En tant qu'assistant IA",
            "Basé sur les informations fournies",
            "D'après le contexte",
            "Selon les données",
            "En consultant",
            "En réponse à votre",
            "Voici les informations",
            "Analyse des",
            "Interprétation des"
        ]
        
        for prefix in prefixes_to_remove:
            if response.lower().startswith(prefix.lower()):
                # Find the first meaningful sentence
                sentences = response.split('. ')
                for i, sentence in enumerate(sentences):
                    if len(sentence.strip()) > 20 and not any(p.lower() in sentence.lower() for p in prefixes_to_remove):
                        response = '. '.join(sentences[i:])
                        break
        
        # Remove excessive formatting
        response = re.sub(r'\n\s*\n\s*\n+', '\n\n', response)  # Max 2 line breaks
        response = re.sub(r'^\s*[\*\-•]\s*', '• ', response, flags=re.MULTILINE)  # Standardize bullets
        
        # Limit response length
        if len(response) > 800:
            sentences = response.split('. ')
            truncated = []
            char_count = 0
            for sentence in sentences:
                if char_count + len(sentence) > 750:
                    break
                truncated.append(sentence)
                char_count += len(sentence)
            response = '. '.join(truncated)
            if not response.endswith('.'):
                response += '.'
        
        return response
    
    def chat_with_context(self, query: str, rag_results: List[Dict], 
                         conversation_history: List[Dict] = None) -> Dict[str, Any]:
        """Enhanced chat with RAG context and conversation memory"""
        try:
            # Prepare context from RAG results
            context = []
            for result in rag_results[:3]:  # Top 3 most relevant
                context.append({
                    'content': result.get('content', ''),
                    'score': result.get('score', 0),
                    'metadata': result.get('metadata', {})
                })
            
            # Generate response
            response = self.generate_response(query, context)
            
            # Prepare sources for citation
            sources = []
            for item in context:
                metadata = item.get('metadata', {})
                if metadata.get('model') and metadata.get('pk'):
                    sources.append({
                        'type': metadata['model'],
                        'id': metadata['pk'],
                        'relevance': item.get('score', 0)
                    })
            
            return {
                'response': response,
                'sources': sources,
                'context_used': len(context),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Chat error: {e}")
            return {
                'response': "Une erreur est survenue lors du traitement de votre demande.",
                'sources': [],
                'context_used': 0,
                'error': str(e)
            }


class RAGChatbot:
    """Enhanced chatbot combining intent-based routing with RAG+LLM"""
    
    def __init__(self, rag_manager, ollama_client):
        self.rag = rag_manager
        self.llm = ollama_client
        self.use_llm = ollama_client.is_available()
        
        if self.use_llm:
            logger.info("✅ RAG Chatbot initialized with LLM support")
        else:
            logger.warning("⚠️ RAG Chatbot initialized without LLM (fallback mode)")
    
    def process_query(self, query: str, use_rag: bool = True) -> Dict[str, Any]:
        """Process query with hybrid approach: intent routing + RAG+LLM"""
        
        # For specific intents, use direct handlers for speed and accuracy
        structured_intents = [
            'liste_materiel', 'liste_commandes', 'liste_fournisseurs',
            'statut_livraison', 'demandes_equipement'
        ]
        
        # For complex/ambiguous queries, use RAG+LLM
        rag_intents = ['recherche_materiel', 'statistiques', 'help']
        
        if use_rag and self.use_llm:
            # Get relevant context from RAG
            rag_results = self.rag.semantic_search(query, top_k=5)
            
            if rag_results:
                # Use LLM with RAG context
                chat_result = self.llm.chat_with_context(query, rag_results)
                return {
                    'response': chat_result['response'] + "\n*Source : modèle Llama 3 avec recherche contextuelle*",
                    'method': 'rag_llm',
                    'sources': chat_result.get('sources', []),
                    'context_used': chat_result.get('context_used', 0)
                }
        
        # Fallback to structured response
        return {
            'response': "Mode de réponse structurée non disponible pour cette requête.",
            'method': 'structured',
            'sources': [],
            'context_used': 0
        }
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get system health status"""
        return {
            'rag_documents': self.rag.get_rag_count(),
            'llm_available': self.use_llm,
            'ollama_models': self.llm.list_models() if self.use_llm else [],
            'timestamp': datetime.now().isoformat()
        }
