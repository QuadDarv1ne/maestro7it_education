#!/usr/bin/env python3
"""
Упрощенная демонстрация интеграции Stockfish
"""

import subprocess
import os
import time

def test_stockfish_availability():
    """Проверка наличия Stockfish"""
    print("=== ПРОВЕРКА STOCKFISH ===")
    
    # Проверяем возможные пути
    possible_paths = [
        "stockfish-windows-x86-64-avx2.exe",
        "stockfish-windows-x86-64.exe", 
        "stockfish.exe",
        "./stockfish.exe"
    ]
    
    found_path = None
    for path in possible_paths:
        if os.path.exists(path):
            found_path = path
            break
    
    if found_path:
        print(f"✅ Stockfish найден: {found_path}")
        return found_path
    else:
        print("❌ Stockfish не найден в текущей директории")
        print("\nДля использования Stockfish:")
        print("1. Скачайте с https://stockfishchess.org/download/")
        print("2. Поместите исполняемый файл в эту директорию")
        print("3. Переименуйте в stockfish.exe (Windows) или stockfish (Linux/macOS)")
        return None

def simple_stockfish_test(stockfish_path):
    """Простой тест Stockfish"""
    print(f"\n=== ТЕСТ STOCKFISH ===")
    print(f"Путь: {stockfish_path}")
    
    try:
        # Запускаем Stockfish
        process = subprocess.Popen(
            [stockfish_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print("✅ Stockfish запущен успешно")
        
        # Отправляем базовые команды UCI
        commands = [
            "uci\n",
            "isready\n", 
            "quit\n"
        ]
        
        for cmd in commands:
            process.stdin.write(cmd)
            process.stdin.flush()
            time.sleep(0.1)
        
        # Читаем ответ
        output, error = process.communicate(timeout=10)
        
        if "uciok" in output and "readyok" in output:
            print("✅ UCI протокол работает корректно")
            print("✅ Stockfish готов к использованию")
            return True
        else:
            print("❌ Проблемы с UCI протоколом")
            print(f"Output: {output}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка тестирования Stockfish: {e}")
        return False

def demonstrate_stockfish_strength():
    """Демонстрация силы Stockfish"""
    print("\n=== СИЛА STOCKFISH ===")
    print("Stockfish - один из самых сильных шахматных движков в мире:")
    print("🏆 Рейтинг Elo: 3500+")
    print("🏆 Используется в топ-турнирах")
    print("🏆 Чемпион мира по шахматам компьютеров")
    print("🏆 Open-source проект")
    print("🏆 Поддерживает многопоточность")
    print("🏆 Совместимость с UCI протоколом")
    
    print("\nПреимущества интеграции:")
    print("⚡ Мгновенный доступ к профессиональной силе")
    print("⚡ Поддержка глубокого анализа")
    print("⚡ Многопоточная обработка")
    print("⚡ Расширенные опции настройки")
    print("⚡ Совместимость с шахматными GUI")

def main():
    print("STOCKFISH INTEGRATION DEMO")
    print("=" * 40)
    
    # Проверяем наличие Stockfish
    stockfish_path = test_stockfish_availability()
    
    if stockfish_path:
        # Тестируем работу
        if simple_stockfish_test(stockfish_path):
            demonstrate_stockfish_strength()
            print("\n🎉 Интеграция Stockfish готова к использованию!")
        else:
            print("\n❌ Интеграция не удалась")
    else:
        demonstrate_stockfish_strength()
        print("\n📥 Пожалуйста, скачайте Stockfish для полноценной интеграции")

if __name__ == "__main__":
    main()