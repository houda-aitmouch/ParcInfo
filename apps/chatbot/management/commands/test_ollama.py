from django.core.management.base import BaseCommand
from django.conf import settings
import requests
import json


class Command(BaseCommand):
    help = 'Test Ollama installation and LLaMA 3 availability'

    def handle(self, *args, **options):
        self.stdout.write("🔍 Testing Ollama installation...")
        
        ollama_url = getattr(settings, 'OLLAMA_URL', 'http://localhost:11434')
        
        # Test 1: Check if Ollama is running
        try:
            response = requests.get(f"{ollama_url}/api/tags", timeout=10)
            if response.status_code == 200:
                self.stdout.write(self.style.SUCCESS("✅ Ollama service is running"))
                
                # List available models
                data = response.json()
                models = [model['name'] for model in data.get('models', [])]
                
                if models:
                    self.stdout.write(f"📦 Available models: {', '.join(models)}")
                    
                    # Check for LLaMA 3 variants
                    llama_models = [m for m in models if 'llama' in m.lower()]
                    if llama_models:
                        self.stdout.write(self.style.SUCCESS(f"🦙 LLaMA models found: {', '.join(llama_models)}"))
                    else:
                        self.stdout.write(self.style.WARNING("⚠️ No LLaMA models found"))
                        self.stdout.write("💡 Install with: ollama pull llama3")
                else:
                    self.stdout.write(self.style.WARNING("⚠️ No models installed"))
                    self.stdout.write("💡 Install LLaMA 3 with: ollama pull llama3")
                    
            else:
                self.stdout.write(self.style.ERROR(f"❌ Ollama API error: {response.status_code}"))
                
        except requests.exceptions.ConnectionError:
            self.stdout.write(self.style.ERROR("❌ Cannot connect to Ollama"))
            self.stdout.write("💡 Install Ollama: https://ollama.ai/download")
            self.stdout.write("💡 Start service: ollama serve")
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Unexpected error: {e}"))
        
        # Test 2: Simple generation test (if available)
        try:
            model_name = getattr(settings, 'OLLAMA_MODEL', 'llama3')
            test_prompt = "Réponds simplement: Bonjour, je suis LLaMA 3"
            
            payload = {
                "model": model_name,
                "prompt": test_prompt,
                "stream": False,
                "options": {"num_predict": 50}
            }
            
            response = requests.post(
                f"{ollama_url}/api/generate",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                generated_text = result.get('response', '').strip()
                self.stdout.write(self.style.SUCCESS(f"✅ Generation test successful"))
                self.stdout.write(f"🤖 Response: {generated_text[:100]}...")
            else:
                self.stdout.write(self.style.WARNING(f"⚠️ Generation test failed: {response.status_code}"))
                
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"⚠️ Generation test error: {e}"))
        
        # Test 3: RAG integration test
        self.stdout.write("\n🔍 Testing RAG integration...")
        try:
            from apps.chatbot.rag_manager import RAGManager
            from apps.chatbot.llm_client import OllamaClient
            
            rag = RAGManager()
            llm = OllamaClient()
            
            doc_count = rag.get_rag_count()
            self.stdout.write(f"📚 RAG documents: {doc_count}")
            
            if doc_count > 0:
                # Test semantic search
                results = rag.semantic_search("matériel informatique", top_k=2)
                self.stdout.write(f"🔍 Semantic search test: {len(results)} results")
                
                if results and llm.is_available():
                    # Test full RAG+LLM pipeline
                    chat_result = llm.chat_with_context("Liste le matériel informatique", results)
                    self.stdout.write(self.style.SUCCESS("✅ Full RAG+LLM pipeline working"))
                    self.stdout.write(f"🤖 Sample response: {chat_result['response'][:100]}...")
                else:
                    self.stdout.write(self.style.WARNING("⚠️ RAG+LLM pipeline incomplete"))
            else:
                self.stdout.write(self.style.WARNING("⚠️ No RAG documents found"))
                self.stdout.write("💡 Run: python manage.py deploy_chatbot to populate RAG index")
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ RAG integration error: {e}"))
        
        self.stdout.write("\n" + "="*50)
        self.stdout.write("🎯 NEXT STEPS:")
        self.stdout.write("1. If Ollama not installed: curl -fsSL https://ollama.ai/install.sh | sh")
        self.stdout.write("2. Start Ollama: ollama serve")
        self.stdout.write("3. Install LLaMA 3: ollama pull llama3")
        self.stdout.write("4. Test chatbot: python manage.py test_ollama")
        self.stdout.write("5. Deploy full system: python manage.py deploy_chatbot")
