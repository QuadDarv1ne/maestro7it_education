# -*- coding: utf-8 -*-
"""
Тестовый скрипт для системы тестирования API
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.api_testing_advanced import APITestRunner, APIDocumentationGenerator

def test_api_testing_system():
    """Тестирование системы тестирования API"""
    print("Testing API Testing System...")
    
    # Тестирование раннера API тестов
    test_runner = APITestRunner()
    print(f"✓ Создан раннер тестов с {len(test_runner.test_cases)} тестовыми случаями по умолчанию")
    
    # Тестирование генератора документации
    doc_generator = APIDocumentationGenerator()
    print("✓ Создан генератор документации")
    
    # Регистрация тестовой конечной точки
    doc_generator.register_endpoint(
        "/test",
        "GET", 
        {
            "summary": "Test endpoint",
            "description": "A test endpoint for documentation"
        }
    )
    
    # Добавление примера
    doc_generator.add_example(
        "/test",
        "GET",
        {"message": "Hello World"}
    )
    
    # Генерация спецификации OpenAPI
    openapi_spec = doc_generator.generate_openapi_spec()
    print(f"✓ Сгенерирована спецификация OpenAPI с {len(openapi_spec['paths'])} конечными точками")
    
    # Генерация документации в формате markdown
    markdown_docs = doc_generator.generate_markdown_docs()
    print(f"✓ Сгенерирована документация markdown ({len(markdown_docs)} символов)")
    
    print("\nТест системы тестирования API: ПРОЙДЕН")

if __name__ == "__main__":
    test_api_testing_system()