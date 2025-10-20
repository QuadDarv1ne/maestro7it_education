#!/usr/bin/env python3
# ============================================================================
# demonstrate_endgame_trainer.py
# ============================================================================

"""
Демонстрация функциональности тренажера эндшпилей.
"""

import sys
import os
import time

# Добавляем путь к модулям
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from utils.endgame_trainer import EndgameTrainer

def demonstrate_endgame_trainer():
    """Демонстрация работы тренажера эндшпилей."""
    print("=== Демонстрация тренажера эндшпилей ===\n")
    
    # Создаем экземпляр тренажера
    trainer = EndgameTrainer()
    
    # Показываем доступные сценарии
    print("Доступные сценарии тренировки:")
    scenarios = trainer.get_available_scenarios()
    for i, scenario in enumerate(scenarios, 1):
        print(f"{i:2d}. {scenario['name']} ({scenario['difficulty']})")
        print(f"    {scenario['description']}")
        if i >= 4:  # Показываем только первые 4 для краткости
            print("    ...")
            break
    print()
    
    # Демонстрируем выбор сценария
    print("Выбор сценария для тренировки:")
    scenario = trainer.select_scenario("ферзь_против_пешки")
    if scenario:
        print(f"Выбран сценарий: {scenario['name']}")
        print(f"Цель: {scenario['goal']}")
        print(f"FEN позиция: {scenario['fen']}")
    print()
    
    # Демонстрируем получение советов
    print("Советы по текущему сценарию:")
    for i in range(2):  # Показываем 2 совета
        tip = trainer.get_random_tip()
        if tip:
            print(f"  {i+1}. {tip}")
    print()
    
    # Демонстрируем завершение сценария
    print("Завершение сценария:")
    trainer.complete_scenario(success=True)
    print("Сценарий завершен успешно!")
    print()
    
    # Демонстрируем статистику
    print("Статистика тренировок:")
    stats = trainer.get_stats()
    print(f"  Завершено сценариев: {stats['scenarios_completed']}")
    print(f"  Всего попыток: {stats['total_attempts']}")
    print(f"  Успешных попыток: {stats['successful_attempts']}")
    print(f"  Процент успеха: {trainer.get_success_rate():.1f}%")
    print(f"  Время тренировки: {stats['time_spent']:.1f} секунд")
    print()

def demonstrate_recommendations():
    """Демонстрация рекомендаций тренажера."""
    print("=== Демонстрация рекомендаций ===\n")
    
    trainer = EndgameTrainer()
    
    # Получаем рекомендацию без статистики
    print("Рекомендация для новичка:")
    recommendation = trainer.get_recommendation()
    if recommendation:
        scenario_info = trainer.select_scenario(recommendation)
        if scenario_info:
            print(f"  Рекомендуемый сценарий: {scenario_info['name']}")
            print(f"  Сложность: {scenario_info['difficulty']}")
    print()
    
    # Имитируем низкую успешность
    print("Рекомендация при низкой успешности:")
    for i in range(3):
        trainer.select_scenario("ферзь_против_пешки")
        trainer.complete_scenario(success=False)
    
    recommendation = trainer.get_recommendation()
    if recommendation:
        scenario_info = trainer.select_scenario(recommendation)
        if scenario_info:
            print(f"  Рекомендуемый сценарий: {scenario_info['name']}")
            print(f"  Сложность: {scenario_info['difficulty']}")
    print()
    
    # Имитируем высокую успешность
    print("Рекомендация при высокой успешности:")
    for i in range(5):
        trainer.select_scenario("ферзь_против_пешки")
        trainer.complete_scenario(success=True)
    
    recommendation = trainer.get_recommendation()
    if recommendation:
        scenario_info = trainer.select_scenario(recommendation)
        if scenario_info:
            print(f"  Рекомендуемый сценарий: {scenario_info['name']}")
            print(f"  Сложность: {scenario_info['difficulty']}")
    print()

def demonstrate_fen_positions():
    """Демонстрация FEN позиций сценариев."""
    print("=== Демонстрация FEN позиций ===\n")
    
    trainer = EndgameTrainer()
    
    # Показываем FEN позиции для нескольких сценариев
    scenarios_to_show = ["ферзь_против_пешки", "ладья_против_пешки", "король_против_пешки"]
    
    for scenario_id in scenarios_to_show:
        scenario = trainer.select_scenario(scenario_id)
        if scenario:
            fen = trainer.get_scenario_fen()
            print(f"{scenario['name']}:")
            print(f"  FEN: {fen}")
            print(f"  Цель: {scenario['goal']}")
            print()

def main():
    """Основная функция демонстрации."""
    print("Демонстрация функциональности тренажера эндшпилей\n")
    print("=" * 50)
    
    demonstrate_endgame_trainer()
    demonstrate_recommendations()
    demonstrate_fen_positions()
    
    print("Демонстрация завершена!")

if __name__ == "__main__":
    main()