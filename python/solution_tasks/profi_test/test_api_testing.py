# -*- coding: utf-8 -*-
"""
Test script for API testing system
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.api_testing_advanced import APITestRunner, APIDocumentationGenerator

def test_api_testing_system():
    """Test the API testing system"""
    print("Testing API Testing System...")
    
    # Test API test runner
    test_runner = APITestRunner()
    print(f"✓ Created test runner with {len(test_runner.test_cases)} default test cases")
    
    # Test documentation generator
    doc_generator = APIDocumentationGenerator()
    print("✓ Created documentation generator")
    
    # Register a test endpoint
    doc_generator.register_endpoint(
        "/test",
        "GET", 
        {
            "summary": "Test endpoint",
            "description": "A test endpoint for documentation"
        }
    )
    
    # Add example
    doc_generator.add_example(
        "/test",
        "GET",
        {"message": "Hello World"}
    )
    
    # Generate OpenAPI spec
    openapi_spec = doc_generator.generate_openapi_spec()
    print(f"✓ Generated OpenAPI spec with {len(openapi_spec['paths'])} endpoints")
    
    # Generate markdown docs
    markdown_docs = doc_generator.generate_markdown_docs()
    print(f"✓ Generated markdown docs ({len(markdown_docs)} characters)")
    
    print("\nAPI Testing System Test: PASSED")

if __name__ == "__main__":
    test_api_testing_system()