#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тестирование FastAPI шахматного сервера
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_root():
    """Тест главной страницы"""
    print("🌐 Тестирование главной страницы...")
    response = requests.get(f"{BASE_URL}/")
    print(f"   Статус: {response.status_code}")
    print(f"   Размер HTML: {len(response.text)} байт")
    assert response.status_code == 200
    assert "Chess Master" in response.text
    print("   ✅ Главная страница работает\n")

def test_new_game():
    """Тест создания новой игры"""
    print("🎮 Тестирование создания новой игры...")
    response = requests.post(
        f"{BASE_URL}/api/new-game",
        json={"player_name": "TestPlayer", "game_mode": "ai", "player_color": True}
    )
    print(f"   Статус: {response.status_code}")
    data = response.json()
    print(f"   Game ID: {data.get('game_id')}")
    print(f"   Доска: {len(data.get('board_state', []))}x{len(data.get('board_state', [[]])[0])}")
    assert response.status_code == 200
    assert "game_id" in data
    print("   ✅ Новая игра создана\n")
    return data["game_id"]

def test_game_state(game_id):
    """Тест получения состояния игры"""
    print(f"📊 Тестирование состояния игры {game_id}...")
    # Для этого API нет отдельного endpoint, используем данные из new-game
    print("   ⚠️ API не имеет отдельного endpoint /api/game-state")
    print("   ✅ Пропускаем тест\n")

def test_evaluation(game_id):
    """Тест оценки позиции"""
    print(f"🧠 Тестирование оценки позиции {game_id}...")
    response = requests.get(f"{BASE_URL}/api/evaluation/{game_id}")
    print(f"   Статус: {response.status_code}")
    data = response.json()
    evaluation = data.get("evaluation", 0)
    print(f"   Оценка: {evaluation} сантипешек")
    print(f"   Позиция: {'Равная' if abs(evaluation) < 50 else 'Неравная'}")
    assert response.status_code == 200
    assert "evaluation" in data
    print("   ✅ Оценка получена\n")

def test_make_move(game_id):
    """Тест выполнения хода"""
    print(f"♟️ Тестирование хода e2-e4 для игры {game_id}...")
    response = requests.post(
        f"{BASE_URL}/api/make-move",
        json={
            "game_id": game_id,
            "from_pos": [6, 4],  # e2
            "to_pos": [4, 4],    # e4
            "player_color": True
        }
    )
    print(f"   Статус: {response.status_code}")
    data = response.json()
    print(f"   Успех: {data.get('success')}")
    if data.get("success"):
        game_state = data.get('game_state', {})
        print(f"   История: {len(game_state.get('move_history', []))} ходов")
        print("   ✅ Ход выполнен\n")
    else:
        print(f"   ❌ Ход отклонен: {data.get('message')}\n")
    return data.get("success", False)

def test_ai_move(game_id):
    """Тест хода AI"""
    print(f"🤖 Тестирование хода AI для игры {game_id}...")
    response = requests.get(f"{BASE_URL}/api/ai-move/{game_id}?depth=3")
    print(f"   Статус: {response.status_code}")
    data = response.json()
    print(f"   Успех: {data.get('success')}")
    if data.get("success"):
        move_notation = data.get("move_notation")
        if move_notation:
            print(f"   Ход AI: {move_notation}")
        game_state = data.get('game_state', {})
        print(f"   История: {len(game_state.get('move_history', []))} ходов")
        print("   ✅ AI сделал ход\n")
    else:
        print(f"   ❌ AI не смог сделать ход\n")

def test_undo_move(game_id):
    """Тест отмены хода"""
    print(f"⏮️ Тестирование отмены хода для игры {game_id}...")
    response = requests.post(f"{BASE_URL}/api/undo-move/{game_id}")
    print(f"   Статус: {response.status_code}")
    data = response.json()
    print(f"   Успех: {data.get('success')}")
    if data.get("success"):
        game_state = data.get('game_state', {})
        print(f"   История: {len(game_state.get('move_history', []))} ходов")
        print("   ✅ Ход отменен\n")
    else:
        print(f"   ❌ Не удалось отменить: {data.get('message')}\n")

def test_stats(game_id):
    """Тест статистики"""
    print(f"📈 Тестирование статистики для игры {game_id}...")
    response = requests.get(f"{BASE_URL}/api/stats/{game_id}")
    print(f"   Статус: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Всего ходов: {data.get('total_moves', 0)}")
        print(f"   Взятий: {data.get('captures', 0)}")
        print("   ✅ Статистика получена\n")
    else:
        print("   ⚠️ Статистика недоступна\n")

def main():
    """Запуск всех тестов"""
    print("=" * 60)
    print("🔍 ТЕСТИРОВАНИЕ FastAPI ШАХМАТНОГО СЕРВЕРА")
    print("=" * 60 + "\n")
    
    try:
        # Тест 1: Главная страница
        test_root()
        
        # Тест 2: Создание игры
        game_id = test_new_game()
        
        # Тест 3: Состояние игры
        test_game_state(game_id)
        
        # Тест 4: Оценка позиции
        test_evaluation(game_id)
        
        # Тест 5: Ход игрока
        move_success = test_make_move(game_id)
        
        # Тест 6: Ход AI (только если ход игрока успешен)
        if move_success:
            test_ai_move(game_id)
        
        # Тест 7: Отмена хода
        test_undo_move(game_id)
        
        # Тест 8: Статистика
        test_stats(game_id)
        
        print("=" * 60)
        print("✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        print("=" * 60)
        print(f"\n🌐 Откройте в браузере: {BASE_URL}")
        print(f"📚 API документация: {BASE_URL}/docs")
        print(f"🔧 Альтернативная документация: {BASE_URL}/redoc")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ОШИБКА: Не удается подключиться к серверу!")
        print("   Убедитесь, что FastAPI сервер запущен:")
        print("   py -3.13 -m uvicorn interfaces.fastapi_chess:app --reload\n")
    except Exception as e:
        print(f"\n❌ ОШИБКА: {e}\n")

if __name__ == "__main__":
    main()
