#!/usr/bin/env python3
"""
Демонстрация улучшенных образовательных функций chess_stockfish.
"""

import sys
import os
import time
import random

# Добавляем путь к модулям игры
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.educational import ChessEducator
from utils.opening_book import OpeningBook

def demonstrate_educational_features():
    """Демонстрация образовательных функций."""
    print("🎓 Демонстрация улучшенных образовательных функций chess_stockfish")
    print("=" * 70)
    
    # Создаем образовательный компонент
    educator = ChessEducator()
    
    print("\n📚 1. Случайные стратегические советы:")
    for i in range(3):
        tip = educator.get_random_tip()
        print(f"   💡 {tip}")
        time.sleep(0.5)
    
    print("\n📖 2. Объяснения шахматных терминов:")
    terms = ["шах", "мат", "рокировка", "форк", "пин"]
    for term in terms:
        explanation = educator.get_term_explanation(term)
        print(f"   {term.capitalize()}: {explanation}")
        time.sleep(0.5)
    
    print("\n♟️ 3. Подсказки по фигурам:")
    pieces = ["пешка", "ладья", "конь", "слон", "ферзь", "король"]
    for piece in pieces:
        hint = educator.get_piece_hint(piece)
        print(f"   {piece.capitalize()}: {hint}")
        time.sleep(0.5)
    
    print("\n📜 4. Исторические факты:")
    for i in range(3):
        fact = educator.get_historical_fact()
        print(f"   📚 {fact}")
        time.sleep(0.5)
    
    print("\n⚔️ 5. Тактические мотивы:")
    for i in range(3):
        motiv = educator.get_tactical_motiv()
        print(f"   {motiv}")
        time.sleep(0.5)
    
    # Создаем дебютную книгу
    opening_book = OpeningBook()
    
    print("\n🎯 6. Информация о дебютах:")
    openings = ["Испанская партия", "Сицилианская защита", "Итальянская партия"]
    for opening in openings:
        info = opening_book.get_opening_info(opening)
        if info:
            print(f"   {opening}:")
            print(f"     Описание: {info['description']}")
            print(f"     Стратегия: {info['strategy']}")
            print(f"     Сложность: {info['difficulty']}")
            if 'educational_tips' in info:
                print(f"     Советы: {info['educational_tips'][0]}")
            print()
            time.sleep(1)
    
    print("\n📘 7. Дебютные принципы:")
    for i in range(3):
        principle, explanation = opening_book.get_random_principle()
        print(f"   {principle}")
        print(f"   {explanation}")
        print()
        time.sleep(1)
    
    print("\n🧩 8. Интерактивные головоломки:")
    for i in range(2):
        puzzle = educator.get_random_puzzle()
        print(f"   Головоломка: {puzzle['name']}")
        print(f"   Описание: {puzzle['description']}")
        print(f"   Решение: {puzzle['solution']}")
        print()
        time.sleep(1)
    
    print("\n🏅 9. Система достижений:")
    achievements = ["first_game", "tactical_master", "opening_expert"]
    for achievement_key in achievements:
        info = educator.get_achievement_info(achievement_key)
        if info:
            print(f"   {info['name']}: {info['description']}")
            time.sleep(0.5)
    
    print("\n📈 10. Прогресс обучения:")
    # Симулируем прогресс
    educator.puzzles_solved = 5
    educator.add_learned_opening("Испанская партия")
    educator.add_learned_opening("Сицилианская защита")
    
    progress = educator.get_learning_progress()
    print(f"   Тактика: {progress['tactics']}/10")
    print(f"   Дебюты: {progress['openings']}/5")
    print(f"   Стратегия: {progress['strategy']}/8")
    
    unlocked = educator.get_unlocked_achievements()
    if unlocked:
        print(f"   Разблокированные достижения: {', '.join(unlocked)}")
    
    print("\n" + "=" * 70)
    print("✅ Демонстрация завершена!")

def interactive_demo():
    """Интерактивная демонстрация."""
    print("\n🎮 Интерактивная демонстрация")
    print("=" * 50)
    
    educator = ChessEducator()
    opening_book = OpeningBook()
    
    while True:
        print("\nВыберите действие:")
        print("1. Получить стратегический совет")
        print("2. Получить исторический факт")
        print("3. Получить информацию о фигуре")
        print("4. Получить объяснение термина")
        print("5. Получить дебютный совет")
        print("6. Решить головоломку")
        print("7. Показать прогресс")
        print("0. Выход")
        
        choice = input("\nВаш выбор: ").strip()
        
        if choice == "1":
            tip = educator.get_random_tip()
            print(f"\n💡 Совет: {tip}")
        elif choice == "2":
            fact = educator.get_historical_fact()
            print(f"\n📚 Факт: {fact}")
        elif choice == "3":
            piece = input("Введите название фигуры (пешка, ладья, конь, слон, ферзь, король): ").strip()
            hint = educator.get_piece_hint(piece)
            print(f"\n♟️ {piece.capitalize()}: {hint}")
        elif choice == "4":
            term = input("Введите шахматный термин: ").strip()
            explanation = educator.get_term_explanation(term)
            print(f"\n📖 {term.capitalize()}: {explanation}")
        elif choice == "5":
            opening = input("Введите название дебюта: ").strip()
            info = opening_book.get_opening_info(opening)
            if info:
                print(f"\n🎯 {opening}:")
                print(f"   Описание: {info['description']}")
                tip = opening_book.get_educational_tip(opening)
                if tip:
                    print(f"   💡 Совет: {tip}")
            else:
                print("Дебют не найден.")
        elif choice == "6":
            puzzle = educator.get_random_puzzle()
            print(f"\n🧩 Головоломка: {puzzle['name']}")
            print(f"   {puzzle['description']}")
            print(f"   Позиция: {puzzle['fen']}")
            user_solution = input("Введите ваше решение (в формате UCI, например e2e4): ").strip()
            if educator.check_puzzle_solution(puzzle, user_solution):
                print("✅ Правильно!")
            else:
                print(f"❌ Неправильно. Правильное решение: {puzzle['solution']}")
        elif choice == "7":
            progress = educator.get_learning_progress()
            print(f"\n📈 Прогресс обучения:")
            print(f"   Тактика: {progress['tactics']} очков")
            print(f"   Дебюты: {progress['openings']} изучено")
            print(f"   Стратегия: {progress['strategy']} очков")
            unlocked = educator.get_unlocked_achievements()
            if unlocked:
                print(f"   Достижения: {', '.join(unlocked)}")
        elif choice == "0":
            break
        else:
            print("Неверный выбор.")

if __name__ == "__main__":
    demonstrate_educational_features()
    
    # Запрашиваем, хочет ли пользователь интерактивную демонстрацию
    interactive = input("\nХотите попробовать интерактивную демонстрацию? (y/n): ").strip().lower()
    if interactive in ('y', 'yes', 'д', 'да'):
        interactive_demo()
    
    print("\n👋 Спасибо за использование chess_stockfish!")