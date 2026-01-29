#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading
import time
import os
import json

class OptimizedChessGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Оптимизированный шахматный движок")
        self.root.geometry("520x450")
        self.root.resizable(True, True)
        self.root.minsize(450, 400)
        
        # Привязка события изменения размера
        self.root.bind('<Configure>', self.on_window_resize)
        
        # Игровое состояние
        self.current_board = self.get_initial_board()
        self.selected_square = None
        self.move_history = []
        self.game_active = True
        
        # Настройки движка
        self.search_depth = 6
        self.thinking_time = 3
        self.use_advanced_engine = True
        
        # Статистика
        self.nodes_searched = 0
        self.moves_count = 0
        
        self.setup_ui()
        
    def get_initial_board(self):
        # Начальная позиция в FEN нотации
        return "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    
    def setup_ui(self):
        # Главный фрейм
        main_frame = ttk.Frame(self.root, padding="5")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Верхняя панель с информацией
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.status_label = ttk.Label(info_frame, text="Готов к игре", font=("Arial", 10, "bold"))
        self.status_label.pack(side=tk.LEFT)
        
        # Статистика
        stats_frame = ttk.Frame(info_frame)
        stats_frame.pack(side=tk.RIGHT)
        
        self.nodes_label = ttk.Label(stats_frame, text="Узлы: 0")
        self.nodes_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.moves_label = ttk.Label(stats_frame, text="Ходы: 0")
        self.moves_label.pack(side=tk.LEFT)
        
        # Шахматная доска
        self.board_frame = ttk.Frame(main_frame, borderwidth=2, relief="ridge")
        self.board_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        self.create_board()
        
        # Панель управления
        control_frame = ttk.LabelFrame(main_frame, text="Управление", padding="5")
        control_frame.pack(fill=tk.X, pady=(0, 5))
        
        # Кнопки
        button_frame = ttk.Frame(control_frame)
        button_frame.pack()
        
        ttk.Button(button_frame, text="Новая игра", command=self.new_game).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Отменить ход", command=self.undo_move).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Сдаться", command=self.resign).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Настройки", command=self.show_settings).pack(side=tk.LEFT, padx=2)
        
        # Настройки движка
        engine_frame = ttk.LabelFrame(main_frame, text="Настройки движка", padding="5")
        engine_frame.pack(fill=tk.X)
        
        settings_frame = ttk.Frame(engine_frame)
        settings_frame.pack()
        
        ttk.Label(settings_frame, text="Глубина:").pack(side=tk.LEFT)
        self.depth_var = tk.StringVar(value=str(self.search_depth))
        depth_spinbox = ttk.Spinbox(settings_frame, from_=1, to=12, textvariable=self.depth_var, width=5)
        depth_spinbox.pack(side=tk.LEFT, padx=(2, 10))
        
        ttk.Label(settings_frame, text="Время:").pack(side=tk.LEFT)
        self.time_var = tk.StringVar(value=str(self.thinking_time))
        time_spinbox = ttk.Spinbox(settings_frame, from_=1, to=10, textvariable=self.time_var, width=5)
        time_spinbox.pack(side=tk.LEFT, padx=(2, 10))
        
        self.advanced_var = tk.BooleanVar(value=self.use_advanced_engine)
        ttk.Checkbutton(settings_frame, text="Продвинутый движок", 
                       variable=self.advanced_var).pack(side=tk.LEFT)
        
        # История ходов
        history_frame = ttk.LabelFrame(main_frame, text="История ходов", padding="5")
        history_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        self.history_text = tk.Text(history_frame, height=6, state=tk.DISABLED)
        history_scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.history_text.yview)
        self.history_text.configure(yscrollcommand=history_scrollbar.set)
        
        self.history_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Настройка весов для адаптивности
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
    def create_board(self):
        # Создание адаптивной шахматной доски
        self.buttons = []
        for row in range(8):
            button_row = []
            for col in range(8):
                color = "white" if (row + col) % 2 == 0 else "#cccccc"
                btn = tk.Button(
                    self.board_frame,
                    bg=color,
                    font=("Arial", 12, "bold"),
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
        # Преобразование FEN в массив доски
        board_array = self.fen_to_board(self.current_board)
        
        for row in range(8):
            for col in range(8):
                piece = board_array[row][col]
                btn = self.buttons[row][col]
                
                # Установка текста фигуры
                btn.config(text=piece if piece != '.' else '')
                
                # Цвет текста
                if piece.isupper():
                    btn.config(fg='black')
                elif piece.islower():
                    btn.config(fg='#8B0000')  # Темно-красный
                else:
                    btn.config(fg='black')
                    
    def fen_to_board(self, fen):
        """Преобразование FEN нотации в массив 8x8"""
        parts = fen.split(' ')
        board_part = parts[0]
        rows = board_part.split('/')
        
        board = []
        for row in rows:
            board_row = []
            for char in row:
                if char.isdigit():
                    # Пустые клетки
                    board_row.extend(['.'] * int(char))
                else:
                    # Фигуры
                    board_row.append(char)
            board.append(board_row)
        
        return board
        
    def on_square_click(self, row, col):
        if not self.game_active:
            return
            
        square_index = row * 8 + col
        
        if self.selected_square is None:
            # Выбор фигуры
            board_array = self.fen_to_board(self.current_board)
            piece = board_array[row][col]
            if piece != '.':
                self.selected_square = square_index
                self.buttons[row][col].config(relief=tk.SUNKEN, bg="#FFD700")  # Золотой
        else:
            # Перемещение фигуры
            if self.selected_square == square_index:
                self.clear_selection()
            else:
                self.make_move(self.selected_square, square_index)
                
    def clear_selection(self):
        if self.selected_square is not None:
            row, col = self.selected_square // 8, self.selected_square % 8
            color = "white" if (row + col) % 2 == 0 else "#cccccc"
            self.buttons[row][col].config(relief=tk.RAISED, bg=color)
            self.selected_square = None
            
    def make_move(self, from_square, to_square):
        # Преобразование координат в шахматную нотацию
        from_notation = self.square_to_notation(from_square)
        to_notation = self.square_to_notation(to_square)
        move = f"{from_notation}{to_notation}"
        
        # Обновление FEN позиции (упрощенная реализация)
        self.moves_count += 1
        self.add_to_history(f"Ход {self.moves_count}: {move}")
        
        # Обновление интерфейса
        self.clear_selection()
        self.update_board_display()
        
        # Обновление статистики
        self.nodes_searched += 1000  # Имитация поиска узлов
        self.update_stats()
        
        # Запрос хода от движка
        if self.game_active:
            self.status_label.config(text="Движок думает...")
            threading.Thread(target=self.get_engine_move, daemon=True).start()
        
    def square_to_notation(self, square):
        row, col = square // 8, square % 8
        file_char = chr(ord('a') + col)
        rank_char = str(8 - row)
        return file_char + rank_char
        
    def get_engine_move(self):
        # Имитация работы шахматного движка
        time.sleep(self.thinking_time)
        
        # Генерация случайного хода для демонстрации
        import random
        possible_moves = ["e7e5", "d7d5", "g8f6", "b8c6", "f8c5", "f8b4"]
        engine_move = random.choice(possible_moves)
        
        # Обновление интерфейса в главном потоке
        self.root.after(0, lambda: self.execute_engine_move(engine_move))
        
    def execute_engine_move(self, move):
        self.moves_count += 1
        self.add_to_history(f"Ход {self.moves_count}: {move} (движок)")
        self.nodes_searched += 1500  # Больше узлов для движка
        self.update_stats()
        self.status_label.config(text="Ваш ход")
        
    def add_to_history(self, move_text):
        self.history_text.config(state=tk.NORMAL)
        self.history_text.insert(tk.END, move_text + "\n")
        self.history_text.see(tk.END)
        self.history_text.config(state=tk.DISABLED)
        
    def update_stats(self):
        self.nodes_label.config(text=f"Узлы: {self.nodes_searched:,}")
        self.moves_label.config(text=f"Ходы: {self.moves_count}")
        
    def new_game(self):
        self.current_board = self.get_initial_board()
        self.selected_square = None
        self.move_history = []
        self.game_active = True
        self.moves_count = 0
        self.nodes_searched = 0
        
        self.update_board_display()
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        self.history_text.config(state=tk.DISABLED)
        
        self.update_stats()
        self.status_label.config(text="Новая игра начата")
        
    def undo_move(self):
        if self.move_history:
            self.move_history.pop()
            self.moves_count = max(0, self.moves_count - 1)
            self.update_stats()
            self.status_label.config(text="Ход отменен")
        else:
            self.status_label.config(text="Нет ходов для отмены")
            
    def resign(self):
        if messagebox.askyesno("Сдаться", "Вы уверены, что хотите сдаться?"):
            self.game_active = False
            self.status_label.config(text="Вы сдались")
            
    def show_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Настройки")
        settings_window.geometry("300x200")
        settings_window.resizable(False, False)
        
        ttk.Label(settings_window, text="Настройки шахматного движка", 
                 font=("Arial", 12, "bold")).pack(pady=10)
        
        ttk.Label(settings_window, text=f"Глубина поиска: {self.search_depth}").pack()
        ttk.Label(settings_window, text=f"Время на ход: {self.thinking_time} сек").pack()
        ttk.Label(settings_window, text=f"Продвинутый движок: {'Да' if self.use_advanced_engine else 'Нет'}").pack()
        
        ttk.Button(settings_window, text="OK", command=settings_window.destroy).pack(pady=20)
        
    def on_window_resize(self, event):
        # Адаптация при изменении размера окна
        pass
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = OptimizedChessGUI()
    app.run()