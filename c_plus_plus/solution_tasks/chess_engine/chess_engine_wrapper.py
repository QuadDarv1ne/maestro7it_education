#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ctypes
import os
import sys
from typing import Tuple, List, Optional

class ChessEngineWrapper:
    """Python wrapper для С++ шахматного движка"""
    
    def __init__(self):
        self.lib = None
        self.board_state = self.get_initial_board()
        self.current_turn = True  # True = белые, False = черные
        
    def initialize_engine(self) -> bool:
        """Инициализация С++ библиотеки движка"""
        try:
            # Попытка загрузить скомпилированную библиотеку
            if os.name == 'nt':  # Windows
                lib_name = 'chess_engine.dll'
            else:  # Linux/Mac
                lib_name = 'libchess_engine.so'
            
            lib_path = os.path.join(os.path.dirname(__file__), 'build_gui', lib_name)
            if os.path.exists(lib_path):
                self.lib = ctypes.CDLL(lib_path)
                print("С++ движок успешно загружен")
                return True
            else:
                print("Библиотека движка не найдена, используем Python реализацию")
                return False
        except Exception as e:
            print(f"Ошибка загрузки движка: {e}")
            return False
    
    def get_initial_board(self) -> List[List[str]]:
        """Начальная позиция шахматной доски"""
        return [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]
    
    def board_to_fen(self) -> str:
        """Преобразование доски в FEN нотацию"""
        fen = ""
        for row in self.board_state:
            empty_count = 0
            for piece in row:
                if piece == '.':
                    empty_count += 1
                else:
                    if empty_count > 0:
                        fen += str(empty_count)
                        empty_count = 0
                    fen += piece
            if empty_count > 0:
                fen += str(empty_count)
            fen += "/"
        fen = fen[:-1]  # Убираем последний слеш
        
        # Добавляем информацию о ходе
        fen += " w " if self.current_turn else " b "
        fen += "KQkq - 0 1"  # Права рокировки, en passant, счетчики
        return fen
    
    def is_valid_move_cpp(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        """Проверка хода через С++ движок (если доступен)"""
        if not self.lib:
            return self.is_valid_move_python(from_pos, to_pos)
        
        try:
            # Преобразуем координаты в шахматную нотацию
            from_square = chr(ord('a') + from_pos[1]) + str(8 - from_pos[0])
            to_square = chr(ord('a') + to_pos[1]) + str(8 - to_pos[0])
            move_str = from_square + to_square
            
            # Вызываем С++ функцию (псевдокод)
            # result = self.lib.validate_move(move_str.encode('utf-8'))
            # return bool(result)
            
            # Пока используем Python реализацию
            return self.is_valid_move_python(from_pos, to_pos)
        except Exception as e:
            print(f"Ошибка вызова С++ движка: {e}")
            return self.is_valid_move_python(from_pos, to_pos)
    
    def is_valid_move_python(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        """Python реализация проверки хода (резервный вариант)"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        piece = self.board_state[from_row][from_col]
        target_piece = self.board_state[to_row][to_col]
        
        # Проверка цвета фигуры
        is_white_piece = piece.isupper()
        if (is_white_piece and not self.current_turn) or (not is_white_piece and self.current_turn):
            return False
            
        # Проверка выхода за границы
        if not (0 <= to_row < 8 and 0 <= to_col < 8):
            return False
            
        # Проверка на то же поле
        if from_pos == to_pos:
            return False
            
        # Проверка, что нельзя съесть свою фигуру
        if target_piece != '.' and ((target_piece.isupper() and is_white_piece) or 
                                   (target_piece.islower() and not is_white_piece)):
            return False
            
        piece_type = piece.lower()
        
        # Логика для пешки
        if piece_type == 'p':
            direction = -1 if is_white_piece else 1
            start_row = 6 if is_white_piece else 1
            
            # Ход вперед на одну клетку
            if from_col == to_col and to_row == from_row + direction and target_piece == '.':
                return True
                
            # Двойной ход с начальной позиции
            if (from_row == start_row and from_col == to_col and 
                to_row == from_row + 2 * direction and 
                target_piece == '.' and self.board_state[from_row + direction][from_col] == '.'):
                return True
                
            # Взятие по диагонали
            if (abs(from_col - to_col) == 1 and to_row == from_row + direction and 
                target_piece != '.' and target_piece.isupper() != is_white_piece):
                return True
                
        # Логика для ладьи
        elif piece_type == 'r':
            return self.is_straight_move(from_pos, to_pos)
            
        # Логика для слона
        elif piece_type == 'b':
            return self.is_diagonal_move(from_pos, to_pos)
            
        # Логика для ферзя
        elif piece_type == 'q':
            return self.is_straight_move(from_pos, to_pos) or self.is_diagonal_move(from_pos, to_pos)
            
        # Логика для короля
        elif piece_type == 'k':
            row_diff = abs(to_row - from_row)
            col_diff = abs(to_col - from_col)
            return row_diff <= 1 and col_diff <= 1
            
        # Логика для коня
        elif piece_type == 'n':
            row_diff = abs(to_row - from_row)
            col_diff = abs(to_col - from_col)
            return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)
            
        return False
    
    def is_straight_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        """Проверка прямолинейного хода"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        if from_row != to_row and from_col != to_col:
            return False
            
        if from_row == to_row:  # Горизонтальный ход
            start, end = sorted([from_col, to_col])
            for col in range(start + 1, end):
                if self.board_state[from_row][col] != '.':
                    return False
        else:  # Вертикальный ход
            start, end = sorted([from_row, to_row])
            for row in range(start + 1, end):
                if self.board_state[row][from_col] != '.':
                    return False
                    
        return True
    
    def is_diagonal_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        """Проверка диагонального хода"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        if abs(from_row - to_row) != abs(from_col - to_col):
            return False
            
        row_step = 1 if to_row > from_row else -1
        col_step = 1 if to_col > from_col else -1
        
        row, col = from_row + row_step, from_col + col_step
        while (row, col) != (to_row, to_col):
            if self.board_state[row][col] != '.':
                return False
            row += row_step
            col += col_step
            
        return True
    
    def make_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        """Выполнение хода"""
        if not self.is_valid_move_python(from_pos, to_pos):
            return False
            
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Выполнение хода
        piece = self.board_state[from_row][from_col]
        self.board_state[to_row][to_col] = piece
        self.board_state[from_row][from_col] = '.'
        
        # Смена хода
        self.current_turn = not self.current_turn
        return True
    
    def get_best_move_cpp(self) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Получение лучшего хода от С++ движка"""
        if not self.lib:
            return self.get_best_move_python()
        
        try:
            # Получаем FEN позицию
            fen = self.board_to_fen()
            
            # Вызываем С++ функцию поиска (псевдокод)
            # move_result = self.lib.find_best_move(fen.encode('utf-8'), 4)  # глубина 4
            # if move_result:
            #     # Преобразуем результат обратно в координаты
            #     from_square, to_square = move_result.decode().split('-')
            #     from_pos = (8 - int(from_square[1]), ord(from_square[0]) - ord('a'))
            #     to_pos = (8 - int(to_square[1]), ord(to_square[0]) - ord('a'))
            #     return (from_pos, to_pos)
            
            return self.get_best_move_python()
        except Exception as e:
            print(f"Ошибка вызова С++ движка для поиска: {e}")
            return self.get_best_move_python()
    
    def get_best_move_python(self) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Python реализация поиска лучшего хода (резервный вариант)"""
        # Простой алгоритм: найти случайный допустимый ход для черных
        import random
        
        possible_moves = []
        for row in range(8):
            for col in range(8):
                piece = self.board_state[row][col]
                if piece != '.' and piece.islower():  # Черная фигура
                    for to_row in range(8):
                        for to_col in range(8):
                            if self.is_valid_move_python((row, col), (to_row, to_col)):
                                possible_moves.append(((row, col), (to_row, to_col)))
        
        return random.choice(possible_moves) if possible_moves else None

# Глобальный экземпляр движка
chess_engine = ChessEngineWrapper()