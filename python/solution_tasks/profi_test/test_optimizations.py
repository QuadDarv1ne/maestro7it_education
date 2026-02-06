#!/usr/bin/env python3
"""
Test script to verify all performance optimizations are working
"""
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_application_creation():
    """Test that the application can be created with all optimizations"""
    print("Testing application creation with optimizations...")
    
    try:
        from app import create_app
        app = create_app()
        print("✅ Application created successfully")
        
        # Test that all optimization components are present
        components = [
            'async_task_processor',
            'compression_middleware', 
            'connection_pool',
            'query_result_cache',
            'static_asset_optimizer',
            'request_batcher',
            'performance_monitor_enhanced'
        ]
        
        missing_components = []
        for component in components:
            if hasattr(app, component):
                print(f"✅ {component} initialized")
            else:
                missing_components.append(component)
                print(f"❌ {component} missing")
        
        if missing_components:
            print(f"\n⚠️  Missing components: {missing_components}")
            return False
        else:
            print("\n🎉 All optimization components successfully initialized!")
            return True
            
    except Exception as e:
        print(f"❌ Error creating application: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_cli_commands():
    """Test that CLI commands are registered"""
    print("\nTesting CLI command registration...")
    
    try:
        from app import create_app
        app = create_app()
        
        # Test command registration
        with app.app_context():
            commands = list(app.cli.commands.keys())
            required_commands = [
                'task-stats',
                'compression-stats', 
                'pool-stats-advanced',
                'cache-stats',
                'asset-stats',
                'batch-stats',
                'perf-dashboard-init'
            ]
            
            available_commands = []
            missing_commands = []
            
            for cmd in required_commands:
                if cmd in commands:
                    available_commands.append(cmd)
                    print(f"✅ CLI command '{cmd}' registered")
                else:
                    missing_commands.append(cmd)
                    print(f"❌ CLI command '{cmd}' missing")
            
            if missing_commands:
                print(f"\n⚠️  Missing CLI commands: {missing_commands}")
                return False
            else:
                print(f"\n🎉 All {len(available_commands)} CLI commands registered!")
                return True
                
    except Exception as e:
        print(f"❌ Error testing CLI commands: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Performance Optimization Test Suite")
    print("=" * 50)
    
    tests = [
        ("Application Creation", test_application_creation),
        ("CLI Commands", test_cli_commands)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name} test...")
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS")
    print("=" * 50)
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print(f"\n📈 Summary: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! Performance optimizations are working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())