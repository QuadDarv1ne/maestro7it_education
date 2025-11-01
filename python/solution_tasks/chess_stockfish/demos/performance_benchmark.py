#!/usr/bin/env python3
"""
Performance benchmark for chess_stockfish optimizations.

This script demonstrates the performance improvements achieved through various optimizations.
"""

import time
import sys
import os
import json
from typing import Dict, List
import psutil
import threading

# Add project path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.stockfish_wrapper import StockfishWrapper
from utils.performance_monitor import PerformanceMonitor, PerformanceTimer


def benchmark_board_state_caching():
    """Benchmark board state caching performance."""
    print("🎯 BOARD STATE CACHING BENCHMARK")
    print("=" * 50)
    
    # Create engine
    engine = StockfishWrapper(skill_level=5)
    
    # Test without caching (first call)
    start_time = time.perf_counter()
    for i in range(100):
        board = engine.get_board_state()
    uncached_time = time.perf_counter() - start_time
    
    # Test with caching (subsequent calls)
    start_time = time.perf_counter()
    for i in range(100):
        board = engine.get_board_state()  # These calls should use cache
    cached_time = time.perf_counter() - start_time
    
    speedup = uncached_time / cached_time if cached_time > 0 else float('inf')
    
    print(f"   Without caching: {uncached_time*1000:.2f} ms")
    print(f"   With caching: {cached_time*1000:.2f} ms")
    print(f"   Speedup: {speedup:.1f}x")
    print()
    
    return {
        'uncached_time': uncached_time,
        'cached_time': cached_time,
        'speedup': speedup
    }


def benchmark_move_validation():
    """Benchmark move validation performance."""
    print("🔍 MOVE VALIDATION BENCHMARK")
    print("=" * 50)
    
    # Create engine
    engine = StockfishWrapper(skill_level=5)
    
    # Test moves
    test_moves = ['e2e4', 'd2d4', 'g1f3', 'b1c3', 'c2c4']
    
    # Test without caching
    start_time = time.perf_counter()
    for i in range(50):
        for move in test_moves:
            is_valid = engine.is_move_correct(move)
    uncached_time = time.perf_counter() - start_time
    
    # Test with caching
    start_time = time.perf_counter()
    for i in range(50):
        for move in test_moves:
            is_valid = engine.is_move_correct(move)  # These calls should use cache
    cached_time = time.perf_counter() - start_time
    
    speedup = uncached_time / cached_time if cached_time > 0 else float('inf')
    
    print(f"   Without caching: {uncached_time*1000:.2f} ms")
    print(f"   With caching: {cached_time*1000:.2f} ms")
    print(f"   Speedup: {speedup:.1f}x")
    print()
    
    return {
        'uncached_time': uncached_time,
        'cached_time': cached_time,
        'speedup': speedup
    }


def benchmark_ai_move_generation():
    """Benchmark AI move generation performance."""
    print("🤖 AI MOVE GENERATION BENCHMARK")
    print("=" * 50)
    
    # Create engine
    engine = StockfishWrapper(skill_level=3)  # Lower skill level for faster testing
    
    # Test AI move generation
    start_time = time.perf_counter()
    moves = []
    for i in range(5):
        move = engine.get_best_move(depth=10)
        if move:
            moves.append(move)
    total_time = time.perf_counter() - start_time
    
    avg_time = total_time / len(moves) if moves else 0
    
    print(f"   Generated {len(moves)} moves")
    print(f"   Total time: {total_time*1000:.2f} ms")
    print(f"   Average time per move: {avg_time*1000:.2f} ms")
    print()
    
    return {
        'total_moves': len(moves),
        'total_time': total_time,
        'avg_time_per_move': avg_time
    }


def benchmark_memory_usage():
    """Benchmark memory usage."""
    print("🧠 MEMORY USAGE BENCHMARK")
    print("=" * 50)
    
    # Get initial memory usage
    process = psutil.Process()
    initial_memory = process.memory_info().rss / 1024 / 1024  # MB
    
    # Create multiple engines
    engines = []
    for i in range(10):
        engine = StockfishWrapper(skill_level=5)
        engines.append(engine)
    
    # Get memory usage after creating engines
    engines_memory = process.memory_info().rss / 1024 / 1024  # MB
    
    # Perform operations
    for engine in engines:
        engine.get_board_state()
        engine.get_evaluation()
    
    # Get memory usage after operations
    operations_memory = process.memory_info().rss / 1024 / 1024  # MB
    
    # Clean up
    del engines
    
    # Get final memory usage
    final_memory = process.memory_info().rss / 1024 / 1024  # MB
    
    print(f"   Initial memory: {initial_memory:.2f} MB")
    print(f"   After creating engines: {engines_memory:.2f} MB")
    print(f"   After operations: {operations_memory:.2f} MB")
    print(f"   After cleanup: {final_memory:.2f} MB")
    print(f"   Memory overhead: {operations_memory - initial_memory:.2f} MB")
    print()
    
    return {
        'initial_memory_mb': initial_memory,
        'engines_memory_mb': engines_memory,
        'operations_memory_mb': operations_memory,
        'final_memory_mb': final_memory,
        'memory_overhead_mb': operations_memory - initial_memory
    }


