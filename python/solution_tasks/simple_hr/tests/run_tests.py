#!/usr/bin/env python3
"""Test runner for the Simple HR application"""

import unittest
import sys
import os
import coverage

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def run_tests():
    """Run all tests with coverage"""
    # Start coverage
    cov = coverage.Coverage()
    cov.start()
    
    # Discover and run tests
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(__file__)
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Stop coverage and save report
    cov.stop()
    cov.save()
    
    # Print coverage report
    print("\nCoverage Summary:")
    cov.report()
    
    # Generate HTML coverage report
    cov.html_report(directory='htmlcov')
    print("\nHTML coverage report generated in 'htmlcov' directory")
    
    # Return exit code based on test results
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    exit_code = run_tests()
    sys.exit(exit_code)