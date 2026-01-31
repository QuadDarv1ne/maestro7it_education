#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Multi-threaded Chess AI Implementation
Uses parallel search to leverage multiple CPU cores
"""

from typing import List, Tuple, Dict, Optional, Any
import threading
import queue
import time
import math
from concurrent.futures import ThreadPoolExecutor, as_completed
import multiprocessing as mp

class ThreadSafeCounter:
    """Thread-safe counter for shared statistics"""
    
    def __init__(self, initial_value=0):
        self._value = initial_value
        self._lock = threading.Lock()
    
    def increment(self, amount=1):
        with self._lock:
            self._value += amount
    
    def get(self):
        with self._lock:
            return self._value
    
    def reset(self, value=0):
        with self._lock:
            self._value = value

class ParallelChessAI:
    """Multi-threaded chess AI with parallel search capabilities"""
    
    def __init__(self, search_depth: int = 4, num_threads: Optional[int] = None):
        self.search_depth = search_depth
        self.num_threads = num_threads or mp.cpu_count()
        self.nodes_searched = ThreadSafeCounter()
        self.tt_hits = ThreadSafeCounter()
        
        # Shared transposition table
        self.transposition_table = {}
        self.tt_lock = threading.Lock()
        
        # Shared evaluation cache
        self.eval_cache = {}
        self.eval_lock = threading.Lock()
        
        # Synchronization primitives
        self.stop_flag = threading.Event()
        self.best_move_lock = threading.Lock()
        self.best_move = None
        self.best_score = None
        
        # Thread pool for parallel execution
        self.executor = ThreadPoolExecutor(max_workers=self.num_threads)
        
        print(f"🧵 Multi-threaded AI initialized with {self.num_threads} threads")
    
    def get_best_move(self, board: List[List[str]], color: bool, time_limit: float = 5.0) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Get best move using parallel search"""
        print(f"🚀 Starting parallel search with {self.num_threads} threads...")
        
        # Reset counters and flags
        self.nodes_searched.reset()
        self.tt_hits.reset()
        self.stop_flag.clear()
        self.best_move = None
        self.best_score = None
        
        start_time = time.time()
        
        try:
            # Split root moves among threads
            legal_moves = self.generate_legal_moves(board, color)
            
            if not legal_moves:
                return None
            
            if len(legal_moves) == 1:
                return legal_moves[0]
            
            # Distribute moves among threads
            moves_per_thread = max(1, len(legal_moves) // self.num_threads)
            move_groups = []
            
            for i in range(0, len(legal_moves), moves_per_thread):
                group = legal_moves[i:i + moves_per_thread]
                if group:
                    move_groups.append(group)
            
            # Ensure we have enough groups for all threads
            while len(move_groups) < self.num_threads and move_groups:
                # Split the largest group
                largest_idx = max(range(len(move_groups)), key=lambda i: len(move_groups[i]))
                if len(move_groups[largest_idx]) > 1:
                    mid = len(move_groups[largest_idx]) // 2
                    split_group = move_groups[largest_idx][mid:]
                    move_groups[largest_idx] = move_groups[largest_idx][:mid]
                    move_groups.append(split_group)
            
            # Submit search tasks
            futures = []
            for i, move_group in enumerate(move_groups[:self.num_threads]):
                future = self.executor.submit(
                    self.parallel_minimax_search,
                    board, color, move_group, self.search_depth, i
                )
                futures.append(future)
            
            # Wait for results with timeout
            results = []
            for future in as_completed(futures, timeout=time_limit - 0.1):
                try:
                    result = future.result(timeout=0.1)
                    if result:
                        results.append(result)
                except Exception as e:
                    print(f"⚠️ Thread error: {e}")
            
            # Process results
            if results:
                # Sort by score and get best move
                results.sort(key=lambda x: x[1], reverse=color)
                self.best_move = results[0][0]
                self.best_score = results[0][1]
            
        except Exception as e:
            print(f"❌ Parallel search failed: {e}")
        finally:
            # Stop all threads
            self.stop_flag.set()
            elapsed = time.time() - start_time
            
            # Print statistics
            nodes = self.nodes_searched.get()
            hits = self.tt_hits.get()
            nps = nodes / elapsed if elapsed > 0 else 0
            hit_rate = (hits / nodes * 100) if nodes > 0 else 0
            
            print(f"🏁 Parallel search completed!")
            print(f"⏱️ Time: {elapsed:.2f}s")
            print(f"🔢 Nodes: {nodes:,}")
            print(f"⚡ NPS: {nps:,.0f}")
            print(f"🎯 TT Hits: {hits:,} ({hit_rate:.1f}%)")
            print(f"🧠 Best move: {self.best_move}")
            
            if self.best_score is not None:
                print(f"📊 Score: {self.best_score/100:.2f}")
        
        return self.best_move
    
    def parallel_minimax_search(self, board: List[List[str]], color: bool, 
                               move_group: List, depth: int, thread_id: int) -> Optional[Tuple]:
        """Minimax search for a subset of moves in a separate thread"""
        thread_best_move = None
        thread_best_score = float('-inf') if color else float('inf')
        
        for move in move_group:
            if self.stop_flag.is_set():
                break
                
            new_board = self.make_move(board, move)
            score = self.minimax(new_board, depth - 1, float('-inf'), float('inf'), not color, thread_id)
            
            # Update thread-local best
            if color:  # Maximizing player
                if score > thread_best_score:
                    thread_best_score = score
                    thread_best_move = move
            else:  # Minimizing player
                if score < thread_best_score:
                    thread_best_score = score
                    thread_best_move = move
        
        return (thread_best_move, thread_best_score) if thread_best_move else None
    
    def minimax(self, board: List[List[str]], depth: int, alpha: float, beta: float,
                maximizing_player: bool, thread_id: int) -> int:
        """Standard minimax with thread-safe operations"""
        self.nodes_searched.increment()
        
        # Check stop flag periodically
        if self.nodes_searched.get() % 1000 == 0 and self.stop_flag.is_set():
            return 0
        
        # Terminal conditions
        if depth == 0:
            return self.evaluate_position(board)
        
        moves = self.generate_legal_moves(board, maximizing_player)
        if not moves:
            if self.is_in_check(board, maximizing_player):
                return -100000 - depth if maximizing_player else 100000 + depth
            return 0
        
        # Transposition table lookup (thread-safe)
        board_hash = self.get_board_hash(board, maximizing_player)
        with self.tt_lock:
            if board_hash in self.transposition_table:
                entry = self.transposition_table[board_hash]
                if entry['depth'] >= depth:
                    self.tt_hits.increment()
                    return entry['score']
        
        if maximizing_player:
            max_eval = float('-inf')
            for move in moves:
                new_board = self.make_move(board, move)
                eval_score = self.minimax(new_board, depth - 1, alpha, beta, False, thread_id)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            # Store in TT (thread-safe)
            with self.tt_lock:
                self.transposition_table[board_hash] = {
                    'score': max_eval, 'depth': depth
                }
            return max_eval
        else:
            min_eval = float('inf')
            for move in moves:
                new_board = self.make_move(board, move)
                eval_score = self.minimax(new_board, depth - 1, alpha, beta, True, thread_id)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            # Store in TT (thread-safe)
            with self.tt_lock:
                self.transposition_table[board_hash] = {
                    'score': min_eval, 'depth': depth
                }
            return min_eval
    
    # Utility methods (delegated to existing implementation)
    def generate_legal_moves(self, board: List[List[str]], color: bool) -> List:
        """Generate legal moves - placeholder implementation"""
        # This would integrate with existing move generation logic
        moves = []
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece != '.' and piece.isupper() == color:
                    # Generate moves for this piece (simplified)
                    for to_row in range(8):
                        for to_col in range(8):
                            if self.is_valid_move(board, (row, col), (to_row, to_col)):
                                moves.append(((row, col), (to_row, to_col)))
        return moves
    
    def is_valid_move(self, board: List[List[str]], from_pos: Tuple, to_pos: Tuple) -> bool:
        """Check if move is valid - placeholder"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        piece = board[from_row][from_col]
        
        if piece == '.':
            return False
        
        # Basic validation (would integrate with full rules)
        return 0 <= to_row < 8 and 0 <= to_col < 8 and to_pos != from_pos
    
    def make_move(self, board: List[List[str]], move: Tuple) -> List[List[str]]:
        """Make a move on the board"""
        from_pos, to_pos = move
        new_board = [row[:] for row in board]
        piece = new_board[from_pos[0]][from_pos[1]]
        new_board[to_pos[0]][to_pos[1]] = piece
        new_board[from_pos[0]][from_pos[1]] = '.'
        return new_board
    
    def evaluate_position(self, board: List[List[str]]) -> int:
        """Evaluate position - thread-safe caching"""
        board_hash = self.get_board_hash(board, True)
        
        # Check cache first (thread-safe)
        with self.eval_lock:
            if board_hash in self.eval_cache:
                return self.eval_cache[board_hash]
        
        # Calculate evaluation
        score = self._calculate_material_balance(board)
        
        # Store in cache (thread-safe)
        with self.eval_lock:
            if len(self.eval_cache) < 10000:  # Limit cache size
                self.eval_cache[board_hash] = score
        
        return score
    
    def _calculate_material_balance(self, board: List[List[str]]) -> int:
        """Simple material evaluation"""
        piece_values = {
            'P': 100, 'N': 320, 'B': 330, 'R': 500, 'Q': 900, 'K': 20000,
            'p': -100, 'n': -320, 'b': -330, 'r': -500, 'q': -900, 'k': -20000
        }
        
        score = 0
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece in piece_values:
                    score += piece_values[piece]
        
        return score
    
    def is_in_check(self, board: List[List[str]], is_white: bool) -> bool:
        """Check if king is in check - simplified"""
        # Find king position
        king_char = 'K' if is_white else 'k'
        king_pos = None
        
        for row in range(8):
            for col in range(8):
                if board[row][col] == king_char:
                    king_pos = (row, col)
                    break
            if king_pos:
                break
        
        if not king_pos:
            return False
        
        # Check if any opponent piece attacks the king
        opponent_char = 'prnbqk' if is_white else 'PRNBQK'
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece in opponent_char:
                    if self.is_valid_move(board, (row, col), king_pos):
                        return True
        
        return False
    
    def get_board_hash(self, board: List[List[str]], turn: bool) -> int:
        """Simple board hashing"""
        hash_value = 0
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece != '.':
                    # Simple hash combining position and piece
                    hash_value ^= (ord(piece) << (row * 8 + col)) + (1 if turn else 0)
        return hash_value
    
    def shutdown(self):
        """Clean shutdown of thread pool"""
        self.stop_flag.set()
        self.executor.shutdown(wait=True)
        print("🛑 Multi-threaded AI shut down")

# Test function
def test_parallel_ai():
    """Test the parallel chess AI"""
    print("♔ ♕ ♖ ♗ ♘ ♙ MULTI-THREADED CHESS AI TEST ♟ ♞ ♝ ♜ ♛ ♚")
    print("=" * 60)
    
    # Create AI instance
    ai = ParallelChessAI(search_depth=4, num_threads=4)
    
    # Test board
    test_board = [
        ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
        ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
        ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
    ]
    
    print("Testing parallel search performance...")
    print(f"Threads: {ai.num_threads}")
    print(f"Search depth: {ai.search_depth}")
    print("-" * 40)
    
    # Run test
    start_time = time.perf_counter()
    try:
        move = ai.get_best_move(test_board, True, time_limit=3.0)
        duration = time.perf_counter() - start_time
        
        print(f"✅ Test completed successfully!")
        print(f"⏱️ Time taken: {duration:.2f} seconds")
        print(f"🔢 Total nodes searched: {ai.nodes_searched.get():,}")
        print(f"⚡ Effective NPS: {ai.nodes_searched.get()/duration:,.0f}")
        print(f"🎯 TT hits: {ai.tt_hits.get():,}")
        print(f"🧠 Best move: {move}")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        ai.shutdown()
    
    print("\n🎉 Parallel AI testing complete!")

if __name__ == "__main__":
    test_parallel_ai()