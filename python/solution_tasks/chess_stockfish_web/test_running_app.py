#!/usr/bin/env python3
"""
Test script to verify the running application
"""

import requests
import time

def test_web_server():
    """Test if the web server is responding"""
    print("Testing web server...")
    try:
        response = requests.get('http://127.0.0.1:5001')
        if response.status_code == 200:
            print("✅ Web server is running and responding")
            return True
        else:
            print(f"❌ Web server returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to web server")
        return False
    except Exception as e:
        print(f"❌ Error testing web server: {e}")
        return False

def test_static_files():
    """Test if static files are accessible"""
    print("\nTesting static files...")
    try:
        # Test CSS file
        css_response = requests.get('http://127.0.0.1:5001/static/css/style.css')
        if css_response.status_code == 200:
            print("✅ CSS file is accessible")
        else:
            print(f"❌ CSS file returned status code: {css_response.status_code}")
            
        # Test JS file
        js_response = requests.get('http://127.0.0.1:5001/static/js/game.js')
        if js_response.status_code == 200:
            print("✅ JavaScript file is accessible")
        else:
            print(f"❌ JavaScript file returned status code: {js_response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing static files: {e}")

def main():
    """Main test function"""
    print("Testing Running Chess Stockfish Web Application")
    print("=" * 50)
    
    # Wait a moment for the server to fully start
    time.sleep(2)
    
    # Test web server
    server_ok = test_web_server()
    
    # Test static files
    if server_ok:
        test_static_files()
    
    print("\n" + "=" * 50)
    if server_ok:
        print("🎉 All tests passed! The application is running correctly.")
        print("\nYou can now access the application in your browser at:")
        print("  http://127.0.0.1:5001")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    
    return server_ok

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)