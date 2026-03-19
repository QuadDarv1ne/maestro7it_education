#!/usr/bin/env python3
"""
Test suite for Sieve of Eratosthenes OpenCL implementation
"""

import subprocess
import json
import sys
import time
from typing import Dict, List, Any

# Test cases: (N, expected_prime_count_approx)
# Expected counts from known data:
# N=1000 -> 168
# N=10000 -> 1229
# N=100000 -> 9592
# N=500000 -> 41538
# N=1000000 -> 78498
# N=2000000 -> 148933
# N=5000000 -> 348513
# N=10000000 -> 664579

KNOWN_RESULTS = {
    1000: 168,
    10000: 1229,
    50000: 5133,
    100000: 9592,
    500000: 41538,
    1000000: 78498,
    2000000: 148933,
    5000000: 348513,
    10000000: 664579,
}

def run_sieve(n: int, local_size: int = 0, mode: str = "both", 
              no_info: bool = True, json_output: bool = True) -> Dict[str, Any]:
    """Run sieve with given parameters"""
    cmd = ["./sieve.exe", str(n)]
    if local_size > 0:
        cmd.append(str(local_size))
    if mode == "cpu":
        cmd.append("--cpu")
    elif mode == "gpu":
        cmd.append("--gpu")
    if no_info:
        cmd.append("--no-info")
    if json_output:
        cmd.append("--json")
    
    try:
        # Use utf-8 with error handling
        result = subprocess.run(cmd, capture_output=True, timeout=60,
                               encoding='utf-8', errors='ignore')
        
        # Find JSON in output
        stdout = result.stdout if result.stdout else ""
        json_start = stdout.find('{')
        if json_start >= 0:
            json_str = stdout[json_start:]
            return json.loads(json_str)
    except Exception as e:
        print(f"Error running test: {e}")
    return {}

def test_correctness():
    """Test that CPU and GPU produce same results"""
    print("=" * 50)
    print("Test: Correctness")
    print("=" * 50)
    
    test_values = [1000, 10000, 100000, 500000, 1000000]
    passed = 0
    failed = 0
    
    for n in test_values:
        result = run_sieve(n)
        if result.get("correct", False):
            print(f"  N={n:>8}: PASS (count={result['cpu']['count']})")
            passed += 1
        else:
            print(f"  N={n:>8}: FAIL")
            failed += 1
    
    print(f"\nPassed: {passed}/{passed+failed}")
    return failed == 0

def test_known_results():
    """Test against known prime counts"""
    print("\n" + "=" * 50)
    print("Test: Known Results")
    print("=" * 50)
    
    passed = 0
    failed = 0
    
    for n, expected in KNOWN_RESULTS.items():
        result = run_sieve(n)
        actual = result.get("cpu", {}).get("count", 0)
        
        if actual == expected:
            print(f"  N={n:>8}: PASS ({actual} primes)")
            passed += 1
        else:
            diff = abs(actual - expected)
            pct = diff / expected * 100 if expected > 0 else 0
            print(f"  N={n:>8}: FAIL (expected={expected}, got={actual}, diff={diff} ({pct:.1f}%))")
            failed += 1
    
    print(f"\nPassed: {passed}/{passed+failed}")
    return failed == 0

def test_performance():
    """Test performance scaling"""
    print("\n" + "=" * 50)
    print("Test: Performance Scaling")
    print("=" * 50)
    
    test_values = [100000, 500000, 1000000, 2000000]
    
    print(f"{'N':>10} | {'CPU (ms)':>10} | {'GPU (ms)':>12} | {'Speedup':>8}")
    print("-" * 50)
    
    for n in test_values:
        result = run_sieve(n)
        cpu_time = result.get("cpu", {}).get("time_ms", 0)
        gpu_time = result.get("gpu", {}).get("kernel_time_ms", 0)
        speedup = result.get("speedup", 0)
        
        print(f"{n:>10} | {cpu_time:>10.2f} | {gpu_time:>12.3f} | {speedup:>8.1f}x")

def test_gpu_vs_cpu():
    """Test GPU vs CPU selection"""
    print("\n" + "=" * 50)
    print("Test: GPU vs CPU Modes")
    print("=" * 50)
    
    n = 100000
    
    # CPU only
    result_cpu = run_sieve(n, mode="cpu")
    print(f"  CPU mode: {result_cpu.get('cpu', {}).get('count', 'N/A')} primes")
    
    # GPU only
    result_gpu = run_sieve(n, mode="gpu")
    print(f"  GPU mode: {result_gpu.get('gpu', {}).get('count', 'N/A')} primes")
    
    # Both
    result_both = run_sieve(n, mode="both")
    print(f"  Both: CPU={result_both.get('cpu', {}).get('count', 'N/A')}, "
          f"GPU={result_both.get('gpu', {}).get('count', 'N/A')}")

def main():
    print("Sieve of Eratosthenes - Test Suite")
    print("=" * 50)
    
    # Run tests
    all_passed = True
    
    all_passed &= test_correctness()
    all_passed &= test_known_results()
    test_performance()
    test_gpu_vs_cpu()
    
    print("\n" + "=" * 50)
    if all_passed:
        print("All tests PASSED!")
    else:
        print("Some tests FAILED!")
    print("=" * 50)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
