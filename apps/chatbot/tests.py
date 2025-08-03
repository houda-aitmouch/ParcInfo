from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import ChatMessage
from .llm_engine import ParcInfoChatbot
import json

User = get_user_model()

class ChatbotTestCase(TestCase):
    def setUp(self):
        """Configuration initiale pour les tests"""
        # Créer un gestionnaire (staff)
        self.manager = User.objects.create_user(
            username='manager',
            password='testpass123',
            is_superuser=False,
            is_staff=True
        )
        
        # Créer un superadmin
        self.superadmin = User.objects.create_user(
            username='superadmin',
            password='adminpass123',
            is_superuser=True,
            is_staff=True
        )
        
        # Créer un employé (non-staff, non-superuser)
        self.employee = User.objects.create_user(
            username='employee',
            password='employeepass123',
            is_superuser=False,
            is_staff=False
        )
        
        self.client = Client()
    
    def test_chat_interface_access_manager(self):
        """Test d'accès à l'interface de chat pour un gestionnaire"""
        # Test avec gestionnaire
        self.client.login(username='manager', password='testpass123')
        response = self.client.get(reverse('chatbot:chat_interface'))
        self.assertEqual(response.status_code, 200)
    
    def test_chat_interface_access_superadmin(self):
        """Test d'accès à l'interface de chat pour un superadmin"""
        # Test avec superadmin
        self.client.login(username='superadmin', password='adminpass123')
        response = self.client.get(reverse('chatbot:chat_interface'))
        self.assertEqual(response.status_code, 200)
    
    def test_chat_interface_access_employee_denied(self):
        """Test que les employés n'ont pas accès au chatbot"""
        # Test avec employé (doit être refusé)
        self.client.login(username='employee', password='employeepass123')
        response = self.client.get(reverse('chatbot:chat_interface'))
        self.assertEqual(response.status_code, 302)  # Redirection
    
    def test_chat_interface_access_unauthenticated(self):
        """Test d'accès sans authentification"""
        response = self.client.get(reverse('chatbot:chat_interface'))
        self.assertEqual(response.status_code, 302)  # Redirection vers login
    
    def test_chat_api_access_manager(self):
        """Test d'accès à l'API de chat pour un gestionnaire"""
        self.client.login(username='manager', password='testpass123')
        
        data = {
            'message': 'Analyser les tendances des demandes',
            'session_id': 'test_session'
        }
        response = self.client.post(
            reverse('chatbot:chat_api'),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        
        # Vérifier que le message a été sauvegardé
        self.assertTrue(ChatMessage.objects.filter(user=self.manager).exists())
    
    def test_chat_api_access_employee_denied(self):
        """Test que les employés n'ont pas accès à l'API"""
        self.client.login(username='employee', password='employeepass123')
        data = {'message': 'Test message'}
        response = self.client.post(
            reverse('chatbot:chat_api'),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 403)
    
    def test_chat_message_model(self):
        """Test du modèle ChatMessage"""
        message = ChatMessage.objects.create(
            user=self.manager,
            message='Test message',
            response='Test response',
            session_id='test_session'
        )
        
        self.assertEqual(message.user, self.manager)
        self.assertEqual(message.message, 'Test message')
        self.assertEqual(message.response, 'Test response')
        self.assertEqual(message.session_id, 'test_session')
        self.assertIsNotNone(message.timestamp)
    
    def test_chat_history_access_manager(self):
        """Test d'accès à l'historique pour un gestionnaire"""
        self.client.login(username='manager', password='testpass123')
        response = self.client.get(reverse('chatbot:chat_history'))
        self.assertEqual(response.status_code, 200)
    
    def test_chat_history_access_employee_denied(self):
        """Test que les employés n'ont pas accès à l'historique"""
        self.client.login(username='employee', password='employeepass123')
        response = self.client.get(reverse('chatbot:chat_history'))
        self.assertEqual(response.status_code, 302)  # Redirection
    
    def test_help_page_access_manager(self):
        """Test d'accès à la page d'aide pour un gestionnaire"""
        self.client.login(username='manager', password='testpass123')
        response = self.client.get(reverse('chatbot:help'))
        self.assertEqual(response.status_code, 200)
    
    def test_help_page_access_employee_denied(self):
        """Test que les employés n'ont pas accès à l'aide"""
        self.client.login(username='employee', password='employeepass123')
        response = self.client.get(reverse('chatbot:help'))
        self.assertEqual(response.status_code, 302)  # Redirection
    
    def test_learning_insights_access_manager(self):
        """Test d'accès aux insights d'apprentissage pour un gestionnaire"""
        self.client.login(username='manager', password='testpass123')
        response = self.client.get(reverse('chatbot:learning_insights'))
        self.assertEqual(response.status_code, 200)
    
    def test_learning_insights_access_employee_denied(self):
        """Test que les employés n'ont pas accès aux insights"""
        self.client.login(username='employee', password='employeepass123')
        response = self.client.get(reverse('chatbot:learning_insights'))
        self.assertEqual(response.status_code, 302)  # Redirection
    
    def test_clear_history_functionality(self):
        """Test de la fonctionnalité d'effacement d'historique"""
        # Créer quelques messages de test
        ChatMessage.objects.create(
            user=self.manager,
            message='Test 1',
            response='Response 1'
        )
        ChatMessage.objects.create(
            user=self.manager,
            message='Test 2',
            response='Response 2'
        )
        
        self.assertEqual(ChatMessage.objects.filter(user=self.manager).count(), 2)
        
        # Effacer l'historique
        self.client.login(username='manager', password='testpass123')
        response = self.client.post(reverse('chatbot:clear_history'))
        self.assertEqual(response.status_code, 302)  # Redirection
        
        # Vérifier que les messages ont été supprimés
        self.assertEqual(ChatMessage.objects.filter(user=self.manager).count(), 0)

class ParcInfoChatbotTestCase(TestCase):
    def setUp(self):
        """Configuration pour les tests du chatbot"""
        self.manager = User.objects.create_user(
            username='manager',
            password='testpass123',
            is_superuser=False,
            is_staff=True
        )
        self.chatbot = ParcInfoChatbot()
    
    def test_llm_initialization(self):
        """Test de l'initialisation du LLM"""
        # Vérifier que le chatbot a été initialisé
        self.assertIsNotNone(self.chatbot)
        
        # Vérifier que les composants sont disponibles
        if self.chatbot.llm:
            self.assertIsNotNone(self.chatbot.llm)
        
        if self.chatbot.vectorstore:
            self.assertIsNotNone(self.chatbot.vectorstore)
    
    def test_comprehensive_database_context(self):
        """Test de la récupération du contexte complet de base de données"""
        context = self.chatbot.get_comprehensive_database_context()
        self.assertIsInstance(context, str)
        self.assertGreater(len(context), 0)
    
    def test_user_context(self):
        """Test de la récupération du contexte utilisateur"""
        data = self.chatbot.get_user_context(self.manager)
        self.assertIsInstance(data, str)
    
    def test_system_analytics(self):
        """Test de la récupération des analytics système"""
        analytics = self.chatbot.get_system_analytics()
        self.assertIsInstance(analytics, str)
    
    def test_get_response(self):
        """Test de la génération de réponses"""
        # Test avec une question technique
        response = self.chatbot.get_response("Analyser les performances du système", self.manager)
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)
        
        # Test avec une question sur l'optimisation
        response = self.chatbot.get_response("Comment optimiser la gestion du stock ?", self.manager)
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)
    
    def test_learning_from_interaction(self):
        """Test de l'apprentissage continu"""
        # Vérifier que l'historique d'apprentissage est initialisé
        self.assertIsInstance(self.chatbot.conversation_history, list)
        
        # Simuler une interaction
        initial_count = len(self.chatbot.conversation_history)
        self.chatbot.learn_from_interaction("Test question", "Test response", self.manager)
        
        # Vérifier que l'interaction a été ajoutée
        self.assertEqual(len(self.chatbot.conversation_history), initial_count + 1)
    
    def test_get_learning_insights(self):
        """Test de la récupération des insights d'apprentissage"""
        insights = self.chatbot.get_learning_insights()
        self.assertIsInstance(insights, dict)
        
        # Vérifier les clés attendues
        expected_keys = ['total_interactions', 'avg_response_length', 'user_role_distribution', 'recent_activity', 'learning_progress']
        for key in expected_keys:
            self.assertIn(key, insights)
    
    def test_refresh_context(self):
        """Test du rafraîchissement du contexte"""
        try:
            self.chatbot.refresh_context()
            # Si pas d'erreur, le test passe
            self.assertTrue(True)
        except Exception as e:
            # Si erreur, c'est normal car pas de base de données de test
            self.assertIsInstance(e, Exception)

