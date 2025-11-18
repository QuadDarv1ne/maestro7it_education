#!/usr/bin/env python3
"""Simple test to verify the application is working correctly."""

import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import create_app, db
    from app.models import Employee, User
    
    app = create_app()
    
    with app.app_context():
        # Test database connection
        employee_count = Employee.query.count()
        user_count = User.query.count()
        
        print(f"✅ Application test successful!")
        print(f"📊 Employee count: {employee_count}")
        print(f"👥 User count: {user_count}")
        print(f"🌐 App name: {app.name}")
        print(f"🔧 Debug mode: {app.debug}")
        
except Exception as e:
    print(f"❌ Application test failed: {e}")
    sys.exit(1)

print("✅ All tests passed!")