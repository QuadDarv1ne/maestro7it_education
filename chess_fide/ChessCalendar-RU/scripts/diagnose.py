#!/usr/bin/env python
"""
Diagnostic script to check for common issues in the Chess Calendar application
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def check_imports():
    """Check if all required modules can be imported"""
    print("=" * 60)
    print("Checking imports...")
    print("=" * 60)
    
    modules = [
        'flask',
        'flask_sqlalchemy',
        'flask_limiter',
        'flask_wtf',
        'flask_socketio',
        'celery',
        'redis',
        'requests',
        'bs4',
    ]
    
    failed = []
    for module in modules:
        try:
            __import__(module)
            print(f"✓ {module}")
        except ImportError as e:
            print(f"✗ {module}: {e}")
            failed.append(module)
    
    if failed:
        print(f"\n⚠ Failed to import: {', '.join(failed)}")
        return False
    else:
        print("\n✓ All imports successful")
        return True

def check_database():
    """Check database connection and tables"""
    print("\n" + "=" * 60)
    print("Checking database...")
    print("=" * 60)
    
    try:
        from app import create_app, db
        app = create_app()
        
        with app.app_context():
            # Check if database file exists
            db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
            if os.path.exists(db_path):
                print(f"✓ Database file exists: {db_path}")
            else:
                print(f"⚠ Database file not found: {db_path}")
            
            # Try to query database
            try:
                from app.models.tournament import Tournament
                count = Tournament.query.count()
                print(f"✓ Database connection successful")
                print(f"  Tournaments in database: {count}")
            except Exception as e:
                print(f"✗ Database query failed: {e}")
                return False
        
        return True
    except Exception as e:
        print(f"✗ Database check failed: {e}")
        return False

def check_redis():
    """Check Redis connection"""
    print("\n" + "=" * 60)
    print("Checking Redis...")
    print("=" * 60)
    
    try:
        import redis
        from app import create_app
        app = create_app()
        
        redis_url = app.config.get('REDIS_URL', 'redis://localhost:6379/0')
        print(f"  Redis URL: {redis_url}")
        
        r = redis.from_url(redis_url)
        r.ping()
        print("✓ Redis connection successful")
        return True
    except Exception as e:
        print(f"⚠ Redis not available: {e}")
        print("  Application will use in-memory cache")
        return False

def check_config():
    """Check application configuration"""
    print("\n" + "=" * 60)
    print("Checking configuration...")
    print("=" * 60)
    
    try:
        from app import create_app
        app = create_app()
        
        # Check important config values
        configs = [
            'SECRET_KEY',
            'SQLALCHEMY_DATABASE_URI',
            'REDIS_URL',
            'CELERY_BROKER_URL',
        ]
        
        for config in configs:
            value = app.config.get(config)
            if value:
                # Mask sensitive values
                if 'KEY' in config or 'PASSWORD' in config:
                    display_value = value[:10] + '...' if len(value) > 10 else '***'
                else:
                    display_value = value
                print(f"✓ {config}: {display_value}")
            else:
                print(f"⚠ {config}: Not set")
        
        return True
    except Exception as e:
        print(f"✗ Configuration check failed: {e}")
        return False

def check_static_files():
    """Check if critical static files exist"""
    print("\n" + "=" * 60)
    print("Checking static files...")
    print("=" * 60)
    
    static_dir = os.path.join(os.path.dirname(__file__), '..', 'static')
    
    critical_files = [
        'css/improvements.css',
        'css/cards-final-fix.css',
        'css/override-all.css',
        'css/composition-fixes.css',
        'css/layout-fixes.css',
        'js/app.js',
    ]
    
    missing = []
    for file in critical_files:
        path = os.path.join(static_dir, file)
        if os.path.exists(path):
            size = os.path.getsize(path)
            print(f"✓ {file} ({size} bytes)")
        else:
            print(f"✗ {file}: Not found")
            missing.append(file)
    
    if missing:
        print(f"\n⚠ Missing files: {', '.join(missing)}")
        return False
    else:
        print("\n✓ All critical static files present")
        return True

def check_logs():
    """Check log files"""
    print("\n" + "=" * 60)
    print("Checking logs...")
    print("=" * 60)
    
    logs_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
    
    if not os.path.exists(logs_dir):
        print(f"⚠ Logs directory not found: {logs_dir}")
        return False
    
    log_files = ['chess_calendar.log', 'chess_calendar_error.log']
    
    for log_file in log_files:
        path = os.path.join(logs_dir, log_file)
        if os.path.exists(path):
            size = os.path.getsize(path)
            print(f"✓ {log_file} ({size} bytes)")
            
            # Check for recent errors
            if 'error' in log_file.lower():
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        if lines:
                            print(f"  Last error: {lines[-1].strip()[:100]}")
                        else:
                            print(f"  No errors logged")
                except Exception as e:
                    print(f"  Could not read log: {e}")
        else:
            print(f"⚠ {log_file}: Not found")
    
    return True

def main():
    """Run all diagnostic checks"""
    print("\n" + "=" * 60)
    print("Chess Calendar - Diagnostic Tool")
    print("=" * 60)
    
    results = {
        'Imports': check_imports(),
        'Database': check_database(),
        'Redis': check_redis(),
        'Configuration': check_config(),
        'Static Files': check_static_files(),
        'Logs': check_logs(),
    }
    
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    
    for check, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{check:20s}: {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ All checks passed!")
    else:
        print("⚠ Some checks failed. Please review the output above.")
    print("=" * 60)
    
    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())