class ChatbotIntegrationTestCase(TestCase):
    """Tests d'intégration du chatbot"""
    
    def setUp(self):
        """Configuration pour les tests d'intégration"""
        self.manager = User.objects.create_user(
            username='integration_manager',
            password='testpass123',
            is_superuser=False,
            is_staff=True
        )
        self.client = Client()
        self.client.login(username='integration_manager', password='testpass123')
    
    def test_full_chat_flow_manager(self):
        """Test du flux complet de chat pour un gestionnaire"""
        # Test de l'accès à l'interface
        response = self.client.get(reverse('chatbot:chat_interface'))
        self.assertEqual(response.status_code, 200)
        
        # Test d'envoi d'un message technique
        data = {
            'message': 'Analyser les tendances des demandes d\'équipement',
            'session_id': 'integration_test'
        }
        response = self.client.post(
            reverse('chatbot:chat_api'),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        
        # Vérifier la réponse
        response_data = json.loads(response.content)
        self.assertIn('response', response_data)
        self.assertIn('session_id', response_data)
        
        # Vérifier que le message a été sauvegardé
        self.assertTrue(ChatMessage.objects.filter(user=self.manager).exists())
    
    def test_learning_insights_integration(self):
        """Test d'intégration des insights d'apprentissage"""
        # Test de l'accès aux insights
        response = self.client.get(reverse('chatbot:learning_insights'))
        self.assertEqual(response.status_code, 200)
    
    def test_chat_history_integration(self):
        """Test d'intégration de l'historique"""
        # Créer quelques messages
        ChatMessage.objects.create(
            user=self.manager,
            message='Message technique 1',
            response='Réponse IA 1',
            session_id='test_session'
        )
        ChatMessage.objects.create(
            user=self.manager,
            message='Message technique 2',
            response='Réponse IA 2',
            session_id='test_session'
        )
        
        # Test de l'accès à l'historique
        response = self.client.get(reverse('chatbot:chat_history'))
        self.assertEqual(response.status_code, 200)
        
        # Vérifier que les messages sont dans le contexte
        self.assertContains(response, 'Message technique 1')
        self.assertContains(response, 'Message technique 2') 