#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import sys
import math
import random
from typing import Tuple, List

class PygameChessGUI:
    def __init__(self):
        pygame.init()
        
        # Настройки экрана
        self.WIDTH = 640
        self.HEIGHT = 640
        self.BOARD_SIZE = 8
        self.SQUARE_SIZE = self.WIDTH // self.BOARD_SIZE
        
        # Цвета
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.LIGHT_SQUARE = (240, 217, 181)
        self.DARK_SQUARE = (181, 136, 99)
        self.SELECTED_COLOR = (124, 252, 0)
        self.HIGHLIGHT_COLOR = (255, 255, 0)
        self.RED = (255, 0, 0)
        
        # Создание окна
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Шахматы на Pygame")
        self.clock = pygame.time.Clock()
        
        # Игровое состояние
        self.board = self.get_initial_board()
        self.selected_square = None
        self.valid_moves = []
        self.game_active = True
        self.white_turn = True
        self.move_history = []
        
        # Шрифты
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Загрузка иконок (если есть)
        self.piece_images = self.load_piece_images()
        
    def get_initial_board(self):
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
    
    def load_piece_images(self):
        """Загрузка изображений фигур (заглушки)"""
        # В реальной реализации здесь будет загрузка PNG файлов
        pieces = {}
        unicode_pieces = {
            'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
            'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟'
        }
        
        for piece, symbol in unicode_pieces.items():
            # Создание поверхности с символом
            surface = pygame.Surface((self.SQUARE_SIZE, self.SQUARE_SIZE), pygame.SRCALPHA)
            text = self.font.render(symbol, True, self.BLACK if piece.isupper() else self.RED)
            text_rect = text.get_rect(center=(self.SQUARE_SIZE//2, self.SQUARE_SIZE//2))
            surface.blit(text, text_rect)
            pieces[piece] = surface
            
        return pieces
    
    def draw_board(self):
        """Отрисовка шахматной доски"""
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                # Определение цвета клетки
                color = self.LIGHT_SQUARE if (row + col) % 2 == 0 else self.DARK_SQUARE
                
                # Выделение выбранной клетки
                if self.selected_square == (row, col):
                    color = self.SELECTED_COLOR
                elif (row, col) in self.valid_moves:
                    color = self.HIGHLIGHT_COLOR
                
                # Отрисовка клетки
                rect = pygame.Rect(col * self.SQUARE_SIZE, row * self.SQUARE_SIZE, 
                                 self.SQUARE_SIZE, self.SQUARE_SIZE)
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, self.BLACK, rect, 1)
                
                # Отрисовка фигуры
                piece = self.board[row][col]
                if piece != '.':
                    if piece in self.piece_images:
                        # Использование загруженных изображений
                        self.screen.blit(self.piece_images[piece], rect)
                    else:
                        # Резервный вариант - текстовые символы
                        text_color = self.BLACK if piece.isupper() else self.RED
                        text = self.font.render(piece, True, text_color)
                        text_rect = text.get_rect(center=rect.center)
                        self.screen.blit(text, text_rect)
    
    def draw_coordinates(self):
        """Отрисовка координат доски"""
        # Буквы по горизонтали (a-h)
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        for i, letter in enumerate(letters):
            text = self.small_font.render(letter, True, self.BLACK)
            x = i * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
            # Снизу
            self.screen.blit(text, (x - text.get_width()//2, self.HEIGHT - 20))
            # Сверху
            self.screen.blit(text, (x - text.get_width()//2, 5))
        
        # Цифры по вертикали (1-8)
        for i in range(8):
            text = self.small_font.render(str(8-i), True, self.BLACK)
            y = i * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
            # Слева
            self.screen.blit(text, (5, y - text.get_height()//2))
            # Справа
            self.screen.blit(text, (self.WIDTH - 20, y - text.get_height()//2))
    
    def draw_status(self):
        """Отрисовка статуса игры"""
        status_text = "Белые ходят" if self.white_turn else "Черные ходят"
        if not self.game_active:
            status_text = "Игра завершена"
            
        text = self.font.render(status_text, True, self.BLACK)
        self.screen.blit(text, (10, self.HEIGHT - 40))
        
        # Отображение последнего хода
        if self.move_history:
            last_move = self.move_history[-1]
            move_text = self.small_font.render(f"Последний ход: {last_move}", True, self.BLACK)
            self.screen.blit(move_text, (self.WIDTH // 2 - 100, self.HEIGHT - 40))
    
    def get_square_from_mouse(self, pos: Tuple[int, int]) -> Tuple[int, int]:
        """Преобразование координат мыши в координаты доски"""
        x, y = pos
        col = x // self.SQUARE_SIZE
        row = y // self.SQUARE_SIZE
        return (row, col) if 0 <= row < 8 and 0 <= col < 8 else None
    
    def is_valid_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        """Проверка корректности хода (упрощенная реализация)"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        piece = self.board[from_row][from_col]
        
        # Проверка цвета фигуры
        is_white_piece = piece.isupper()
        if (is_white_piece and not self.white_turn) or (not is_white_piece and self.white_turn):
            return False
            
        # Проверка выхода за границы
        if not (0 <= to_row < 8 and 0 <= to_col < 8):
            return False
            
        # Проверка на то же поле
        if from_pos == to_pos:
            return False
            
        # Упрощенная проверка для пешки
        if piece.lower() == 'p':
            direction = -1 if is_white_piece else 1
            start_row = 6 if is_white_piece else 1
            
            # Ход вперед
            if from_col == to_col:
                if to_row == from_row + direction and self.board[to_row][to_col] == '.':
                    return True
                # Двойной ход с начальной позиции
                if from_row == start_row and to_row == from_row + 2 * direction:
                    if (self.board[from_row + direction][from_col] == '.' and 
                        self.board[to_row][to_col] == '.'):
                        return True
            # Взятие по диагонали
            elif abs(from_col - to_col) == 1 and to_row == from_row + direction:
                target_piece = self.board[to_row][to_col]
                if target_piece != '.' and target_piece.isupper() != is_white_piece:
                    return True
                    
        return True  # Для других фигур - базовая проверка
    
    def get_valid_moves(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Получение списка допустимых ходов для фигуры"""
        valid_moves = []
        for row in range(8):
            for col in range(8):
                if self.is_valid_move(pos, (row, col)):
                    valid_moves.append((row, col))
        return valid_moves
    
    def make_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]):
        """Выполнение хода"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Сохранение хода в истории
        piece = self.board[from_row][from_col]
        captured = self.board[to_row][to_col]
        
        move_notation = f"{chr(ord('a') + from_col)}{8-from_row}-{chr(ord('a') + to_col)}{8-to_row}"
        if captured != '.':
            move_notation += f"x{captured}"
            
        self.move_history.append(move_notation)
        
        # Выполнение хода
        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = '.'
        
        # Смена хода
        self.white_turn = not self.white_turn
        
        # Сброс выбора
        self.selected_square = None
        self.valid_moves = []
    
    def handle_events(self):
        """Обработка событий"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.game_active:
                    pos = pygame.mouse.get_pos()
                    square = self.get_square_from_mouse(pos)
                    if square:
                        self.handle_square_click(square)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:  # Новая игра
                    self.new_game()
                elif event.key == pygame.K_ESCAPE:  # Выход
                    return False
        return True
    
    def handle_square_click(self, square: Tuple[int, int]):
        """Обработка клика по клетке"""
        row, col = square
        
        if self.selected_square is None:
            # Выбор фигуры
            piece = self.board[row][col]
            if piece != '.':
                is_white_piece = piece.isupper()
                if (is_white_piece and self.white_turn) or (not is_white_piece and not self.white_turn):
                    self.selected_square = square
                    self.valid_moves = self.get_valid_moves(square)
        else:
            # Выполнение хода
            if square in self.valid_moves:
                self.make_move(self.selected_square, square)
            elif self.selected_square == square:
                # Отмена выбора
                self.selected_square = None
                self.valid_moves = []
            else:
                # Выбор другой фигуры
                piece = self.board[row][col]
                if piece != '.':
                    is_white_piece = piece.isupper()
                    if (is_white_piece and self.white_turn) or (not is_white_piece and not self.white_turn):
                        self.selected_square = square
                        self.valid_moves = self.get_valid_moves(square)
                    else:
                        self.selected_square = None
                        self.valid_moves = []
    
    def new_game(self):
        """Начало новой игры"""
        self.board = self.get_initial_board()
        self.selected_square = None
        self.valid_moves = []
        self.game_active = True
        self.white_turn = True
        self.move_history = []
    
    def draw(self):
        """Основная отрисовка"""
        self.screen.fill(self.WHITE)
        self.draw_board()
        self.draw_coordinates()
        self.draw_status()
        pygame.display.flip()
    
    def run(self):
        """Основной цикл игры"""
        running = True
        while running:
            running = self.handle_events()
            self.draw()
            self.clock.tick(60)  # 60 FPS
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = PygameChessGUI()
    game.run()