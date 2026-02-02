"""
Simple test script to verify the application works
"""
import os
import sys

print("Starting application test...")
print(f"Python version: {sys.version}")

try:
    print("Importing Flask app...")
    from app import create_app, db
    print("✓ Flask app imported successfully")
    
    print("Creating app instance...")
    app = create_app()
    print("✓ App instance created")
    
    print("Testing database connection...")
    with app.app_context():
        # Try to create all tables
        db.create_all()
        print("✓ Database tables created")
        
        # Try to query the database
        from app.models import User
        users = User.query.all()
        print(f"✓ Database query successful, found {len(users)} users")
    
    print("Application test completed successfully!")
    print("You can now run: python run.py")
    
except Exception as e:
    print(f"✗ Error during test: {e}")
    import traceback
    traceback.print_exc()