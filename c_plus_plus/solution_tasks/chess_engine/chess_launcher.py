#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Chess Game Launcher
Main menu to choose between terminal and graphical interface
"""

import os
import sys
import subprocess

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the main header"""
    print("♔ ♕ ♖ ♗ ♘ ♙  ШАХМАТЫ  ♟ ♞ ♝ ♜ ♛ ♚")
    print("=" * 40)
    print("    ВЫБЕРИТЕ РЕЖИМ ИГРЫ")
    print("=" * 40)
    print()

def show_menu():
    """Show the main menu"""
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
    print("  3. ❌ Выход")
    print()
    print("-" * 40)

def check_pygame():
    """Check if pygame is installed"""
    try:
        import pygame
        return True
    except ImportError:
        return False

def install_pygame():
    """Attempt to install pygame"""
    print("🔧 Pygame не найден. Пытаюсь установить...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
        print("✅ Pygame успешно установлен!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Не удалось установить pygame автоматически")
        print("Попробуйте вручную: pip install pygame")
        return False
    except Exception as e:
        print(f"❌ Ошибка установки: {e}")
        return False

def run_terminal_version():
    """Run the terminal chess game"""
    print("🚀 Запуск консольной версии...")
    print()
    try:
        from full_chess_game import FullChessGame
        game = FullChessGame()
        game.run()
    except Exception as e:
        print(f"❌ Ошибка запуска: {e}")
        input("Нажмите Enter для возврата в меню...")

def run_graphical_version():
    """Run the graphical chess game"""
    print("🎮 Запуск графической версии...")
    print()
    
    # Check if pygame is available
    if not check_pygame():
        print("⚠️  Pygame не установлен!")
        choice = input("Установить pygame автоматически? (y/n): ").strip().lower()
        if choice == 'y':
            if not install_pygame():
                input("Нажмите Enter для возврата в меню...")
                return
        else:
            print("Для графической версии нужен pygame!")
            input("Нажмите Enter для возврата в меню...")
            return
    
    # Run pygame version
    try:
        from pygame_chess import PygameChessGUI
        game = PygameChessGUI()
        game.run()
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        print("Попробуйте установить недостающие зависимости")
        input("Нажмите Enter для возврата в меню...")
    except Exception as e:
        print(f"❌ Ошибка запуска: {e}")
        input("Нажмите Enter для возврата в меню...")

def main():
    """Main menu loop"""
    while True:
        clear_screen()
        print_header()
        show_menu()
        
        try:
            choice = input("Введите номер варианта (1-3): ").strip()
            
            if choice == '1':
                run_terminal_version()
            elif choice == '2':
                run_graphical_version()
            elif choice == '3':
                print("👋 До свидания! Спасибо за игру!")
                break
            else:
                print("❌ Неверный выбор. Введите число от 1 до 3.")
                input("Нажмите Enter для продолжения...")
                
        except KeyboardInterrupt:
            print("\n\n👋 Программа прервана пользователем. До свидания!")
            break
        except Exception as e:
            print(f"❌ Произошла ошибка: {e}")
            input("Нажмите Enter для продолжения...")

if __name__ == "__main__":
    main()