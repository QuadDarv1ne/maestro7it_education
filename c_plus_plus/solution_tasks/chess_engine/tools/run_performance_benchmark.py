#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Performance Benchmark Runner
Runs the C++ performance benchmark and displays results
"""

import subprocess
import sys
import os
import time
from pathlib import Path

def run_cpp_benchmark():
    """Compile and run the C++ performance benchmark"""
    print("🚀 Running C++ Performance Benchmark...")
    print("=" * 50)
    
    # Change to project directory
    project_dir = Path(__file__).parent.parent
    os.chdir(project_dir)
    
    try:
        # Compile the benchmark
        print("🔧 Compiling benchmark...")
        cmake_build_cmd = ["cmake", "--build", ".", "--config", "Release", "--target", "performance_benchmark"]
        result = subprocess.run(cmake_build_cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print("❌ Compilation failed:")
            print(result.stderr)
            return False
            
        print("✅ Compilation successful!")
        
        # Run the benchmark
        print("\n🏃 Running performance benchmark...")
        benchmark_exe = "./performance_benchmark.exe" if sys.platform == "win32" else "./performance_benchmark"
        
        start_time = time.time()
        result = subprocess.run([benchmark_exe], capture_output=True, text=True)
        end_time = time.time()
        
        if result.returncode == 0:
            print("✅ Benchmark completed successfully!")
            print(f"⏱️  Total execution time: {end_time - start_time:.2f} seconds\n")
            print(result.stdout)
            return True
        else:
            print("❌ Benchmark failed:")
            print(result.stderr)
            return False
            
    except FileNotFoundError:
        print("❌ CMake or compiler not found. Make sure you have CMake installed.")
        return False
    except Exception as e:
        print(f"❌ Error running benchmark: {e}")
        return False

def main():
    """Main function"""
    print("♔ ♕ ♖ ♗ ♘ ♙ CHESS ENGINE PERFORMANCE BENCHMARK RUNNER ♟ ♞ ♝ ♜ ♛ ♚")
    print("=" * 70)
    
    success = run_cpp_benchmark()
    
    if success:
        print("\n🎉 Performance benchmark completed!")
        print("📊 Check the output above for detailed performance metrics.")
    else:
        print("\n❌ Benchmark failed. Check error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()