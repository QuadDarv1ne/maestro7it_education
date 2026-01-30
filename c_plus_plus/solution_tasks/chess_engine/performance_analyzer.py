#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Performance Analysis Tool for Chess Engine
Analyzes bottlenecks and provides optimization recommendations
"""

import time
import cProfile
import pstats
import io
import psutil
import gc
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt
import numpy as np

class PerformanceAnalyzer:
    """Comprehensive performance analyzer for chess engine"""
    
    def __init__(self):
        self.metrics = {}
        self.baseline_results = {}
        
    def measure_memory_usage(self) -> Dict[str, float]:
        """Measure current memory usage"""
        process = psutil.Process()
        memory_info = process.memory_info()
        
        return {
            'rss_mb': memory_info.rss / 1024 / 1024,  # Resident Set Size
            'vms_mb': memory_info.vms / 1024 / 1024,  # Virtual Memory Size
            'percent': process.memory_percent()
        }
    
    def profile_function(self, func, *args, **kwargs) -> Dict:
        """Profile a function and return performance metrics"""
        pr = cProfile.Profile()
        start_time = time.perf_counter()
        start_memory = self.measure_memory_usage()
        
        # Run function with profiling
        pr.enable()
        result = func(*args, **kwargs)
        pr.disable()
        
        end_time = time.perf_counter()
        end_memory = self.measure_memory_usage()
        
        # Get profiling stats
        s = io.StringIO()
        ps = pstats.Stats(pr, stream=s)
        ps.sort_stats('cumulative')
        ps.print_stats(20)  # Top 20 functions
        
        return {
            'execution_time': end_time - start_time,
            'memory_used': end_memory['rss_mb'] - start_memory['rss_mb'],
            'result': result,
            'profile_stats': s.getvalue()
        }
    
    def analyze_move_generation_performance(self):
        """Analyze move generation performance"""
        print("🔍 Analyzing Move Generation Performance...")
        
        # Test different board positions
        test_positions = [
            # Starting position
            ('start', [
                ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
                ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
            ]),
            # Mid-game position with many pieces
            ('mid_game', [
                ['r', '.', 'b', 'q', 'k', '.', 'n', 'r'],
                ['p', 'p', 'p', '.', '.', 'p', 'p', 'p'],
                ['.', '.', 'n', '.', '.', '.', '.', '.'],
                ['.', '.', '.', 'p', 'p', '.', '.', '.'],
                ['.', '.', '.', 'P', 'P', '.', '.', '.'],
                ['.', '.', '.', '.', '.', 'N', '.', '.'],
                ['P', 'P', 'P', '.', '.', 'P', 'P', 'P'],
                ['R', '.', 'B', 'Q', 'K', 'B', '.', 'R']
            ]),
            # Endgame position
            ('endgame', [
                ['.', '.', '.', '.', 'k', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', 'K', '.', '.', '.']
            ])
        ]
        
        results = {}
        
        for pos_name, board in test_positions:
            print(f"\nTesting {pos_name} position...")
            
            # Import and initialize engine
            from chess_engine_wrapper import ChessEngineWrapper
            engine = ChessEngineWrapper()
            engine.board_state = board
            
            # Profile move generation
            def generate_all_moves():
                moves = []
                for row in range(8):
                    for col in range(8):
                        piece = engine.board_state[row][col]
                        if piece != '.':
                            # Generate moves for this piece (simplified)
                            for to_row in range(8):
                                for to_col in range(8):
                                    if engine.is_valid_move((row, col), (to_row, to_col)):
                                        moves.append(((row, col), (to_row, to_col)))
                return moves
            
            profile_result = self.profile_function(generate_all_moves)
            results[pos_name] = profile_result
            
            print(f"  Execution time: {profile_result['execution_time']:.4f}s")
            print(f"  Memory used: {profile_result['memory_used']:.2f}MB")
            print(f"  Valid moves found: {len(profile_result['result'])}")
        
        return results
    
    def analyze_ai_performance(self):
        """Analyze AI decision-making performance"""
        print("\n🤖 Analyzing AI Performance...")
        
        from chess_engine_wrapper import ChessEngineWrapper
        engine = ChessEngineWrapper()
        
        # Test AI response time at different depths
        depths = [1, 2, 3, 4]
        results = {}
        
        for depth in depths:
            print(f"\nTesting AI at depth {depth}...")
            
            def ai_move():
                # Simulate AI thinking (simplified minimax)
                best_move = None
                best_score = float('-inf')
                
                # Generate all possible moves
                moves = []
                for row in range(8):
                    for col in range(8):
                        piece = engine.board_state[row][col]
                        if piece != '.' and piece.isupper():  # White pieces
                            for to_row in range(8):
                                for to_col in range(8):
                                    if engine.is_valid_move((row, col), (to_row, to_col)):
                                        moves.append(((row, col), (to_row, to_col)))
                
                # Evaluate each move (simplified)
                for move in moves[:10]:  # Limit for testing
                    from_pos, to_pos = move
                    # Simple evaluation
                    score = self.simple_position_evaluator(engine.board_state, to_pos)
                    if score > best_score:
                        best_score = score
                        best_move = move
                
                return best_move
            
            profile_result = self.profile_function(ai_move)
            results[f'depth_{depth}'] = profile_result
            
            print(f"  Execution time: {profile_result['execution_time']:.4f}s")
            print(f"  Memory used: {profile_result['memory_used']:.2f}MB")
        
        return results
    
    def simple_position_evaluator(self, board, target_pos):
        """Simple position evaluator for testing"""
        to_row, to_col = target_pos
        target_piece = board[to_row][to_col]
        
        # Basic material evaluation
        piece_values = {
            '.': 0, 'p': 1, 'n': 3, 'b': 3, 'r': 5, 'q': 9, 'k': 100,
            'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 100
        }
        
        # Center control bonus
        center_bonus = 0
        if 2 <= to_row <= 5 and 2 <= to_col <= 5:
            center_bonus = 0.5
        
        return piece_values.get(target_piece.lower(), 0) + center_bonus
    
    def analyze_web_interface_performance(self):
        """Analyze web interface performance"""
        print("\n🌐 Analyzing Web Interface Performance...")
        
        # Test HTML rendering performance
        def render_board():
            # Simulate board rendering
            html = '<div class="chess-board">'
            for row in range(8):
                for col in range(8):
                    piece = 'KQRBNPkqrbnp.'[row % 13]  # Simulated pieces
                    html += f'<div class="square">{piece}</div>'
            html += '</div>'
            return html
        
        profile_result = self.profile_function(render_board)
        
        print(f"  Board rendering time: {profile_result['execution_time']:.6f}s")
        print(f"  Memory used: {profile_result['memory_used']:.2f}MB")
        
        return {'rendering': profile_result}
    
    def generate_performance_report(self):
        """Generate comprehensive performance report"""
        print("📊 Generating Performance Report...")
        print("=" * 50)
        
        # Run all analyses
        move_gen_results = self.analyze_move_generation_performance()
        ai_results = self.analyze_ai_performance()
        web_results = self.analyze_web_interface_performance()
        
        # Memory analysis
        memory_usage = self.measure_memory_usage()
        
        # Generate report
        report = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'memory_usage': memory_usage,
            'move_generation': move_gen_results,
            'ai_performance': ai_results,
            'web_performance': web_results
        }
        
        # Print summary
        print("\n📈 PERFORMANCE SUMMARY:")
        print("=" * 30)
        print(f"Current Memory Usage: {memory_usage['rss_mb']:.2f} MB")
        print(f"CPU Usage: {psutil.cpu_percent()}%")
        
        print("\n⏱️  MOVE GENERATION:")
        for pos_name, result in move_gen_results.items():
            print(f"  {pos_name}: {result['execution_time']:.4f}s ({len(result['result'])} moves)")
        
        print("\n🧠 AI PERFORMANCE:")
        for depth_key, result in ai_results.items():
            depth = depth_key.split('_')[1]
            print(f"  Depth {depth}: {result['execution_time']:.4f}s")
        
        print("\n🌐 WEB INTERFACE:")
        print(f"  Rendering: {web_results['rendering']['execution_time']:.6f}s")
        
        # Identify bottlenecks
        print("\n⚠️  IDENTIFIED BOTTLENECKS:")
        bottlenecks = self.identify_bottlenecks(report)
        for bottleneck in bottlenecks:
            print(f"  • {bottleneck}")
        
        # Recommendations
        print("\n💡 OPTIMIZATION RECOMMENDATIONS:")
        recommendations = self.generate_recommendations(report)
        for rec in recommendations:
            print(f"  • {rec}")
        
        return report
    
    def identify_bottlenecks(self, report):
        """Identify performance bottlenecks"""
        bottlenecks = []
        
        # Check move generation times
        for pos_name, result in report['move_generation'].items():
            if result['execution_time'] > 0.1:  # Threshold
                bottlenecks.append(f"Slow move generation in {pos_name} position ({result['execution_time']:.4f}s)")
        
        # Check AI performance
        for depth_key, result in report['ai_performance'].items():
            depth = int(depth_key.split('_')[1])
            expected_time = 0.1 * (depth ** 2)  # Rough estimation
            if result['execution_time'] > expected_time:
                bottlenecks.append(f"AI too slow at depth {depth} ({result['execution_time']:.4f}s)")
        
        # Check memory usage
        if report['memory_usage']['rss_mb'] > 100:
            bottlenecks.append(f"High memory usage: {report['memory_usage']['rss_mb']:.2f} MB")
        
        return bottlenecks
    
    def generate_recommendations(self, report):
        """Generate optimization recommendations"""
        recommendations = []
        
        # Move generation recommendations
        move_times = [r['execution_time'] for r in report['move_generation'].values()]
        avg_move_time = sum(move_times) / len(move_times)
        
        if avg_move_time > 0.05:
            recommendations.append("Implement bitboard representation for faster move generation")
            recommendations.append("Add move ordering heuristics to reduce search space")
            recommendations.append("Consider transposition tables for repeated positions")
        
        # AI recommendations
        ai_times = [r['execution_time'] for r in report['ai_performance'].values()]
        if any(t > 1.0 for t in ai_times):
            recommendations.append("Implement iterative deepening with time management")
            recommendations.append("Add alpha-beta pruning optimization")
            recommendations.append("Use opening book for early game moves")
        
        # Memory recommendations
        if report['memory_usage']['rss_mb'] > 100:
            recommendations.append("Implement garbage collection strategy")
            recommendations.append("Optimize data structures to reduce memory footprint")
            recommendations.append("Consider lazy evaluation where possible")
        
        # Web recommendations
        web_time = report['web_performance']['rendering']['execution_time']
        if web_time > 0.001:
            recommendations.append("Optimize HTML rendering with virtual DOM")
            recommendations.append("Implement client-side caching for board states")
            recommendations.append("Add loading indicators for better UX")
        
        return recommendations

def main():
    """Main analysis function"""
    print("♔ ♕ ♖ ♗ ♘ ♙ CHESS ENGINE PERFORMANCE ANALYSIS ♟ ♞ ♝ ♜ ♛ ♚")
    print("=" * 60)
    
    analyzer = PerformanceAnalyzer()
    report = analyzer.generate_performance_report()
    
    # Save report to file
    import json
    with open('performance_analysis_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Detailed report saved to: performance_analysis_report.json")
    print("✅ Analysis complete!")

if __name__ == "__main__":
    main()