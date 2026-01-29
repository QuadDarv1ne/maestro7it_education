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
        self.WIDTH = 800  # Увеличил ширину для боковой панели
        self.HEIGHT = 640
        self.BOARD_SIZE = 8
        self.SQUARE_SIZE = 640 // self.BOARD_SIZE  # 80 пикселей
        self.SIDE_PANEL_WIDTH = 160
        
        # Цвета
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.LIGHT_SQUARE = (240, 217, 181)
        self.DARK_SQUARE = (181, 136, 99)
        self.SELECTED_COLOR = (124, 252, 0)
        self.HIGHLIGHT_COLOR = (255, 255, 0)
        self.RED = (255, 0, 0)
        self.GRAY = (128, 128, 128)
        self.PANEL_BG = (245, 245, 245)
        
        # Создание окна
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Шахматы на Pygame - Улучшенная версия")
        self.clock = pygame.time.Clock()
        
        # Игровое состояние
        self.board = self.get_initial_board()
        self.selected_square = None
        self.valid_moves = []
        self.game_active = True
        self.white_turn = True
        self.move_history = []
        self.captured_pieces = {'white': [], 'black': []}
        self.game_mode = 'computer'  # 'computer' или 'two_players'
        self.castling_rights = {
            'K': True, 'Q': True,  # Белые короткая и длинная рокировка
            'k': True, 'q': True   # Черные короткая и длинная рокировка
        }
        self.en_passant_target = None  # Возможность взятия на проходе
        self.halfmove_clock = 0  # Для правила 50 ходов
        self.fullmove_number = 1        
        # Шрифты
        self.font = pygame.font.SysFont('Arial', 24)
        self.big_font = pygame.font.SysFont('Arial', 32, bold=True)
        self.small_font = pygame.font.SysFont('Arial', 18)
        
        # Загрузка иконок
        self.piece_images = self.load_piece_images()
        
        # Анимация
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
        """Загрузка реальных иконок фигур"""
        import os
        pieces = {}
        
        # Сопоставление фигур с файлами
        piece_files = {
            'K': 'white_king.png', 'Q': 'white_queen.png', 'R': 'white_rook.png',
            'B': 'white_bishop.png', 'N': 'white_knight.png', 'P': 'white_pawn.png',
            'k': 'black_king.png', 'q': 'black_queen.png', 'r': 'black_rook.png',
            'b': 'black_bishop.png', 'n': 'black_knight.png', 'p': 'black_pawn.png'
        }
        
        # Путь к папке с иконками
        icons_path = os.path.join(os.path.dirname(__file__), 'icons')
        
        for piece, filename in piece_files.items():
            try:
                file_path = os.path.join(icons_path, filename)
                if os.path.exists(file_path):
                    # Загружаем изображение
                    image = pygame.image.load(file_path).convert_alpha()
                    # Масштабируем до размера клетки
                    scaled_image = pygame.transform.smoothscale(image, 
                                                              (self.SQUARE_SIZE, self.SQUARE_SIZE))
                    pieces[piece] = scaled_image
                    print(f"Загружена иконка: {filename}")
                else:
                    print(f"Файл не найден: {filename}")
                    pieces[piece] = None
            except Exception as e:
                print(f"Ошибка загрузки {filename}: {e}")
                pieces[piece] = None
        
        return pieces
    
    def draw_board(self):
        """Отрисовка шахматной доски с улучшенной графикой"""
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                # Определение цвета клетки
                color = self.LIGHT_SQUARE if (row + col) % 2 == 0 else self.DARK_SQUARE
                
                # Выделение выбранной клетки
                if self.selected_square == (row, col):
                    color = self.SELECTED_COLOR
                elif (row, col) in self.valid_moves:
                    # Полупрозрачное выделение возможных ходов
                    highlight_surface = pygame.Surface((self.SQUARE_SIZE, self.SQUARE_SIZE), pygame.SRCALPHA)
                    highlight_surface.fill((*self.HIGHLIGHT_COLOR, 100))
                    rect = pygame.Rect(col * self.SQUARE_SIZE, row * self.SQUARE_SIZE, 
                                     self.SQUARE_SIZE, self.SQUARE_SIZE)
                    self.screen.blit(highlight_surface, rect)
                    continue  # Пропускаем обычную отрисовку клетки
                
                # Отрисовка клетки
                rect = pygame.Rect(col * self.SQUARE_SIZE, row * self.SQUARE_SIZE, 
                                 self.SQUARE_SIZE, self.SQUARE_SIZE)
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, self.BLACK, rect, 1)
                
                # Отрисовка фигуры
                piece = self.board[row][col]
                if piece != '.':
                    if piece in self.piece_images and self.piece_images[piece] is not None:
                        # Использование реальных иконок
                        piece_surface = self.piece_images[piece]
                        piece_rect = piece_surface.get_rect(center=rect.center)
                        self.screen.blit(piece_surface, piece_rect)
                    else:
                        # Резервный вариант - текстовые символы
                        unicode_symbols = {
                            'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
                            'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟'
                        }
                        symbol = unicode_symbols.get(piece, piece)
                        text_color = self.BLACK if piece.isupper() else self.RED
                        text = self.font.render(symbol, True, text_color)
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
    
    def draw_side_panel(self):
        """Отрисовка боковой панели с информацией"""
        panel_rect = pygame.Rect(640, 0, self.SIDE_PANEL_WIDTH, self.HEIGHT)
        pygame.draw.rect(self.screen, self.PANEL_BG, panel_rect)
        pygame.draw.line(self.screen, self.BLACK, (640, 0), (640, self.HEIGHT), 2)
        
        # Заголовок
        title = self.big_font.render("Информация", True, self.BLACK)
        self.screen.blit(title, (650, 20))
        
        # Текущий игрок
        player_text = "Белые" if self.white_turn else "Черные"
        turn_text = self.font.render(f"Ход: {player_text}", True, self.BLACK)
        self.screen.blit(turn_text, (650, 70))
        
        # Режим игры
        mode_text = "Против компьютера" if self.game_mode == 'computer' else "Два игрока"
        mode_render = self.small_font.render(mode_text, True, self.GRAY)
        self.screen.blit(mode_render, (650, 100))
        
        # Захваченные фигуры
        self.draw_captured_pieces(650, 130)
        
        # История ходов
        self.draw_move_history(650, 250)
        
        # Кнопки управления
        self.draw_control_buttons()
    
    def draw_captured_pieces(self, x, y):
        """Отрисовка захваченных фигур"""
        # Заголовок
        cap_title = self.small_font.render("Захвачено:", True, self.BLACK)
        self.screen.blit(cap_title, (x, y))
        
        # Белые фигуры (захваченные черными)
        white_captured = self.captured_pieces['white']
        if white_captured:
            white_text = self.small_font.render("Белые: " + ''.join(white_captured), True, self.BLACK)
            self.screen.blit(white_text, (x, y + 25))
        
        # Черные фигуры (захваченные белыми)
        black_captured = self.captured_pieces['black']
        if black_captured:
            black_text = self.small_font.render("Черные: " + ''.join(black_captured), True, self.BLACK)
            self.screen.blit(black_text, (x, y + 45))
    
    def draw_move_history(self, x, y):
        """Отрисовка истории ходов"""
        history_title = self.small_font.render("История ходов:", True, self.BLACK)
        self.screen.blit(history_title, (x, y))
        
        # Показываем последние 8 ходов
        start_index = max(0, len(self.move_history) - 8)
        for i, move in enumerate(self.move_history[start_index:], start_index):
            move_text = self.small_font.render(f"{i+1}. {move}", True, self.BLACK)
            self.screen.blit(move_text, (x, y + 25 + (i - start_index) * 20))
    
    def draw_control_buttons(self):
        """Отрисовка кнопок управления"""
        # Кнопка новой игры
        new_game_btn = pygame.Rect(650, 500, 140, 30)
        pygame.draw.rect(self.screen, (70, 130, 180), new_game_btn)
        pygame.draw.rect(self.screen, self.BLACK, new_game_btn, 2)
        new_game_text = self.small_font.render("Новая игра", True, self.WHITE)
        text_rect = new_game_text.get_rect(center=new_game_btn.center)
        self.screen.blit(new_game_text, text_rect)
        
        # Кнопка смены режима
        mode_btn = pygame.Rect(650, 540, 140, 30)
        mode_color = (220, 20, 60) if self.game_mode == 'computer' else (50, 205, 50)
        pygame.draw.rect(self.screen, mode_color, mode_btn)
        pygame.draw.rect(self.screen, self.BLACK, mode_btn, 2)
        mode_text = "Два игрока" if self.game_mode == 'computer' else "Против ИИ"
        mode_render = self.small_font.render(mode_text, True, self.WHITE)
        text_rect = mode_render.get_rect(center=mode_btn.center)
        self.screen.blit(mode_render, text_rect)
        
        # Кнопка выхода
        exit_btn = pygame.Rect(650, 580, 140, 30)
        pygame.draw.rect(self.screen, (169, 169, 169), exit_btn)
        pygame.draw.rect(self.screen, self.BLACK, exit_btn, 2)
        exit_text = self.small_font.render("Выход", True, self.BLACK)
        text_rect = exit_text.get_rect(center=exit_btn.center)
        self.screen.blit(exit_text, text_rect)
        
        return new_game_btn, mode_btn, exit_btn
    
    def get_square_from_mouse(self, pos: Tuple[int, int]) -> Tuple[int, int]:
        """Преобразование координат мыши в координаты доски"""
        x, y = pos
        col = x // self.SQUARE_SIZE
        row = y // self.SQUARE_SIZE
        return (row, col) if 0 <= row < 8 and 0 <= col < 8 else None
    
    def is_valid_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        """Проверка корректности хода с улучшенной логикой"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        piece = self.board[from_row][from_col]
        target_piece = self.board[to_row][to_col]
        
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
                target_piece == '.' and self.board[from_row + direction][from_col] == '.'):
                return True
                
            # Взятие по диагонали
            if (abs(from_col - to_col) == 1 and to_row == from_row + direction and 
                target_piece != '.' and target_piece.isupper() != is_white_piece):
                return True
                
            # Взятие на проходе (en passant)
            if (self.en_passant_target and to_pos == self.en_passant_target and 
                abs(from_col - to_col) == 1 and to_row == from_row + direction):
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
            
            # Обычный ход короля
            if row_diff <= 1 and col_diff <= 1:
                return not self.would_be_in_check(from_pos, to_pos)
            
            # Рокировка
            if row_diff == 0 and abs(col_diff) == 2 and not self.is_king_in_check(is_white_piece):
                # Короткая рокировка
                if col_diff == 2:  # Король идет вправо
                    if (self.castling_rights['K' if is_white_piece else 'k'] and
                        self.board[from_row][from_col + 1] == '.' and 
                        self.board[from_row][from_col + 2] == '.' and
                        not self.would_be_in_check(from_pos, (from_row, from_col + 1))):
                        return True
                # Длинная рокировка
                elif col_diff == -2:  # Король идет влево
                    if (self.castling_rights['Q' if is_white_piece else 'q'] and
                        self.board[from_row][from_col - 1] == '.' and 
                        self.board[from_row][from_col - 2] == '.' and
                        self.board[from_row][from_col - 3] == '.' and
                        not self.would_be_in_check(from_pos, (from_row, from_col - 1))):
                        return True
            
        # Логика для коня
        elif piece_type == 'n':
            row_diff = abs(to_row - from_row)
            col_diff = abs(to_col - from_col)
            return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)
            
        return False
    
    def is_king_in_check(self, king_color: bool) -> bool:
        """Проверка, находится ли король под шахом"""
        # Находим положение короля
        king_piece = 'K' if king_color else 'k'
        king_pos = None
        
        for row in range(8):
            for col in range(8):
                if self.board[row][col] == king_piece:
                    king_pos = (row, col)
                    break
            if king_pos:
                break
        
        if not king_pos:
            return False
            
        # Проверяем, может ли какая-либо вражеская фигура атаковать короля
        opponent_color = not king_color
        
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece != '.' and ((piece.isupper() and not opponent_color) or 
                                   (piece.islower() and opponent_color)):
                    # Временно меняем очередь хода для проверки
                    original_turn = self.white_turn
                    self.white_turn = opponent_color
                    if self.is_valid_move((row, col), king_pos):
                        self.white_turn = original_turn
                        return True
                    self.white_turn = original_turn
        
        return False
    
    def would_be_in_check(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        """Проверка, будет ли король под шахом после хода"""
        # Сохраняем текущее состояние
        original_board = [row[:] for row in self.board]
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Делаем временный ход
        piece = self.board[from_row][from_col]
        captured = self.board[to_row][to_col]
        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = '.'
        
        # Проверяем шах
        king_color = piece.isupper()
        in_check = self.is_king_in_check(king_color)
        
        # Восстанавливаем доску
        self.board = original_board
        
        return in_check
    
    def get_valid_moves(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Получение списка допустимых ходов для фигуры с проверкой шаха"""
        valid_moves = []
        for row in range(8):
            for col in range(8):
                if self.is_valid_move(pos, (row, col)):
                    # Проверка, что ход не приводит к шаху своему королю
                    if not self.would_be_in_check(pos, (row, col)):
                        valid_moves.append((row, col))
        return valid_moves
    
    def is_straight_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        """Проверка прямого хода (для ладьи и ферзя)"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Проверяем, что ход по прямой
        if from_row != to_row and from_col != to_col:
            return False
            
        # Проверяем, что между начальной и конечной позицией нет фигур
        if from_row == to_row:  # Горизонтальный ход
            start, end = sorted([from_col, to_col])
            for col in range(start + 1, end):
                if self.board[from_row][col] != '.':
                    return False
        else:  # Вертикальный ход
            start, end = sorted([from_row, to_row])
            for row in range(start + 1, end):
                if self.board[row][from_col] != '.':
                    return False
                    
        return True
    
    def is_diagonal_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        """Проверка диагонального хода (для слона и ферзя)"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Проверяем, что ход по диагонали
        if abs(from_row - to_row) != abs(from_col - to_col):
            return False
            
        # Проверяем, что между начальной и конечной позицией нет фигур
        row_step = 1 if to_row > from_row else -1
        col_step = 1 if to_col > from_col else -1
        
        row, col = from_row + row_step, from_col + col_step
        while (row, col) != (to_row, to_col):
            if self.board[row][col] != '.':
                return False
            row += row_step
            col += col_step
            
        return True
    
    def update_castling_rights(self, piece: str, pos: Tuple[int, int]):
        """Обновление прав на рокировку"""
        row, col = pos
        piece_type = piece.lower()
        
        # Если двигается король, теряет право на рокировку
        if piece_type == 'k':
            if piece.isupper():
                self.castling_rights['K'] = False
                self.castling_rights['Q'] = False
            else:
                self.castling_rights['k'] = False
                self.castling_rights['q'] = False
        
        # Если двигается ладья, теряет право на соответствующую рокировку
        elif piece_type == 'r':
            if row == 7 and col == 0:  # Белая левая ладья
                self.castling_rights['Q'] = False
            elif row == 7 and col == 7:  # Белая правая ладья
                self.castling_rights['K'] = False
            elif row == 0 and col == 0:  # Черная левая ладья
                self.castling_rights['q'] = False
            elif row == 0 and col == 7:  # Черная правая ладья
                self.castling_rights['k'] = False
    
    def is_checkmate(self) -> bool:
        """Проверка мата"""
        if not self.is_king_in_check(self.white_turn):
            return False
        
        # Проверяем, есть ли хоть один допустимый ход
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece != '.' and ((piece.isupper() and self.white_turn) or 
                                   (piece.islower() and not self.white_turn)):
                    moves = self.get_valid_moves((row, col))
                    if moves:
                        return False
        
        return True
    
    def is_stalemate(self) -> bool:
        """Проверка пата"""
        if self.is_king_in_check(self.white_turn):
            return False
        
        # Проверяем, есть ли хоть один допустимый ход
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece != '.' and ((piece.isupper() and self.white_turn) or 
                                   (piece.islower() and not self.white_turn)):
                    moves = self.get_valid_moves((row, col))
                    if moves:
                        return False
        
        return True
    
    def handle_button_click(self, pos):
        """Обработка кликов по кнопкам"""
        new_game_btn, mode_btn, exit_btn = self.draw_control_buttons()
        
        if new_game_btn.collidepoint(pos):
            self.new_game()
            return True
        elif mode_btn.collidepoint(pos):
            self.game_mode = 'two_players' if self.game_mode == 'computer' else 'computer'
            return True
        elif exit_btn.collidepoint(pos):
            return False
        return True
    
    def make_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]):
        """Выполнение хода с учетом всех правил шахмат"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Сохранение информации о ходе
        piece = self.board[from_row][from_col]
        captured = self.board[to_row][to_col]
        
        # Обновление прав на рокировку
        self.update_castling_rights(piece, from_pos)
        
        # Запись захваченной фигуры
        if captured != '.':
            captured_color = 'white' if captured.isupper() else 'black'
            self.captured_pieces[captured_color].append(captured.upper())
            self.halfmove_clock = 0  # Сброс счетчика при взятии
        else:
            self.halfmove_clock += 1
        
        # Обработка специальных ходов
        piece_type = piece.lower()
        
        # Рокировка
        if piece_type == 'k' and abs(from_col - to_col) == 2:
            # Перемещаем ладью
            if to_col > from_col:  # Короткая рокировка
                rook_from_col = 7
                rook_to_col = to_col - 1
            else:  # Длинная рокировка
                rook_from_col = 0
                rook_to_col = to_col + 1
            
            rook = self.board[from_row][rook_from_col]
            self.board[from_row][rook_to_col] = rook
            self.board[from_row][rook_from_col] = '.'
        
        # Взятие на проходе
        elif piece_type == 'p' and self.en_passant_target and to_pos == self.en_passant_target:
            captured_row = from_row
            captured_col = to_col
            captured_pawn = self.board[captured_row][captured_col]
            self.board[captured_row][captured_col] = '.'
            captured_color = 'white' if captured_pawn.isupper() else 'black'
            self.captured_pieces[captured_color].append(captured_pawn.upper())
        
        # Обновление цели взятия на проходе
        self.en_passant_target = None
        if piece_type == 'p' and abs(from_row - to_row) == 2:
            self.en_passant_target = ((from_row + to_row) // 2, from_col)
        
        # Превращение пешки
        if piece_type == 'p' and (to_row == 0 or to_row == 7):
            piece = 'Q' if piece.isupper() else 'q'  # Автоматическое превращение в ферзя
        
        # Запись хода в нотации
        from_square = chr(ord('a') + from_col) + str(8 - from_row)
        to_square = chr(ord('a') + to_col) + str(8 - to_row)
        piece_symbol = piece.upper() if piece.lower() != 'p' else ''
        capture_symbol = 'x' if captured != '.' else ''
        promotion_symbol = '=Q' if piece_type == 'p' and (to_row == 0 or to_row == 7) else ''
        
        move_notation = f"{piece_symbol}{from_square}{capture_symbol}{to_square}{promotion_symbol}"
        self.move_history.append(move_notation)
        
        # Выполнение хода
        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = '.'
        
        # Смена хода
        self.white_turn = not self.white_turn
        if self.white_turn:
            self.fullmove_number += 1
        
        # Сброс выбора
        self.selected_square = None
        self.valid_moves = []
        
        # Проверка окончания игры
        if self.is_checkmate():
            self.game_active = False
            winner = "Черные" if self.white_turn else "Белые"
            print(f"Шах и мат! Победили {winner}")
        elif self.is_stalemate():
            self.game_active = False
            print("Пат! Ничья")
        elif self.halfmove_clock >= 100:
            self.game_active = False
            print("Ничья по правилу 50 ходов")
    
    def update_castling_rights(self, piece: str, pos: Tuple[int, int]):
        """Обновление прав на рокировку"""
        row, col = pos
        piece_type = piece.lower()
        
        # Если двигается король, теряет право на рокировку
        if piece_type == 'k':
            if piece.isupper():
                self.castling_rights['K'] = False
                self.castling_rights['Q'] = False
            else:
                self.castling_rights['k'] = False
                self.castling_rights['q'] = False
        
        # Если двигается ладья, теряет право на соответствующую рокировку
        elif piece_type == 'r':
            if row == 7 and col == 0:  # Белая левая ладья
                self.castling_rights['Q'] = False
            elif row == 7 and col == 7:  # Белая правая ладья
                self.castling_rights['K'] = False
            elif row == 0 and col == 0:  # Черная левая ладья
                self.castling_rights['q'] = False
            elif row == 0 and col == 7:  # Черная правая ладья
                self.castling_rights['k'] = False
        
        # Если захватывается ладья, противник теряет право на соответствующую рокировку
        # (это обрабатывается в основном коде хода)
    
    def is_checkmate(self) -> bool:
        """Проверка мата"""
        if not self.is_king_in_check(self.white_turn):
            return False
        
        # Проверяем, есть ли хоть один допустимый ход
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece != '.' and ((piece.isupper() and self.white_turn) or 
                                   (piece.islower() and not self.white_turn)):
                    moves = self.get_valid_moves((row, col))
                    if moves:
                        return False
        
        return True
    
    def is_stalemate(self) -> bool:
        """Проверка пата"""
        if self.is_king_in_check(self.white_turn):
            return False
        
        # Проверяем, есть ли хоть один допустимый ход
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece != '.' and ((piece.isupper() and self.white_turn) or 
                                   (piece.islower() and not self.white_turn)):
                    moves = self.get_valid_moves((row, col))
                    if moves:
                        return False
        
        return True
    
    def handle_events(self):
        """Обработка событий с поддержкой боковой панели"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.game_active:
                    pos = pygame.mouse.get_pos()
                    # Проверяем клик по боковой панели
                    if pos[0] >= 640:
                        continue_running = self.handle_button_click(pos)
                        if not continue_running:
                            return False
                    else:
                        # Клик по доске
                        square = self.get_square_from_mouse(pos)
                        if square:
                            self.handle_square_click(square)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:  # Новая игра
                    self.new_game()
                elif event.key == pygame.K_m:  # Смена режима
                    self.game_mode = 'two_players' if self.game_mode == 'computer' else 'computer'
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
        """Начало новой игры с очисткой всей статистики"""
        self.board = self.get_initial_board()
        self.selected_square = None
        self.valid_moves = []
        self.game_active = True
        self.white_turn = True
        self.move_history = []
        self.captured_pieces = {'white': [], 'black': []}
    
    def draw(self):
        """Основная отрисовка с боковой панелью"""
        self.screen.fill(self.WHITE)
        self.draw_board()
        self.draw_coordinates()
        self.draw_side_panel()
        pygame.display.flip()
    
    def computer_move(self):
        """Простой компьютерный ход"""
        if self.white_turn or not self.game_active:
            return
            
        # Найдем все возможные ходы для черных
        possible_moves = []
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece != '.' and piece.islower():  # Черная фигура
                    moves = self.get_valid_moves((row, col))
                    for move in moves:
                        possible_moves.append(((row, col), move))
        
        # Сделаем случайный ход
        if possible_moves:
            from_pos, to_pos = random.choice(possible_moves)
            self.make_move(from_pos, to_pos)
    
    def run(self):
        """Основной цикл игры с компьютерным противником"""
        running = True
        computer_timer = 0
        COMPUTER_DELAY = 1000  # 1 секунда задержки для хода компьютера
        
        while running:
            running = self.handle_events()
            self.draw()
            
            # Ход компьютера с задержкой
            if not self.white_turn and self.game_active:
                computer_timer += self.clock.get_time()
                if computer_timer >= COMPUTER_DELAY:
                    self.computer_move()
                    computer_timer = 0
            
            self.clock.tick(60)  # 60 FPS
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = PygameChessGUI()
    game.run()