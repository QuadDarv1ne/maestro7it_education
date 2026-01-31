#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simple HTTP Server for Chess Web Interface
Serves the chess web interface and provides API endpoints
"""

import http.server
import socketserver
import json
import os
import urllib.parse
from pathlib import Path

class ChessHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(Path(__file__).parent.parent / "web"), **kwargs)
    
    def do_GET(self):
        # Serve the main chess interface
        if self.path == '/' or self.path == '/index.html':
            self.path = '/chess_web_interface.html'
        
        # API endpoints
        elif self.path.startswith('/api/'):
            self.handle_api_request()
            return
        
        return super().do_GET()
    
    def do_POST(self):
        if self.path.startswith('/api/'):
            self.handle_api_request()
            return
        
        return super().do_POST()
    
    def handle_api_request(self):
        """Handle API requests for chess engine integration"""
        try:
            if self.path == '/api/move':
                self.handle_move_request()
            elif self.path == '/api/new-game':
                self.handle_new_game_request()
            elif self.path == '/api/evaluate':
                self.handle_evaluate_request()
            elif self.path == '/api/valid-moves':
                self.handle_valid_moves_request()
            else:
                self.send_error(404, "API endpoint not found")
        except Exception as e:
            self.send_error(500, f"Internal server error: {str(e)}")
    
    def handle_move_request(self):
        """Handle move validation and execution"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        move_data = json.loads(post_data.decode('utf-8'))
        
        # In a real implementation, this would connect to the C++ chess engine
        response = {
            "success": True,
            "move": move_data,
            "board_state": self.get_mock_board_state(),
            "game_status": "playing"
        }
        
        self.send_json_response(response)
    
    def handle_new_game_request(self):
        """Handle new game request"""
        response = {
            "success": True,
            "board_state": self.get_initial_board_state(),
            "current_player": "white",
            "game_status": "playing"
        }
        
        self.send_json_response(response)
    
    def handle_evaluate_request(self):
        """Handle position evaluation request"""
        response = {
            "evaluation": 0.0,  # Neutral position
            "best_move": "e2e4",
            "depth": 3,
            "nodes": 10000
        }
        
        self.send_json_response(response)
    
    def handle_valid_moves_request(self):
        """Handle valid moves request"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        position_data = json.loads(post_data.decode('utf-8'))
        
        # Mock valid moves - in real implementation, query the engine
        valid_moves = ["e2e4", "d2d4", "g1f3", "b1c3"]
        
        response = {
            "valid_moves": valid_moves,
            "piece": position_data.get("piece", ""),
            "position": position_data.get("position", "")
        }
        
        self.send_json_response(response)
    
    def send_json_response(self, data):
        """Send JSON response"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def get_initial_board_state(self):
        """Return initial chess board state"""
        return [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]
    
    def get_mock_board_state(self):
        """Return mock board state"""
        return self.get_initial_board_state()

class ChessWebServer:
    def __init__(self, port=8080):
        self.port = port
        self.handler = ChessHTTPRequestHandler
        self.httpd = None
    
    def start(self):
        """Start the web server"""
        try:
            self.httpd = socketserver.TCPServer(("", self.port), self.handler)
            print(f"♔ ♕ ♖ ♗ ♘ ♙ CHESS WEB SERVER STARTED ♟ ♞ ♝ ♜ ♛ ♚")
            print(f"🌐 Server running at: http://localhost:{self.port}")
            print(f"📁 Serving files from: {Path(__file__).parent.parent / 'web'}")
            print(f"🎮 Access the chess interface at: http://localhost:{self.port}")
            print(f"🔄 Press Ctrl+C to stop the server")
            print("=" * 50)
            
            self.httpd.serve_forever()
            
        except KeyboardInterrupt:
            print("\n🛑 Shutting down server...")
            self.stop()
        except Exception as e:
            print(f"❌ Server error: {e}")
    
    def stop(self):
        """Stop the web server"""
        if self.httpd:
            self.httpd.shutdown()
            self.httpd.server_close()
            print("✅ Server stopped")

def main():
    """Main function to run the web server"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Chess Web Interface Server')
    parser.add_argument('-p', '--port', type=int, default=8080, 
                       help='Port to run the server on (default: 8080)')
    parser.add_argument('--host', default='localhost',
                       help='Host to bind to (default: localhost)')
    
    args = parser.parse_args()
    
    # Change to project directory
    project_dir = Path(__file__).parent.parent
    os.chdir(project_dir)
    
    server = ChessWebServer(port=args.port)
    server.start()

if __name__ == "__main__":
    main()