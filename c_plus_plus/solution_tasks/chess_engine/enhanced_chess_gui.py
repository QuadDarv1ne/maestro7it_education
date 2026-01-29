#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import random

class EnhancedChessGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Улучшенные шахматы")
        self.root.geometry("600x650")
        self.root.resizable(True, True)
        self.root.minsize(500, 550)
        
        # Привязка события изменения размера
        self.root.bind('<Configure>', self.on_window_resize)
        
        # Игровое состояние
        self.board = self.get_initial_board()
        self.selected_square = None
        self.valid_moves = []
        self.game_active = True
        self.white_turn = True
        self.move_history = []
        self.nodes_searched = 0
        
        # Настройки
        self.search_depth = 4
        self.thinking_time = 2
        
        self.setup_ui()
        
    def get_initial_board(self):
        """Начальная позиция"""
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
    
    def setup_ui(self):
        # Главный фрейм
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Верхняя панель
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Статус и статистика
        status_frame = ttk.Frame(top_frame)
        status_frame.pack(side=tk.LEFT)
        
        self.status_label = ttk.Label(status_frame, text="Белые ходят", 
                                     font=("Arial", 12, "bold"))
        self.status_label.pack()
        
        self.stats_label = ttk.Label(status_frame, text="Узлы: 0 | Ходы: 0")
        self.stats_label.pack()
        
        # Настройки
        settings_frame = ttk.Frame(top_frame)
        settings_frame.pack(side=tk.RIGHT)
        
        ttk.Label(settings_frame, text="Глубина:").pack(side=tk.LEFT)
        self.depth_var = tk.StringVar(value=str(self.search_depth))
        depth_spin = ttk.Spinbox(settings_frame, from_=1, to=8, 
                                textvariable=self.depth_var, width=5)
        depth_spin.pack(side=tk.LEFT, padx=(2, 10))
        
        ttk.Label(settings_frame, text="Время:").pack(side=tk.LEFT)
        self.time_var = tk.StringVar(value=str(self.thinking_time))
        time_spin = ttk.Spinbox(settings_frame, from_=1, to=5,
                               textvariable=self.time_var, width=5)
        time_spin.pack(side=tk.LEFT, padx=(2, 0))
        
        # Шахматная доска
        self.board_frame = ttk.Frame(main_frame, borderwidth=2, relief="ridge")
        self.board_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.create_board()
        
        # История ходов
        history_frame = ttk.LabelFrame(main_frame, text="История ходов", padding="5")
        history_frame.pack(fill=tk.BOTH, expand=True)
        
        self.history_text = tk.Text(history_frame, height=8, state=tk.DISABLED)
        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, 
                                 command=self.history_text.yview)
        self.history_text.configure(yscrollcommand=scrollbar.set)
        
        self.history_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Кнопки управления
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(button_frame, text="Новая игра", 
                  command=self.new_game).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Отменить ход", 
                  command=self.undo_move).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Сдаться", 
                  command=self.resign).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Выход", 
                  command=self.root.quit).pack(side=tk.RIGHT)
        
        # Настройка весов
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
    def create_board(self):
        """Создание адаптивной доски"""
        self.buttons = []
        for row in range(8):
            button_row = []
            for col in range(8):
                color = "white" if (row + col) % 2 == 0 else "#d3d3d3"
                btn = tk.Button(
                    self.board_frame,
                    bg=color,
                    font=("Arial", 16, "bold"),
                    width=3,
                    height=1,
                    command=lambda r=row, c=col: self.on_square_click(r, c)
                )
                btn.grid(row=7-row, column=col, padx=1, pady=1, sticky="nsew")
                button_row.append(btn)
            self.buttons.append(button_row)
        
        # Настройка равномерного растягивания
        for i in range(8):
            self.board_frame.grid_columnconfigure(i, weight=1)
            self.board_frame.grid_rowconfigure(i, weight=1)
        
        self.update_board_display()
        
    def update_board_display(self):
        """Обновление отображения доски"""
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                btn = self.buttons[row][col]
                
                # Установка текста фигуры
                btn.config(text=piece if piece != '.' else '')
                
                # Цвет текста
                if piece.isupper():
                    btn.config(fg='black')
                elif piece.islower():
                    btn.config(fg='red')
                else:
                    btn.config(fg='black')
                
                # Выделение выбранной клетки
                if self.selected_square == (row, col):
                    btn.config(bg="#90EE90", relief=tk.SUNKEN)
                elif (row, col) in self.valid_moves:
                    btn.config(bg="#FFFF99")
                else:
                    color = "white" if (row + col) % 2 == 0 else "#d3d3d3"
                    btn.config(bg=color, relief=tk.RAISED)
    
    def on_square_click(self, row, col):
        """Обработка клика по клетке"""
        if not self.game_active:
            return
            
        if self.selected_square is None:
            # Выбор фигуры
            piece = self.board[row][col]
            if piece != '.':
                is_white = piece.isupper()
                if (is_white and self.white_turn) or (not is_white and not self.white_turn):
                    self.selected_square = (row, col)
                    self.valid_moves = self.get_valid_moves(row, col)
                    self.update_board_display()
        else:
            # Выполнение хода
            if (row, col) in self.valid_moves:
                self.make_move(self.selected_square[0], self.selected_square[1], row, col)
            elif self.selected_square == (row, col):
                # Отмена выбора
                self.selected_square = None
                self.valid_moves = []
                self.update_board_display()
            else:
                # Выбор другой фигуры
                piece = self.board[row][col]
                if piece != '.':
                    is_white = piece.isupper()
                    if (is_white and self.white_turn) or (not is_white and not self.white_turn):
                        self.selected_square = (row, col)
                        self.valid_moves = self.get_valid_moves(row, col)
                        self.update_board_display()
                    else:
                        self.selected_square = None
                        self.valid_moves = []
                        self.update_board_display()
    
    def get_valid_moves(self, row, col):
        """Получение допустимых ходов (упрощенная реализация)"""
        valid_moves = []
        piece = self.board[row][col]
        
        # Пешка
        if piece.lower() == 'p':
            direction = -1 if piece.isupper() else 1
            start_row = 6 if piece.isupper() else 1
            
            # Ход вперед
            new_row = row + direction
            if 0 <= new_row < 8 and self.board[new_row][col] == '.':
                valid_moves.append((new_row, col))
                # Двойной ход
                if row == start_row and self.board[row + 2*direction][col] == '.':
                    valid_moves.append((row + 2*direction, col))
            
            # Взятие по диагонали
            for dc in [-1, 1]:
                new_col = col + dc
                new_row = row + direction
                if (0 <= new_row < 8 and 0 <= new_col < 8 and 
                    self.board[new_row][new_col] != '.' and
                    self.board[new_row][new_col].isupper() != piece.isupper()):
                    valid_moves.append((new_row, new_col))
        
        # Король (простое движение)
        elif piece.lower() == 'k':
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    new_row, new_col = row + dr, col + dc
                    if (0 <= new_row < 8 and 0 <= new_col < 8 and
                        (self.board[new_row][new_col] == '.' or 
                         self.board[new_row][new_col].isupper() != piece.isupper())):
                        valid_moves.append((new_row, new_col))
        
        return valid_moves
    
    def make_move(self, from_row, from_col, to_row, to_col):
        """Выполнение хода"""
        piece = self.board[from_row][from_col]
        captured = self.board[to_row][to_col]
        
        # Сохранение хода
        move_notation = self.coords_to_notation(from_row, from_col, to_row, to_col, captured)
        self.move_history.append(move_notation)
        
        # Выполнение хода
        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = '.'
        
        # Обновление интерфейса
        self.selected_square = None
        self.valid_moves = []
        self.update_board_display()
        
        # Статистика
        self.nodes_searched += 100
        self.update_stats()
        
        # Смена хода
        self.white_turn = not self.white_turn
        self.status_label.config(text="Белые ходят" if self.white_turn else "Черные ходят")
        
        # Добавление в историю
        self.add_to_history(move_notation)
        
        # Ход компьютера
        if self.game_active and not self.white_turn:
            self.status_label.config(text="Компьютер думает...")
            threading.Thread(target=self.computer_move, daemon=True).start()
    
    def coords_to_notation(self, from_row, from_col, to_row, to_col, captured):
        """Преобразование координат в шахматную нотацию"""
        files = 'abcdefgh'
        from_square = f"{files[from_col]}{8-from_row}"
        to_square = f"{files[to_col]}{8-to_row}"
        capture = 'x' if captured != '.' else ''
        return f"{from_square}{capture}{to_square}"
    
    def computer_move(self):
        """Ход компьютера (простая реализация)"""
        time.sleep(int(self.time_var.get()))
        
        # Поиск допустимых ходов для черных фигур
        possible_moves = []
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece != '.' and piece.islower():  # Черная фигура
                    moves = self.get_valid_moves(row, col)
                    for move in moves:
                        possible_moves.append(((row, col), move))
        
        if possible_moves:
            # Случайный ход
            from_pos, to_pos = random.choice(possible_moves)
            from_row, from_col = from_pos
            to_row, to_col = to_pos
            
            # Выполнение хода в основном потоке
            self.root.after(0, lambda: self.execute_computer_move(from_row, from_col, to_row, to_col))
        else:
            self.root.after(0, lambda: self.status_label.config(text="Мат или пат"))
    
    def execute_computer_move(self, from_row, from_col, to_row, to_col):
        """Выполнение хода компьютера в основном потоке"""
        piece = self.board[from_row][from_col]
        captured = self.board[to_row][to_col]
        
        move_notation = self.coords_to_notation(from_row, from_col, to_row, to_col, captured)
        self.move_history.append(move_notation)
        
        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = '.'
        
        self.nodes_searched += 150
        self.update_stats()
        self.update_board_display()
        self.add_to_history(move_notation)
        
        self.white_turn = True
        self.status_label.config(text="Белые ходят")
    
    def add_to_history(self, move):
        """Добавление хода в историю"""
        move_number = len(self.move_history)
        if move_number % 2 == 1:  # Белые
            history_text = f"{(move_number + 1) // 2}. {move}"
        else:  # Черные
            history_text = f"   {move}\n"
            
        self.history_text.config(state=tk.NORMAL)
        self.history_text.insert(tk.END, history_text)
        self.history_text.see(tk.END)
        self.history_text.config(state=tk.DISABLED)
    
    def update_stats(self):
        """Обновление статистики"""
        moves_count = len(self.move_history)
        self.stats_label.config(text=f"Узлы: {self.nodes_searched:,} | Ходы: {moves_count}")
    
    def new_game(self):
        """Новая игра"""
        self.board = self.get_initial_board()
        self.selected_square = None
        self.valid_moves = []
        self.game_active = True
        self.white_turn = True
        self.move_history = []
        self.nodes_searched = 0
        
        self.update_board_display()
        self.update_stats()
        
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        self.history_text.config(state=tk.DISABLED)
        
        self.status_label.config(text="Белые ходят")
    
    def undo_move(self):
        """Отмена последнего хода"""
        if self.move_history:
            self.move_history.pop()
            # Здесь должна быть логика восстановления позиции
            self.nodes_searched = max(0, self.nodes_searched - 100)
            self.update_stats()
            self.status_label.config(text="Ход отменен")
        else:
            self.status_label.config(text="Нет ходов для отмены")
    
    def resign(self):
        """Сдаться"""
        if messagebox.askyesno("Сдаться", "Вы уверены, что хотите сдаться?"):
            self.game_active = False
            self.status_label.config(text="Вы сдались")
    
    def on_window_resize(self, event):
        """Обработка изменения размера окна"""
        pass
    
    def run(self):
        """Запуск интерфейса"""
        self.root.mainloop()

if __name__ == "__main__":
    app = EnhancedChessGUI()
    app.run()