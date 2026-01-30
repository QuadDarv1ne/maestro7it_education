#!/usr/bin/env python3
"""
Flask backend для веб-интерфейса шахмат
"""

from flask import Flask, render_template, jsonify, request
import json
import os
from datetime import datetime

# Импортируем наши компоненты
try:
    from chess_engine_wrapper import ChessEngineWrapper
    from stockfish_integration import StockfishIntegration
    from endgame_tablebase import g_endgame_tablebase
except ImportError as e:
    print(f"Предупреждение: некоторые модули недоступны: {e}")
    ChessEngineWrapper = None
    StockfishIntegration = None
    g_endgame_tablebase = None

app = Flask(__name__, static_folder='web', template_folder='web')

# Глобальные объекты
chess_engine = None
stockfish_engine = None

class WebChessGame:
    """Класс для управления веб-игрой"""
    
    def __init__(self):
        self.board_state = self.get_initial_board()
        self.move_history = []
        self.current_player = 'white'
        self.game_active = True
        self.difficulty = 18  # Средний уровень по умолчанию
        
    def get_initial_board(self):
        """Возвращает начальную позицию"""
        return [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]
    
    def reset_game(self):
        """Сброс игры"""
        self.board_state = self.get_initial_board()
        self.move_history = []
        self.current_player = 'white'
        self.game_active = True
    
    def make_move(self, from_pos, to_pos):
        """Выполнить ход"""
        if not self.game_active:
            return False, "Игра завершена"
        
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Проверка границ доски
        if not (0 <= from_row < 8 and 0 <= from_col < 8 and 
                0 <= to_row < 8 and 0 <= to_col < 8):
            return False, "Неверные координаты"
        
        piece = self.board_state[from_row][from_col]
        if not piece:
            return False, "Нет фигуры для хода"
        
        # Проверка очередности хода
        is_white_piece = piece.isupper()
        if (self.current_player == 'white' and not is_white_piece) or \
           (self.current_player == 'black' and is_white_piece):
            return False, "Не ваша очередь ходить"
        
        # Проверка валидности хода (упрощенная)
        if not self.is_valid_move(from_pos, to_pos):
            return False, "Невалидный ход"
        
        # Выполняем ход
        captured_piece = self.board_state[to_row][to_col]
        
        # Сохраняем ход
        move_record = {
            'from': from_pos,
            'to': to_pos,
            'piece': piece,
            'captured': captured_piece,
            'player': self.current_player,
            'timestamp': datetime.now().isoformat()
        }
        
        self.move_history.append(move_record)
        
        # Обновляем доску
        self.board_state[to_row][to_col] = piece
        self.board_state[from_row][from_col] = None
        
        # Меняем игрока
        self.current_player = 'black' if self.current_player == 'white' else 'white'
        
        return True, "Ход выполнен"
    
    def is_valid_move(self, from_pos, to_pos):
        """Проверка валидности хода (упрощенная)"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        piece = self.board_state[from_row][from_col]
        target_piece = self.board_state[to_row][to_col]
        
        # Нельзя съесть свою фигуру
        if target_piece:
            if (piece.isupper() and target_piece.isupper()) or \
               (piece.islower() and target_piece.islower()):
                return False
        
        # Упрощенные правила для разных фигур
        piece_lower = piece.lower()
        
        if piece_lower == 'p':  # Пешка
            return self._is_valid_pawn_move(from_pos, to_pos, piece.isupper())
        elif piece_lower == 'r':  # Ладья
            return self._is_valid_rook_move(from_pos, to_pos)
        elif piece_lower == 'n':  # Конь
            return self._is_valid_knight_move(from_pos, to_pos)
        elif piece_lower == 'b':  # Слон
            return self._is_valid_bishop_move(from_pos, to_pos)
        elif piece_lower == 'q':  # Ферзь
            return self._is_valid_queen_move(from_pos, to_pos)
        elif piece_lower == 'k':  # Король
            return self._is_valid_king_move(from_pos, to_pos)
        
        return False
    
    def _is_valid_pawn_move(self, from_pos, to_pos, is_white):
        """Правила движения пешки"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        direction = -1 if is_white else 1
        start_row = 6 if is_white else 1
        
        # Обычный ход вперед
        if from_col == to_col and to_row == from_row + direction and not self.board_state[to_row][to_col]:
            return True
        
        # Начальный двойной ход
        if (from_col == to_col and from_row == start_row and 
            to_row == from_row + 2 * direction and 
            not self.board_state[to_row][to_col] and 
            not self.board_state[from_row + direction][to_col]):
            return True
        
        # Взятие по диагонали
        if (abs(from_col - to_col) == 1 and to_row == from_row + direction and 
            self.board_state[to_row][to_col]):
            return True
        
        return False
    
    def _is_valid_rook_move(self, from_pos, to_pos):
        """Правила движения ладьи"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        if from_row != to_row and from_col != to_col:
            return False
        
        # Проверка пути
        if from_row == to_row:
            min_col = min(from_col, to_col)
            max_col = max(from_col, to_col)
            for col in range(min_col + 1, max_col):
                if self.board_state[from_row][col]:
                    return False
        else:
            min_row = min(from_row, to_row)
            max_row = max(from_row, to_row)
            for row in range(min_row + 1, max_row):
                if self.board_state[row][from_col]:
                    return False
        
        return True
    
    def _is_valid_knight_move(self, from_pos, to_pos):
        """Правила движения коня"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        row_diff = abs(from_row - to_row)
        col_diff = abs(from_col - to_col)
        return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)
    
    def _is_valid_bishop_move(self, from_pos, to_pos):
        """Правила движения слона"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        row_diff = abs(from_row - to_row)
        col_diff = abs(from_col - to_col)
        
        if row_diff != col_diff:
            return False
        
        # Проверка диагонального пути
        row_dir = 1 if to_row > from_row else -1
        col_dir = 1 if to_col > from_col else -1
        
        for i in range(1, row_diff):
            if self.board_state[from_row + i * row_dir][from_col + i * col_dir]:
                return False
        
        return True
    
    def _is_valid_queen_move(self, from_pos, to_pos):
        """Правила движения ферзя"""
        return (self._is_valid_rook_move(from_pos, to_pos) or 
                self._is_valid_bishop_move(from_pos, to_pos))
    
    def _is_valid_king_move(self, from_pos, to_pos):
        """Правила движения короля"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        row_diff = abs(from_row - to_row)
        col_diff = abs(from_col - to_col)
        return row_diff <= 1 and col_diff <= 1
    
    def undo_move(self):
        """Отменить последний ход"""
        if not self.move_history:
            return False, "Нет ходов для отмены"
        
        last_move = self.move_history.pop()
        from_pos = last_move['from']
        to_pos = last_move['to']
        piece = last_move['piece']
        captured_piece = last_move['captured']
        
        # Восстанавливаем позицию
        self.board_state[from_pos[0]][from_pos[1]] = piece
        self.board_state[to_pos[0]][to_pos[1]] = captured_piece
        
        # Меняем игрока обратно
        self.current_player = last_move['player']
        
        return True, "Ход отменен"
    
    def get_game_state(self):
        """Получить текущее состояние игры"""
        return {
            'board': self.board_state,
            'current_player': self.current_player,
            'move_history': self.move_history,
            'game_active': self.game_active,
            'difficulty': self.difficulty
        }

