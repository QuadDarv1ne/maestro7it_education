#!/usr/bin/env python3
"""
Test script to verify connection pooling functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.connection_pool import stockfish_pool
from contextlib import contextmanager
import time

def test_connection_pooling():
    """Test the connection pooling functionality"""
    print("Testing Stockfish engine connection pooling...")
    
    # Test getting engines from pool
    engines = []
    try:
        # Get multiple engines
        for i in range(3):
            print(f"Getting engine {i+1} from pool...")
            engine = stockfish_pool.get_engine(skill_level=i+1)
            engines.append(engine)
            print(f"Got engine {i+1} with skill level {i+1}")
            
            # Test engine functionality
            fen = engine.get_fen_position()
            print(f"Engine {i+1} FEN: {fen}")
            
        # Return engines to pool
        print("Returning engines to pool...")
        for i, engine in enumerate(engines):
            stockfish_pool.return_engine(engine)
            print(f"Returned engine {i+1} to pool")
            
        # Get stats
        stats = stockfish_pool.get_stats()
        print(f"Pool stats: {stats}")
        
        print("Connection pooling test completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error during connection pooling test: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Clean up
        try:
            stockfish_pool.close_all()
        except:
            pass

def test_context_manager():
    """Test the context manager functionality"""
    print("\nTesting context manager...")
    
    try:
        from utils.connection_pool import get_stockfish_engine
        
        # Test context manager
        with get_stockfish_engine(skill_level=3) as engine:
            print("Got engine from context manager")
            fen = engine.get_fen_position()
            print(f"Engine FEN: {fen}")
            
        print("Context manager test completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error during context manager test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Starting connection pooling tests...")
    
    # Test basic pooling
    success1 = test_connection_pooling()
    
    # Test context manager
    success2 = test_context_manager()
    
    if success1 and success2:
        print("\nAll tests passed!")
        sys.exit(0)
    else:
        print("\nSome tests failed!")
        sys.exit(1)