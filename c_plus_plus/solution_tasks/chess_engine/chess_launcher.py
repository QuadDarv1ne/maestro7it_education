#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Улучшенный лаунчер шахматной игры
Главное меню с расширенными возможностями и улучшенной обработкой ошибок
"""

import os
import sys
import subprocess
import platform
import time
from pathlib import Path
from typing import Optional, Dict, Any

def clear_screen():
    """Очистка экрана терминала"""
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
    except Exception:
        pass  # Игнорируем ошибки очистки экрана

def print_header():
    """Вывод главного заголовка"""
    print("♔ ♕ ♖ ♗ ♘ ♙  ШАХМАТЫ  ♟ ♞ ♝ ♜ ♛ ♚")
    print("=" * 50)
    print("    ВЫБЕРИТЕ РЕЖИМ ИГРЫ")
    print("=" * 50)
    print()
    
    # Показываем информацию о системе
    try:
        python_ver = sys.version.split()[0]
        system_info = f"Python {python_ver} | {platform.system()} {platform.release()}"
        print(f"💻 {system_info}")
        print()
    except Exception:
        pass

def show_menu():
    """Отображение главного меню"""
    print("📋 ДОСТУПНЫЕ РЕЖИМЫ:")
    print()
    print("  1. 🖥️  Консольная версия (терминал)")
    print("     • Текстовый интерфейс")
    print("     • Юникод символы фигур")
    print("     • Работает на всех системах")
    print("     • Быстрый запуск")
    print()
    print("  2. 🎮 Графическая версия (pygame)")
    print("     • Полноценный GUI")
    print("     • Анимация ходов")
    print("     • Мышиный интерфейс")
    print("     • Требует установку pygame")
    print()
    print("  3. 🔧 Сервисные утилиты")
    print("     • Тестирование движка")
    print("     • Анализ производительности")
    print("     • Проверка оптимизаций")
    print()
    print("  4. ⚡ Веб-версия (FastAPI)")
    print("     • Высокая производительность")
    print("     • Современная архитектура")
    print("     • RESTful API")
    print("     • WebSocket поддержка")
    print()
    print("  5. 🌐 Веб-интерфейс (HTML5)")
    print("     • Современный дизайн")
    print("     • Адаптивная верстка")
    print("     • Работает в браузере")
    print("     • Не требует установки")
    print()
    print("  6. 🚪 Выход")
    print()
    print("-" * 50)

def check_dependencies(dependencies: list) -> Dict[str, bool]:
    """Проверка установленных зависимостей"""
    results = {}
    for dep in dependencies:
        try:
            __import__(dep)
            results[dep] = True
        except ImportError:
            results[dep] = False
    return results

def check_pygame():
    """Проверка установки pygame"""
    return check_dependencies(['pygame'])['pygame']

def install_package(package_name: str) -> bool:
    """Универсальная функция установки пакета"""
    print(f"🔧 {package_name} не найден. Пытаюсь установить...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name], 
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"✅ {package_name} успешно установлен!")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Не удалось установить {package_name} автоматически")
        print(f"Попробуйте вручную: pip install {package_name}")
        return False
    except Exception as e:
        print(f"❌ Ошибка установки {package_name}: {e}")
        return False

def install_pygame():
    """Попытка установки pygame"""
    return install_package("pygame")

def run_terminal_version():
    """Запуск терминальной шахматной игры"""
    print("🖥️  Запуск консольной версии...")
    print()
    try:
        # Проверяем наличие файла
        module_path = Path(__file__).parent / "interfaces" / "full_chess_game.py"
        if not module_path.exists():
            print("❌ Файл full_chess_game.py не найден!")
            input("Нажмите Enter для возврата в меню...")
            return
            
        from interfaces.full_chess_game import FullChessGame
        print("✅ Интерфейс загружен. Запуск игры...")
        time.sleep(0.5)
        game = FullChessGame()
        game.run()
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        print("Проверьте наличие всех необходимых файлов.")
        input("Нажмите Enter для возврата в меню...")
    except Exception as e:
        print(f"❌ Ошибка запуска: {e}")
        input("Нажмите Enter для возврата в меню...")

def run_graphical_version():
    """Запуск графической шахматной игры с Python 3.13.11"""
    print("🎮 Запуск графической версии (Python 3.13.11)...")
    print()
    
    # Проверка доступности pygame
    if not check_pygame():
        print("⚠️  Pygame не установлен!")
        print("Для лучшего качества изображения рекомендуется установить pygame.")
        choice = input("Установить pygame автоматически? (y/n): ").strip().lower()
        if choice == 'y':
            if not install_pygame():
                print("Вы можете продолжить без pygame, но будет использована консольная версия.")
                choice2 = input("Запустить консольную версию вместо этого? (y/n): ").strip().lower()
                if choice2 == 'y':
                    run_terminal_version()
                    return
                input("Нажмите Enter для возврата в меню...")
                return
        else:
            choice2 = input("Запустить консольную версию вместо этого? (y/n): ").strip().lower()
            if choice2 == 'y':
                run_terminal_version()
                return
            print("Для графической версии нужен pygame!")
            input("Нажмите Enter для возврата в меню...")
            return
    
    # Запуск pygame версии с Python 3.13.11
    try:
        print("✅ Pygame найден. Загрузка графического интерфейса...")
        print("🐍 Используется Python 3.13.11 для оптимальной производительности...")
        
        # Запуск через subprocess с явным указанием Python 3.13.11
        pygame_script = Path(__file__).parent / "interfaces" / "pygame_chess.py"
        if pygame_script.exists():
            print("🎮 Запуск игры...")
            time.sleep(0.5)
            subprocess.run(["py", "-3.13", str(pygame_script)])
        else:
            # Альтернативный импорт если subprocess не сработает
            from interfaces.pygame_chess import PygameChessGUI
            game = PygameChessGUI()
            game.run()
            
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        print("Попробуйте установить недостающие зависимости")
        input("Нажмите Enter для возврата в меню...")
    except FileNotFoundError:
        print("❌ Python 3.13.11 не найден! Попробуйте установить Python 3.13.11")
        print("Скачайте с: https://www.python.org/downloads/")
        input("Нажмите Enter для возврата в меню...")
    except Exception as e:
        print(f"❌ Ошибка запуска: {e}")
        print("Попробуйте запустить консольную версию как альтернативу.")
        choice = input("Запустить консольную версию вместо этого? (y/n): ").strip().lower()
        if choice == 'y':
            run_terminal_version()
        else:
            input("Нажмите Enter для возврата в меню...")

def run_utilities_menu():
    """Запуск сервисных утилит"""
    while True:
        clear_screen()
        print("🔧 СЕРВИСНЫЕ УТИЛИТЫ")
        print("=" * 30)
        print()
        print("  1. 🧪 Тестирование движка")
        print("  2. 📊 Анализ производительности")
        print("  3. 🔍 Проверка оптимизаций")
        print("  4. 📈 Статистика движка")
        print("  5. ⬅️  Назад в главное меню")
        print()
        print("-" * 30)
        
        try:
            choice = input("Выберите утилиту (1-5): ").strip()
            
            if choice == '1':
                run_engine_tests()
            elif choice == '2':
                run_performance_analysis()
            elif choice == '3':
                run_optimization_check()
            elif choice == '4':
                show_engine_stats()
            elif choice == '5':
                break
            else:
                print("❌ Неверный выбор. Введите число от 1 до 5.")
                time.sleep(1.5)
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            time.sleep(2)

def run_engine_tests():
    """Запуск тестов движка"""
    print("🧪 Запуск тестов движка...")
    try:
        # Поиск тестовых файлов
        test_files = [
            "tests/test_game_states.cpp",
            "tests/test_special_moves.cpp",
            "src/comprehensive_tester.py"
        ]
        
        available_tests = [f for f in test_files if Path(f).exists()]
        
        if not available_tests:
            print("❌ Тестовые файлы не найдены!")
            input("Нажмите Enter для возврата...")
            return
        
        print("Найдены тесты:")
        for i, test_file in enumerate(available_tests, 1):
            print(f"  {i}. {test_file}")
        
        choice = input("\nВыберите тест для запуска (или Enter для всех): ").strip()
        
        if not choice:
            # Запуск всех тестов
            for test_file in available_tests:
                print(f"\n🚀 Запуск {test_file}...")
                if test_file.endswith('.py'):
                    subprocess.run([sys.executable, test_file])
                else:
                    print(f"Компиляция и запуск {test_file}...")
                    # Здесь можно добавить компиляцию C++
        elif choice.isdigit() and 1 <= int(choice) <= len(available_tests):
            test_file = available_tests[int(choice) - 1]
            print(f"\n🚀 Запуск {test_file}...")
            if test_file.endswith('.py'):
                subprocess.run([sys.executable, test_file])
            else:
                print("Для C++ файлов требуется компиляция.")
        else:
            print("❌ Неверный выбор.")
            
    except Exception as e:
        print(f"❌ Ошибка запуска тестов: {e}")
    
    input("\nНажмите Enter для возврата...")

def run_performance_analysis():
    """Анализ производительности"""
    print("📊 Анализ производительности...")
    try:
        perf_script = Path("tools/performance_analyzer.py")
        if perf_script.exists():
            subprocess.run([sys.executable, str(perf_script)])
        else:
            print("⚠️  Скрипт анализа не найден. Запуск быстрого теста...")
            # Быстрый тест производительности
            import time
            start_time = time.time()
            
            # Имитация работы движка
            try:
                from core.enhanced_chess_ai import EnhancedChessAI
                ai = EnhancedChessAI(search_depth=3)
                test_time = time.time() - start_time
                print(f"✅ AI инициализирован за {test_time:.3f} секунд")
            except Exception as e:
                print(f"⚠️  Быстрый тест: {e}")
                
    except Exception as e:
        print(f"❌ Ошибка анализа: {e}")
    
    input("\nНажмите Enter для возврата...")

def run_optimization_check():
    """Проверка оптимизаций"""
    print("🔍 Проверка оптимизаций...")
    try:
        opt_script = Path("src/analysis_integration.py")
        if opt_script.exists():
            subprocess.run([sys.executable, str(opt_script)])
        else:
            print("ℹ️  Подробный анализ недоступен. Показ основной информации:")
            deps = check_dependencies(['pygame', 'fastapi', 'uvicorn'])
            print("\nУстановленные зависимости:")
            for dep, installed in deps.items():
                status = "✅" if installed else "❌"
                print(f"  {status} {dep}")
    except Exception as e:
        print(f"❌ Ошибка проверки: {e}")
    
    input("\nНажмите Enter для возврата...")

def show_engine_stats():
    """Показ статистики движка"""
    print("📈 Статистика шахматного движка")
    print("=" * 40)
    
    try:
        # Базовая информация
        print(f"Python версия: {sys.version.split()[0]}")
        print(f"Платформа: {platform.system()} {platform.release()}")
        print(f"Архитектура: {platform.machine()}")
        
        # Проверка зависимостей
        deps = check_dependencies(['pygame', 'fastapi', 'uvicorn', 'numpy'])
        print("\nЗависимости:")
        for dep, installed in deps.items():
            status = "✅ Установлен" if installed else "❌ Не установлен"
            print(f"  {dep}: {status}")
            
        # Размер проекта
        project_dir = Path(__file__).parent
        total_files = sum(1 for _ in project_dir.rglob("*.py"))
        cpp_files = sum(1 for _ in project_dir.rglob("*.cpp"))
        hpp_files = sum(1 for _ in project_dir.rglob("*.hpp"))
        
        print(f"\nСтруктура проекта:")
        print(f"  Python файлов: {total_files}")
        print(f"  C++ файлов: {cpp_files}")
        print(f"  Заголовочных файлов: {hpp_files}")
        
    except Exception as e:
        print(f"❌ Ошибка получения статистики: {e}")
    
    input("\nНажмите Enter для возврата...")

def run_fastapi_web_version():
    """Запуск FastAPI веб-сервера шахмат"""
    print("⚡ Запуск FastAPI веб-сервера...")
    print()
    
    # Проверка зависимостей
    deps = check_dependencies(['fastapi', 'uvicorn'])
    missing_deps = [dep for dep, installed in deps.items() if not installed]
    
    if missing_deps:
        print(f"⚠️  Отсутствуют зависимости: {', '.join(missing_deps)}")
        choice = input("Установить недостающие библиотеки? (y/n): ").strip().lower()
        if choice == 'y':
            print("🔧 Устанавливаю зависимости...")
            success = True
            for dep in missing_deps:
                if not install_package(dep if dep != 'uvicorn' else 'uvicorn[standard]'):
                    success = False
                    break
            
            if not success:
                print("❌ Не удалось установить все зависимости")
                input("Нажмите Enter для возврата в меню...")
                return
            print("✅ Все зависимости установлены!")
        else:
            print("Для FastAPI версии нужны fastapi и uvicorn!")
            input("Нажмите Enter для возврата в меню...")
            return
    
    # Проверка наличия файла сервера
    server_file = Path("interfaces/fastapi_chess.py")
    if not server_file.exists():
        print("❌ Файл сервера fastapi_chess.py не найден!")
        input("Нажмите Enter для возврата в меню...")
        return
    
    # Запуск FastAPI сервера
    try:
        print("🚀 Запуск FastAPI сервера...")
        print("🌐 Сервер будет доступен по адресу: http://localhost:8000")
        print("📚 Документация API: http://localhost:8000/docs")
        print("⌨️  Нажмите Ctrl+C для остановки сервера")
        print("💡 Откройте браузер и перейдите по адресу выше")
        print()
        
        # Запуск с uvicorn напрямую для лучшего контроля
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "interfaces.fastapi_chess:app", 
            "--host", "localhost", 
            "--port", "8000",
            "--reload"
        ])
            
    except KeyboardInterrupt:
        print("\n\n🛑 Сервер остановлен пользователем")
        print("Спасибо за использование веб-интерфейса!")
    except Exception as e:
        print(f"❌ Ошибка запуска сервера: {e}")
        print("Проверьте, что порт 8000 свободен.")
        input("Нажмите Enter для возврата в меню...")

def run_websocket_server():
    """Запуск WebSocket сервера для мультиплеера"""
    print("🌐 Запуск WebSocket сервера для мультиплеера...")
    print()
    
    try:
        # Проверяем наличие серверного скрипта
        server_script = Path(__file__).parent / "web" / "chess_websocket_server.py"
        if not server_script.exists():
            print("❌ Файл chess_websocket_server.py не найден")
            input("Нажмите Enter для возврата в меню...")
            return
        
        print("✅ Серверный скрипт найден")
        print("🚀 Запуск WebSocket сервера...")
        print()
        print("♔ ♕ ♖ ♗ ♘ ♙ ШАХМАТНЫЙ WEBSOCKET СЕРВЕР ♟ ♞ ♝ ♜ ♛ ♚")
        print("=" * 55)
        print("🌐 WebSocket сервер запущен на: ws://localhost:8765")
        print("🎮 Готов принимать соединения для онлайн-игр")
        print("🔄 Нажмите Ctrl+C для остановки сервера")
        print("=" * 55)
        print()
        
        # Запуск сервера
        subprocess.run([sys.executable, str(server_script)])
        
    except KeyboardInterrupt:
        print("\n🛑 WebSocket сервер остановлен пользователем")
    except Exception as e:
        print(f"❌ Ошибка запуска WebSocket сервера: {e}")
        input("Нажмите Enter для возврата в меню...")

def run_web_interface():
    """Запуск веб-интерфейса HTML5"""
    print("🌐 Запуск веб-интерфейса...")
    print()
    
    try:
        # Проверяем наличие серверного скрипта
        server_script = Path(__file__).parent / "web" / "chess_server.py"
        if not server_script.exists():
            print("❌ Файл chess_server.py не найден")
            input("Нажмите Enter для возврата в меню...")
            return
        
        print("✅ Серверный скрипт найден")
        print("🚀 Запуск веб-сервера...")
        print()
        print("♔ ♕ ♖ ♗ ♘ ♙ ШАХМАТНЫЙ ВЕБ-ИНТЕРФЕЙС ♟ ♞ ♝ ♜ ♛ ♚")
        print("=" * 50)
        print("🌐 Сервер запущен на: http://localhost:8080")
        print("🎮 Интерфейс доступен по адресу выше")
        print("🔄 Нажмите Ctrl+C для остановки сервера")
        print("=" * 50)
        print()
        
        # Запуск сервера
        subprocess.run([sys.executable, str(server_script)])
        
    except KeyboardInterrupt:
        print("\n🛑 Сервер остановлен пользователем")
    except Exception as e:
        print(f"❌ Ошибка запуска веб-интерфейса: {e}")
        input("Нажмите Enter для возврата в меню...")


def main():
    """Главный цикл меню"""
    print("🚀 Запуск шахматного лаунчера...")
    time.sleep(0.5)
    
    while True:
        clear_screen()
        print_header()
        show_menu()
        
        try:
            choice = input("Введите номер варианта (1-7): ").strip()
                        
            if choice == '1':
                run_terminal_version()
            elif choice == '2':
                run_graphical_version()
            elif choice == '3':
                run_utilities_menu()
            elif choice == '4':
                run_fastapi_web_version()
            elif choice == '5':
                run_web_interface()
            elif choice == '6':
                run_websocket_server()
            elif choice == '7':
                print("\n👋 До свидания. Спасибо за игру")
                print("♟️  Возвращайтесь снова! ♔")
                break
            else:
                print("❌ Неверный выбор. Введите число от 1 до 7.")
                time.sleep(1.5)
                
        except KeyboardInterrupt:
            print("\n\n👋 Программа прервана пользователем До свидания!")
            print("♟️  Игра сохранена. Возвращайтесь снова")
            break
        except Exception as e:
            print(f"❌ Произошла непредвиденная ошибка: {e}")
            print("🔄 Перезапуск меню...")
            time.sleep(2)

if __name__ == "__main__":
    main()