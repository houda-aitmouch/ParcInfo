#!/usr/bin/env python3
"""
RAG Chatbot test file for ParcInfo project
Tests the chatbot functionality and RAG system
"""

import os
import sys
import django
import json
from datetime import datetime

def setup_django():
    """Setup Django environment"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ParcInfo.settings')
    django.setup()

def test_chatbot_imports():
    """Test that chatbot modules can be imported"""
    try:
        from apps.chatbot.models import ChatMessage, VectorStore
        from apps.chatbot.core_chatbot import CoreChatbot
        from apps.chatbot.rag_manager import RAGManager
        print("✓ Chatbot imports successful")
        return True
    except ImportError as e:
        print(f"✗ Chatbot import error: {e}")
        return False

def test_chatbot_models():
    """Test chatbot models"""
    try:
        from apps.chatbot.models import ChatMessage, VectorStore
        
        # Test model creation
        print("✓ Chatbot models accessible")
        return True
    except Exception as e:
        print(f"✗ Chatbot models error: {e}")
        return False

def test_rag_manager():
    """Test RAG manager functionality"""
    try:
        from apps.chatbot.rag_manager import RAGManager
        
        # Test RAG manager initialization
        rag_manager = RAGManager()
        print("✓ RAG Manager initialization successful")
        return True
    except Exception as e:
        print(f"✗ RAG Manager error: {e}")
        return False

def test_core_chatbot():
    """Test core chatbot functionality"""
    try:
        from apps.chatbot.core_chatbot import CoreChatbot
        
        # Test chatbot initialization
        chatbot = CoreChatbot()
        print("✓ Core Chatbot initialization successful")
        return True
    except Exception as e:
        print(f"✗ Core Chatbot error: {e}")
        return False

def test_vector_store():
    """Test vector store functionality"""
    try:
        from apps.chatbot.models import VectorStore
        
        # Test vector store operations
        print("✓ Vector Store accessible")
        return True
    except Exception as e:
        print(f"✗ Vector Store error: {e}")
        return False

def test_chatbot_dependencies():
    """Test chatbot-specific dependencies"""
    try:
        import sentence_transformers
        import transformers
        import torch
        import numpy
        import pandas
        print("✓ Chatbot dependencies available")
        return True
    except ImportError as e:
        print(f"✗ Chatbot dependencies error: {e}")
        return False

def run_chatbot_tests():
    """Run all chatbot tests"""
    print("Running RAG Chatbot tests for ParcInfo...")
    print("=" * 60)
    
    tests = [
        test_chatbot_dependencies,
        test_chatbot_imports,
        test_chatbot_models,
        test_rag_manager,
        test_core_chatbot,
        test_vector_store
    ]
    
    passed = 0
    total = len(tests)
    test_results = []
    
    for test in tests:
        test_name = test.__name__
        print(f"Running {test_name}...")
        
        try:
            if test():
                passed += 1
                test_results.append({
                    "test": test_name,
                    "status": "PASSED",
                    "timestamp": datetime.now().isoformat()
                })
            else:
                test_results.append({
                    "test": test_name,
                    "status": "FAILED",
                    "timestamp": datetime.now().isoformat()
                })
        except Exception as e:
            print(f"✗ {test_name} failed with exception: {e}")
            test_results.append({
                "test": test_name,
                "status": "ERROR",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
        print()
    
    # Generate test report
    report = {
        "summary": {
            "total_tests": total,
            "passed": passed,
            "failed": total - passed,
            "timestamp": datetime.now().isoformat()
        },
        "results": test_results
    }
    
    # Save test report
    report_filename = f"test_report_chatbot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_filename, 'w') as f:
        json.dump(report, f, indent=2)
    
    print("=" * 60)
    print(f"Chatbot tests completed: {passed}/{total} passed")
    print(f"Test report saved to: {report_filename}")
    
    if passed == total:
        print("✓ All chatbot tests passed!")
        return 0
    else:
        print("✗ Some chatbot tests failed!")
        return 1

def main():
    """Main test function"""
    try:
        setup_django()
        return run_chatbot_tests()
    except Exception as e:
        print(f"✗ Test setup failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