# Глобальный экземпляр игры
web_game = WebChessGame()

@app.route('/')
def index():
    """Главная страница"""
    return render_template('index.html')

@app.route('/api/new-game', methods=['POST'])
def new_game():
    """Новая игра"""
    try:
        web_game.reset_game()
        return jsonify({
            'success': True,
            'message': 'Новая игра начата',
            'game_state': web_game.get_game_state()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Ошибка: {str(e)}'
        }), 500

@app.route('/api/make-move', methods=['POST'])
def make_move():
    """Выполнить ход"""
    try:
        data = request.get_json()
        from_pos = data['from']
        to_pos = data['to']
        
        success, message = web_game.make_move(from_pos, to_pos)
        
        response = {
            'success': success,
            'message': message,
            'game_state': web_game.get_game_state()
        }
        
        # Если ход успешен и очередь черных - ход компьютера
        if success and web_game.current_player == 'black' and web_game.game_active:
            computer_success, computer_message = make_computer_move()
            response['computer_move'] = {
                'success': computer_success,
                'message': computer_message
            }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Ошибка: {str(e)}'
        }), 500

@app.route('/api/undo-move', methods=['POST'])
def undo_move():
    """Отменить ход"""
    try:
        success, message = web_game.undo_move()
        return jsonify({
            'success': success,
            'message': message,
            'game_state': web_game.get_game_state()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Ошибка: {str(e)}'
        }), 500

@app.route('/api/get-state', methods=['GET'])
def get_state():
    """Получить состояние игры"""
    try:
        return jsonify({
            'success': True,
            'game_state': web_game.get_game_state()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Ошибка: {str(e)}'
        }), 500

@app.route('/api/set-difficulty', methods=['POST'])
def set_difficulty():
    """Установить уровень сложности"""
    try:
        data = request.get_json()
        difficulty = data.get('difficulty', 18)
        web_game.difficulty = difficulty
        
        return jsonify({
            'success': True,
            'message': f'Уровень сложности установлен: {difficulty}',
            'difficulty': difficulty
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Ошибка: {str(e)}'
        }), 500

def make_computer_move():
    """Ход компьютера (интеграция с различными ИИ)"""
    try:
        # Попытка использовать различные ИИ в порядке приоритета
        
        # 1. Endgame Tablebase (если применимо)
        if g_endgame_tablebase and g_endgame_tablebase.is_applicable(web_game.get_game_state()):
            # Здесь будет логика использования tablebase
            pass
        
        # 2. Stockfish (если доступен)
        if StockfishIntegration:
            # Здесь будет интеграция с Stockfish
            pass
        
        # 3. Наш шахматный движок
        if ChessEngineWrapper:
            # Здесь будет интеграция с нашим движком
            pass
        
        # 4. Упрощенный AI (заглушка)
        # Находим случайный валидный ход для черных
        valid_moves = []
        
        for row in range(8):
            for col in range(8):
                piece = web_game.board_state[row][col]
                if piece and piece.islower():  # Черная фигура
                    for to_row in range(8):
                        for to_col in range(8):
                            if web_game.is_valid_move([row, col], [to_row, to_col]):
                                valid_moves.append([[row, col], [to_row, to_col]])
        
        if valid_moves:
            import random
            from_pos, to_pos = random.choice(valid_moves)
            success, message = web_game.make_move(from_pos, to_pos)
            return success, message if success else "Компьютер не может сделать ход"
        else:
            return False, "Нет доступных ходов для компьютера"
            
    except Exception as e:
        return False, f"Ошибка компьютерного хода: {str(e)}"

if __name__ == '__main__':
    print("=== ЗАПУСК ВЕБ-СЕРВЕРА ШАХМАТ ===")
    print("Откройте в браузере: http://localhost:5000")
    print("Для остановки нажмите Ctrl+C")
    
    # Запуск Flask приложения
    app.run(host='0.0.0.0', port=5000, debug=True)