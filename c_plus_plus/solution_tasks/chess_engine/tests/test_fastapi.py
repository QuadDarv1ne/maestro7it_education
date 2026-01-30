#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Тестирование и документация FastAPI Chess API
Проверка всех endpoint'ов и генерация API документации
"""

import requests
import json
import time
from typing import Dict, List

class APITester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.game_id = None
    
    def test_health_endpoint(self) -> bool:
        """Тест health check endpoint"""
        print("🏥 Testing Health Endpoint...")
        try:
            response = self.session.get(f"{self.base_url}/health")
            if response.status_code == 200:
                data = response.json()
                print(f"   ✓ Health check passed: {data}")
                return True
            else:
                print(f"   ✗ Health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"   ✗ Health check error: {e}")
            return False
    
    def test_create_game(self) -> bool:
        """Тест создания новой игры"""
        print("\n🎮 Testing Game Creation...")
        try:
            payload = {
                "player_name": "Test Player",
                "game_mode": "ai",
                "player_color": True
            }
            
            response = self.session.post(
                f"{self.base_url}/api/new-game",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                self.game_id = data.get('game_id')
                print(f"   ✓ Game created successfully")
                print(f"   Game ID: {self.game_id}")
                print(f"   Board state shape: {len(data['board_state'])}x{len(data['board_state'][0])}")
                print(f"   Current turn: {'White' if data['current_turn'] else 'Black'}")
                return True
            else:
                print(f"   ✗ Game creation failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
        except Exception as e:
            print(f"   ✗ Game creation error: {e}")
            return False
    
    def test_make_move(self) -> bool:
        """Тест выполнения хода"""
        if not self.game_id:
            print("   ⚠ No game ID available for move test")
            return False
            
        print("\n♟️ Testing Move Making...")
        try:
            # Пробуем простой ход пешки: e2 на e4 (в индексации с 0: [6,4] на [4,4])
            payload = {
                "game_id": self.game_id,
                "from_pos": [6, 4],  # e2
                "to_pos": [4, 4],    # e4
                "player_color": True
            }
            
            response = self.session.post(
                f"{self.base_url}/api/make-move",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print("   ✓ Move made successfully")
                    print(f"   New board turn: {'White' if data['game_state']['current_turn'] else 'Black'}")
                    print(f"   Move history length: {len(data['game_state']['move_history'])}")
                    return True
                else:
                    print(f"   ⚠ Move rejected: {data.get('message', 'Unknown reason')}")
                    return False
            else:
                print(f"   ✗ Move request failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"   ✗ Move test error: {e}")
            return False
    
    def test_ai_move(self) -> bool:
        """Тест получения хода AI"""
        if not self.game_id:
            print("   ⚠ No game ID available for AI test")
            return False
            
        print("\n🤖 Testing AI Move...")
        try:
            response = self.session.get(f"{self.base_url}/api/ai-move/{self.game_id}")
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print(f"   ✓ AI move generated: {data.get('move_notation', 'N/A')}")
                    print(f"   New board turn: {'White' if data['game_state']['current_turn'] else 'Black'}")
                    return True
                else:
                    print("   ⚠ AI move failed")
                    return False
            else:
                print(f"   ✗ AI move request failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"   ✗ AI test error: {e}")
            return False
    
    def test_undo_move(self) -> bool:
        """Тест отмены хода"""
        if not self.game_id:
            print("   ⚠ No game ID available for undo test")
            return False
            
        print("\n↩️ Testing Move Undo...")
        try:
            response = self.session.post(f"{self.base_url}/api/undo-move/{self.game_id}")
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print("   ✓ Move undone successfully")
                    print(f"   Move history length after undo: {len(data['game_state']['move_history'])}")
                    return True
                else:
                    print("   ⚠ Undo failed")
                    return False
            else:
                print(f"   ✗ Undo request failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"   ✗ Undo test error: {e}")
            return False
    
    def run_comprehensive_test(self):
        """Запуск всех тестов и генерация отчёта"""
        print("♔ ♕ ♖ ♗ ♘ ♙ FASTAPI CHESS API TEST SUITE ♟ ♞ ♝ ♜ ♛ ♚")
        print("=" * 60)
        
        results = {}
        
        # Тест health endpoint
        results['health'] = self.test_health_endpoint()
        
        # Тест создания игры
        results['create_game'] = self.test_create_game()
        
        # Тест выполнения хода (если игра создана)
        if results['create_game']:
            results['make_move'] = self.test_make_move()
            
            # Тест хода AI (если ход был сделан)
            if results['make_move']:
                results['ai_move'] = self.test_ai_move()
                results['undo_move'] = self.test_undo_move()
        
        # Generate summary
        print("\n" + "=" * 60)
        print("📋 TEST RESULTS SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        for test_name, result in results.items():
            status = "✓ PASS" if result else "✗ FAIL"
            print(f"{test_name:15} {status}")
        
        print("-" * 60)
        print(f"Overall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
        
        if passed == total:
            print("🎉 All tests passed! API is working correctly.")
        else:
            print("⚠️  Some tests failed. Please check the API implementation.")
        
        return results

def generate_api_documentation():
    """Generate API documentation"""
    doc = {
        "title": "Chess Engine API Documentation",
        "version": "2.0.0",
        "description": "RESTful API for chess game operations with real-time WebSocket support",
        "base_url": "http://localhost:8000",
        "endpoints": [
            {
                "method": "GET",
                "path": "/",
                "description": "Serve the main chess application frontend",
                "response": "HTML page with chess interface"
            },
            {
                "method": "GET",
                "path": "/health",
                "description": "Health check endpoint",
                "response": {
                    "status": "healthy",
                    "timestamp": "ISO timestamp"
                }
            },
            {
                "method": "POST",
                "path": "/api/new-game",
                "description": "Create a new chess game",
                "request_body": {
                    "player_name": "string (optional)",
                    "game_mode": "string ('ai' or 'human')",
                    "player_color": "boolean (true=white, false=black)"
                },
                "response": {
                    "game_id": "string",
                    "board_state": "2D array",
                    "current_turn": "boolean",
                    "game_status": "string",
                    "move_history": "array",
                    "player_name": "string",
                    "game_mode": "string"
                }
            },
            {
                "method": "POST",
                "path": "/api/make-move",
                "description": "Make a move in the chess game",
                "request_body": {
                    "game_id": "string",
                    "from_pos": "[int, int]",
                    "to_pos": "[int, int]",
                    "player_color": "boolean"
                },
                "response": {
                    "success": "boolean",
                    "game_state": "GameState object (if success=true)",
                    "message": "string (if success=false)"
                }
            },
            {
                "method": "GET",
                "path": "/api/ai-move/{game_id}",
                "description": "Get AI move for current position",
                "response": {
                    "success": "boolean",
                    "move_notation": "string",
                    "game_state": "GameState object"
                }
            },
            {
                "method": "POST",
                "path": "/api/undo-move/{game_id}",
                "description": "Undo the last move",
                "response": {
                    "success": "boolean",
                    "game_state": "GameState object"
                }
            },
            {
                "method": "WebSocket",
                "path": "/ws/{game_id}",
                "description": "Real-time game updates via WebSocket",
                "messages": {
                    "incoming": "Connection established",
                    "outgoing": {
                        "type": "'game_update' or 'move_made'",
                        "game_state": "GameState object",
                        "move_notation": "string (for move_made)"
                    }
                }
            }
        ],
        "models": {
            "GameState": {
                "game_id": "string",
                "board_state": "8x8 array of strings",
                "current_turn": "boolean (true=white turn)",
                "game_status": "string ('active', 'check', 'checkmate', 'stalemate')",
                "move_history": "array of move objects",
                "player_name": "string",
                "game_mode": "string"
            },
            "MoveRecord": {
                "from": "[int, int]",
                "to": "[int, int]",
                "piece": "string",
                "captured": "string or null",
                "timestamp": "ISO timestamp"
            }
        }
    }
    
    # Save documentation
    with open('api_documentation.json', 'w', encoding='utf-8') as f:
        json.dump(doc, f, indent=2, ensure_ascii=False)
    
    print(f"\n📚 API documentation saved to: api_documentation.json")
    return doc

def main():
    """Main testing function"""
    # Generate documentation
    print("Generating API documentation...")
    generate_api_documentation()
    
    # Wait a moment for server to start
    print("\nWaiting for server to start...")
    time.sleep(2)
    
    # Run tests
    tester = APITester()
    results = tester.run_comprehensive_test()
    
    # Save test results
    with open('api_test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Test results saved to: api_test_results.json")

if __name__ == "__main__":
    main()