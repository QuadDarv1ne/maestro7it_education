#!/usr/bin/env python3
"""
Simple Flask Web Server for Chess Interface
"""

from flask import Flask, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def index():
    """Serve the enhanced chess interface"""
    web_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(web_dir, 'enhanced_chess.html')

@app.route('/classic')
def classic():
    """Serve the classic interface"""
    web_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(web_dir, 'index.html')

if __name__ == '__main__':
    print("♔ ♕ ♖ ♗ ♘ ♙ SIMPLE CHESS SERVER ♟ ♞ ♝ ♜ ♛ ♚")
    print("=" * 40)
    print("Available at: http://localhost:5000")
    print("Classic version: http://localhost:5000/classic")
    print("=" * 40)
    
    app.run(host='0.0.0.0', port=5000, debug=True)