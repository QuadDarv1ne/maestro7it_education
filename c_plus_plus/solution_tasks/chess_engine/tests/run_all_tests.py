#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test Runner Script
Automatically runs all chess engine tests and generates consolidated reports
"""

import subprocess
import sys
import os
import json
import time
from datetime import datetime
from pathlib import Path

class TestRunner:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.tests_dir = self.project_root / "tests"
        self.reports_dir = self.project_root / "test_reports"
        self.reports_dir.mkdir(exist_ok=True)
        
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "tests_run": [],
            "summary": {
                "total_tests": 0,
                "passed": 0,
                "failed": 0,
                "skipped": 0
            }
        }
    
    def run_cpp_test(self, test_name: str, source_file: str) -> dict:
        """Compile and run C++ test"""
        print(f"\n🔬 Running C++ test: {test_name}")
        print("-" * 50)
        
        source_path = self.tests_dir / source_file
        if not source_path.exists():
            result = {
                "name": test_name,
                "status": "SKIPPED",
                "reason": f"Source file not found: {source_file}"
            }
            print(f"⚠️  Skipped: {result['reason']}")
            return result
        
        # Compile the test
        executable = self.tests_dir / f"{test_name.replace(' ', '_')}_test.exe"
        compile_cmd = [
            "g++", "-std=c++17", "-O2",
            f"-I{self.project_root}/include",
            str(source_path),
            "-o", str(executable)
        ]
        
        try:
            compile_result = subprocess.run(
                compile_cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if compile_result.returncode != 0:
                result = {
                    "name": test_name,
                    "status": "COMPILATION_FAILED",
                    "stderr": compile_result.stderr,
                    "stdout": compile_result.stdout
                }
                print(f"❌ Compilation failed:")
                print(compile_result.stderr)
                return result
            
            # Run the compiled test
            print("✅ Compilation successful. Running test...")
            run_result = subprocess.run(
                [str(executable)],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            # Clean up executable
            if executable.exists():
                executable.unlink()
            
            result = {
                "name": test_name,
                "status": "PASSED" if run_result.returncode == 0 else "FAILED",
                "return_code": run_result.returncode,
                "stdout": run_result.stdout,
                "stderr": run_result.stderr,
                "duration": None  # Could add timing
            }
            
            print(run_result.stdout)
            if run_result.stderr:
                print("STDERR:", run_result.stderr)
            
            return result
            
        except subprocess.TimeoutExpired:
            result = {
                "name": test_name,
                "status": "TIMEOUT",
                "reason": "Test execution timed out"
            }
            print("⏰ Test timed out")
            return result
        except Exception as e:
            result = {
                "name": test_name,
                "status": "ERROR",
                "error": str(e)
            }
            print(f"❌ Error running test: {e}")
            return result
    
    def run_python_test(self, test_name: str, script_file: str) -> dict:
        """Run Python test script"""
        print(f"\n🐍 Running Python test: {test_name}")
        print("-" * 50)
        
        script_path = self.tests_dir / script_file
        if not script_path.exists():
            result = {
                "name": test_name,
                "status": "SKIPPED",
                "reason": f"Script file not found: {script_file}"
            }
            print(f"⚠️  Skipped: {result['reason']}")
            return result
        
        try:
            start_time = time.time()
            result = subprocess.run(
                [sys.executable, str(script_path)],
                capture_output=True,
                text=True,
                timeout=120,
                cwd=str(self.project_root)
            )
            duration = time.time() - start_time
            
            test_result = {
                "name": test_name,
                "status": "PASSED" if result.returncode == 0 else "FAILED",
                "return_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "duration": duration
            }
            
            print(result.stdout)
            if result.stderr:
                print("STDERR:", result.stderr)
            
            return test_result
            
        except subprocess.TimeoutExpired:
            result = {
                "name": test_name,
                "status": "TIMEOUT",
                "reason": "Test execution timed out"
            }
            print("⏰ Test timed out")
            return result
        except Exception as e:
            result = {
                "name": test_name,
                "status": "ERROR",
                "error": str(e)
            }
            print(f"❌ Error running test: {e}")
            return result
    
    def run_all_tests(self):
        """Run all configured tests"""
        print("🧪 CHESS ENGINE COMPREHENSIVE TEST SUITE")
        print("=" * 60)
        print(f"Project: {self.project_root}")
        print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Define test suite
        test_suite = [
            # C++ Tests
            {
                "type": "cpp",
                "name": "Game State Detection",
                "file": "test_game_states.cpp"
            },
            {
                "type": "cpp",
                "name": "Special Moves",
                "file": "test_special_moves.cpp"
            },
            {
                "type": "cpp",
                "name": "Enhanced Game Tests",
                "file": "enhanced_game_tests.cpp"
            },
            {
                "type": "cpp",
                "name": "Comprehensive Special Moves",
                "file": "comprehensive_special_moves.cpp"
            },
            
            # Python Tests
            {
                "type": "python",
                "name": "FastAPI Basic Tests",
                "file": "test_fastapi.py"
            },
            {
                "type": "python",
                "name": "Enhanced FastAPI Tests",
                "file": "enhanced_fastapi_test.py"
            }
        ]
        
        # Run each test
        for test_config in test_suite:
            if test_config["type"] == "cpp":
                result = self.run_cpp_test(test_config["name"], test_config["file"])
            else:  # python
                result = self.run_python_test(test_config["name"], test_config["file"])
            
            self.results["tests_run"].append(result)
            
            # Update summary
            self.results["summary"]["total_tests"] += 1
            if result["status"] == "PASSED":
                self.results["summary"]["passed"] += 1
            elif result["status"] in ["FAILED", "COMPILATION_FAILED", "ERROR", "TIMEOUT"]:
                self.results["summary"]["failed"] += 1
            else:
                self.results["summary"]["skipped"] += 1
        
        # Generate final report
        self.generate_final_report()
    
    def generate_final_report(self):
        """Generate comprehensive test report"""
        print("\n" + "=" * 60)
        print("📊 FINAL TEST RESULTS SUMMARY")
        print("=" * 60)
        
        summary = self.results["summary"]
        print(f"Total Tests: {summary['total_tests']}")
        print(f"✅ Passed: {summary['passed']}")
        print(f"❌ Failed: {summary['failed']}")
        print(f"⚠️  Skipped: {summary['skipped']}")
        
        if summary['total_tests'] > 0:
            success_rate = (summary['passed'] / summary['total_tests']) * 100
            print(f"Success Rate: {success_rate:.1f}%")
        
        # Show failed tests
        failed_tests = [t for t in self.results["tests_run"] if t["status"] != "PASSED"]
        if failed_tests:
            print(f"\n❌ Failed/Skipped Tests ({len(failed_tests)}):")
            for test in failed_tests:
                print(f"  • {test['name']}: {test['status']}")
                if "reason" in test:
                    print(f"    Reason: {test['reason']}")
                elif "error" in test:
                    print(f"    Error: {test['error']}")
        
        # Save detailed report
        report_file = self.reports_dir / f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"\n📋 Detailed report saved to: {report_file}")
        
        # Overall status
        if summary['failed'] == 0 and summary['passed'] > 0:
            print("\n🎉 All executed tests passed! Engine is working correctly.")
            return 0
        elif summary['passed'] > 0:
            print(f"\n⚠️  {summary['failed']} tests failed. Review the report above.")
            return 1
        else:
            print("\n❌ No tests were successfully executed.")
            return 2

def main():
    """Main entry point"""
    runner = TestRunner()
    
    try:
        runner.run_all_tests()
        return 0
    except KeyboardInterrupt:
        print("\n\n🛑 Test execution interrupted by user")
        return 1
    except Exception as e:
        print(f"\n💥 Test runner failed with error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())