def benchmark_concurrent_operations():
    """Benchmark concurrent operations performance."""
    print("🧵 CONCURRENT OPERATIONS BENCHMARK")
    print("=" * 50)
    
    def worker(results, worker_id):
        """Worker function for concurrent testing."""
        engine = StockfishWrapper(skill_level=3)
        start_time = time.perf_counter()
        
        # Perform operations
        for i in range(10):
            engine.get_board_state()
            engine.get_evaluation()
            
        end_time = time.perf_counter()
        results[worker_id] = end_time - start_time
    
    # Test sequential execution
    start_time = time.perf_counter()
    results_seq = {}
    for i in range(8):
        worker(results_seq, i)
    sequential_time = time.perf_counter() - start_time
    
    # Test concurrent execution
    start_time = time.perf_counter()
    results_concurrent = {}
    threads = []
    
    for i in range(8):
        thread = threading.Thread(target=worker, args=(results_concurrent, i))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    concurrent_time = time.perf_counter() - start_time
    
    speedup = sequential_time / concurrent_time if concurrent_time > 0 else float('inf')
    
    print(f"   Sequential execution: {sequential_time*1000:.2f} ms")
    print(f"   Concurrent execution: {concurrent_time*1000:.2f} ms")
    print(f"   Speedup: {speedup:.1f}x")
    print()
    
    return {
        'sequential_time': sequential_time,
        'concurrent_time': concurrent_time,
        'speedup': speedup
    }


def main():
    """Main benchmark function."""
    print("🚀 PERFORMANCE BENCHMARK FOR CHESS_STOCKFISH")
    print("Optimized Version - Maestro7IT Education")
    print("=" * 60)
    print()
    
    # Initialize performance monitor
    monitor = PerformanceMonitor("performance_benchmark_log.json")
    monitor.start_monitoring(0.1)  # Frequent monitoring for benchmark
    
    results = {}
    
    # Run all benchmarks
    results['board_state_caching'] = benchmark_board_state_caching()
    results['move_validation'] = benchmark_move_validation()
    results['ai_move_generation'] = benchmark_ai_move_generation()
    results['memory_usage'] = benchmark_memory_usage()
    results['concurrent_operations'] = benchmark_concurrent_operations()
    
    # Get performance summary
    summary = monitor.get_performance_summary()
    results['performance_summary'] = summary
    
    # Stop monitoring
    monitor.stop_monitoring()
    monitor.save_log()
    
    # Display final results
    print("=" * 60)
    print("📊 BENCHMARK RESULTS SUMMARY")
    print("=" * 60)
    
    if 'board_state_caching' in results:
        speedup = results['board_state_caching']['speedup']
        print(f"⚡ Board State Caching Speedup: {speedup:.1f}x")
    
    if 'move_validation' in results:
        speedup = results['move_validation']['speedup']
        print(f"✅ Move Validation Speedup: {speedup:.1f}x")
    
    if 'ai_move_generation' in results:
        avg_time = results['ai_move_generation']['avg_time_per_move']
        print(f"🤖 Average AI Move Time: {avg_time*1000:.2f} ms")
    
    if 'memory_usage' in results:
        overhead = results['memory_usage']['memory_overhead_mb']
        print(f"💾 Memory Overhead: {overhead:.2f} MB")
    
    if 'concurrent_operations' in results:
        speedup = results['concurrent_operations']['speedup']
        print(f"🔄 Concurrent Operations Speedup: {speedup:.1f}x")
    
    if 'performance_summary' in results and results['performance_summary']:
        cpu_avg = results['performance_summary']['cpu_usage']['average']
        memory_avg = results['performance_summary']['memory_usage']['process_memory_mb']['average']
        print(f"🖥️  Average CPU Usage: {cpu_avg:.1f}%")
        print(f"💾 Average Memory Usage: {memory_avg:.1f} MB")
    
    print("\n" + "=" * 60)
    print("🎉 BENCHMARK COMPLETED SUCCESSFULLY")
    print("=" * 60)
    
    # Save results to file
    with open("performance_benchmark_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"💾 Results saved to performance_benchmark_results.json")


if __name__ == "__main__":
    main()