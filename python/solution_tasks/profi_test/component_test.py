"""
Test individual components of the profi_test application
"""
import os
import sys

print("Testing individual components...")

# Test 1: Basic imports
print("\n1. Testing basic imports:")
try:
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    from flask_login import LoginManager
    print("✓ Basic Flask components imported")
except Exception as e:
    print(f"✗ Basic imports failed: {e}")

# Test 2: Database models
print("\n2. Testing database models:")
try:
    # Test if we can import models without ML dependencies
    sys.path.insert(0, 'app')
    from models import User, TestResult, TestQuestion
    print("✓ Database models imported")
except Exception as e:
    print(f"✗ Database models import failed: {e}")

# Test 3: Routes
print("\n3. Testing routes:")
try:
    from app.routes import main
    from app.auth import auth
    print("✓ Routes imported")
except Exception as e:
    print(f"✗ Routes import failed: {e}")

# Test 4: Configuration
print("\n4. Testing configuration:")
try:
    from config import Config
    print("✓ Configuration imported")
    print(f"  Database URI: {Config.SQLALCHEMY_DATABASE_URI}")
    print(f"  Secret key length: {len(Config.SECRET_KEY) if Config.SECRET_KEY else 0}")
except Exception as e:
    print(f"✗ Configuration import failed: {e}")

# Test 5: Simple database operations
print("\n5. Testing database operations:")
try:
    from app import create_app, db
    app = create_app()
    with app.app_context():
        # Test creating tables
        db.create_all()
        print("✓ Database tables created")
        
        # Test simple query
        from app.models import User
        users = User.query.all()
        print(f"✓ Database query successful, found {len(users)} users")
        
        # Test creating a user
        if len(users) == 0:
            user = User(username='testuser', email='test@example.com')
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()
            print("✓ User created successfully")
            
            # Verify user was created
            created_user = User.query.filter_by(username='testuser').first()
            if created_user and created_user.check_password('password123'):
                print("✓ User authentication works")
            else:
                print("✗ User authentication failed")
        else:
            print(f"✓ Found existing users: {len(users)}")
    
    print("✓ All database tests passed")
    
except Exception as e:
    print(f"✗ Database operations failed: {e}")
    import traceback
    traceback.print_exc()

print("\nComponent testing completed!")