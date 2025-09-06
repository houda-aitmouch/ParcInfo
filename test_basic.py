#!/usr/bin/env python3
"""
Basic test file for ParcInfo project
Tests basic imports and Django configuration
"""

import os
import sys
import django
from django.conf import settings

def test_basic_imports():
    """Test that basic Python imports work"""
    try:
        import django
        import psycopg2
        import pandas
        import numpy
        print("✓ Basic imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_django_setup():
    """Test Django setup and configuration"""
    try:
        # Set up Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ParcInfo.settings')
        django.setup()
        
        # Test basic Django functionality
        from django.apps import apps
        from django.contrib.auth.models import User
        
        print("✓ Django setup successful")
        print(f"✓ Django version: {django.get_version()}")
        print(f"✓ Installed apps: {len(apps.get_app_configs())}")
        return True
    except Exception as e:
        print(f"✗ Django setup error: {e}")
        return False

def test_database_connection():
    """Test database connection"""
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result[0] == 1:
                print("✓ Database connection successful")
                return True
            else:
                print("✗ Database query failed")
                return False
    except Exception as e:
        print(f"✗ Database connection error: {e}")
        return False

def main():
    """Run all basic tests"""
    print("Running basic tests for ParcInfo...")
    print("=" * 50)
    
    tests = [
        test_basic_imports,
        test_django_setup,
        test_database_connection
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All basic tests passed!")
        return 0
    else:
        print("✗ Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
