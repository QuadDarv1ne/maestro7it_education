#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading
import time
import os
import sys

class ChessGUIWithIcons:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Шахматный движок - Интерфейс с иконками")
        self.root.geometry("900x750")
        self.root.resizable(True, True)
        
        # Игровое состояние
        self.current_board = self.get_initial_board()
        self.selected_square = None
        self.move_history = []
        
        # Иконки фигур
        self.piece_icons = self.load_piece_icons()
        
        self.setup_ui()
        
    def get_initial_board(self):
        # Начальная позиция
        return [
            'r', 'n', 'b', 'q', 'k', 'b', 'n', 'r',
            'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p',
            ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
            ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
            ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
            ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
            'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P',
            'R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'
        ]
    
    def load_piece_icons(self):
        """Загрузка иконок фигур"""
        icons = {}
        icon_files = {
            'K': 'white_king.txt',
            'Q': 'white_queen.txt',
            'R': 'white_rook.txt',
            'B': 'white_bishop.txt',
            'N': 'white_knight.txt',
            'P': 'white_pawn.txt',
            'k': 'black_king.txt',
            'q': 'black_queen.txt',
            'r': 'black_rook.txt',
            'b': 'black_bishop.txt',
            'n': 'black_knight.txt',
            'p': 'black_pawn.txt'
        }
        
        for piece, filename in icon_files.items():
            try:
                with open(f'icons/{filename}', 'r', encoding='utf-8') as f:
                    icons[piece] = f.read().strip()
            except FileNotFoundError:
                # Используем Unicode символы если файлы не найдены
                unicode_map = {
                    'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
                    'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟'
                }
                icons[piece] = unicode_map.get(piece, '')
                
        return icons
    
    def setup_ui(self):
        # Основной фрейм
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Доска
        self.board_frame = ttk.Frame(main_frame, borderwidth=2, relief="ridge")
        self.board_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        
        self.create_board()
        
        # Панель управления
        control_frame = ttk.LabelFrame(main_frame, text="Управление", padding="10")
        control_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=10, pady=5)
        
        # Кнопки управления
        ttk.Button(control_frame, text="Новая игра", command=self.new_game).grid(row=0, column=0, padx=5)
        ttk.Button(control_frame, text="Отменить ход", command=self.undo_move).grid(row=0, column=1, padx=5)
        ttk.Button(control_frame, text="Сдаться", command=self.resign).grid(row=0, column=2, padx=5)
        
        # Информационная панель
        info_frame = ttk.LabelFrame(main_frame, text="Информация", padding="10")
        info_frame.grid(row=0, column=2, rowspan=2, sticky=(tk.N, tk.S, tk.E), padx=10, pady=10)
        
        self.status_label = ttk.Label(info_frame, text="Готов к игре", font=("Arial", 10, "bold"))
        self.status_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        ttk.Label(info_frame, text="Ход:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.turn_label = ttk.Label(info_frame, text="Белые")
        self.turn_label.grid(row=1, column=1, sticky=tk.W, pady=2)
        
        # История ходов
        history_frame = ttk.LabelFrame(info_frame, text="История ходов", padding="5")
        history_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        self.history_text = tk.Text(history_frame, width=25, height=20, state=tk.DISABLED)
        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.history_text.yview)
        self.history_text.configure(yscrollcommand=scrollbar.set)
        
        self.history_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Легенда фигур
        legend_frame = ttk.LabelFrame(info_frame, text="Легенда фигур", padding="5")
        legend_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        legend_text = "♔ - Белый король\n♕ - Белый ферзь\n♖ - Белая ладья\n♗ - Белый слон\n♘ - Белый конь\n♙ - Белая пешка\n\n♚ - Черный король\n♛ - Черный ферзь\n♜ - Черная ладья\n♝ - Черный слон\n♞ - Черный конь\n♟ - Черная пешка"
        
        legend_label = ttk.Label(legend_frame, text=legend_text, justify=tk.LEFT, font=("Arial", 9))
        legend_label.grid(row=0, column=0, sticky=tk.W)
        
        # Статус бар
        self.status_bar = ttk.Label(self.root, text="Готов", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Настройка весов для растягивания
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        info_frame.rowconfigure(2, weight=1)
        
    def create_board(self):
        self.buttons = []
        for row in range(8):
            button_row = []
            for col in range(8):
                color = "white" if (row + col) % 2 == 0 else "gray"
                btn = tk.Button(
                    self.board_frame,
                    width=6,
                    height=3,
                    bg=color,
                    font=("Arial", 16, "bold"),
                    command=lambda r=row, c=col: self.on_square_click(r, c)
                )
                btn.grid(row=7-row, column=col, padx=1, pady=1)
                button_row.append(btn)
            self.buttons.append(button_row)
        
        self.update_board_display()
        
    def update_board_display(self):
        for row in range(8):
            for col in range(8):
                piece = self.current_board[row * 8 + col]
                btn = self.buttons[row][col]
                
                # Установка иконки фигуры
                if piece != ' ' and piece in self.piece_icons:
                    icon = self.piece_icons[piece]
                    btn.config(text=icon)
                else:
                    btn.config(text='')
                
                # Цвет текста
                if piece.isupper():
                    btn.config(fg='black')
                elif piece.islower():
                    btn.config(fg='red')
                else:
                    btn.config(fg='black')
                    
    def on_square_click(self, row, col):
        square_index = row * 8 + col
        
        if self.selected_square is None:
            # Выбор фигуры
            piece = self.current_board[square_index]
            if piece != ' ':
                self.selected_square = square_index
                self.buttons[row][col].config(relief=tk.SUNKEN, bg="yellow")
        else:
            # Перемещение фигуры
            if self.selected_square == square_index:
                # Отмена выбора
                self.clear_selection()
            else:
                # Выполнение хода
                self.make_move(self.selected_square, square_index)
                
    def clear_selection(self):
        if self.selected_square is not None:
            row, col = self.selected_square // 8, self.selected_square % 8
            color = "white" if (row + col) % 2 == 0 else "gray"
            self.buttons[row][col].config(relief=tk.RAISED, bg=color)
            self.selected_square = None
            
    def make_move(self, from_square, to_square):
        # Преобразование координат в шахматную нотацию
        from_notation = self.square_to_notation(from_square)
        to_notation = self.square_to_notation(to_square)
        move = f"{from_notation}{to_notation}"
        
        # Выполнение хода
        piece = self.current_board[from_square]
        self.current_board[to_square] = piece
        self.current_board[from_square] = ' '
        
        # Обновление интерфейса
        self.clear_selection()
        self.update_board_display()
        
        # Добавление в историю
        piece_name = self.get_piece_name(piece)
        self.add_to_history(f"{piece_name}: {move}")
        
        # Обновление статуса
        self.status_bar.config(text=f"Выполнен ход: {piece_name} {move}")
        
        # Смена хода
        self.turn_label.config(text="Черные" if self.turn_label.cget("text") == "Белые" else "Белые")
        
    def square_to_notation(self, square):
        row, col = square // 8, square % 8
        file_char = chr(ord('a') + col)
        rank_char = str(8 - row)
        return file_char + rank_char
        
    def get_piece_name(self, piece):
        names = {
            'K': '♔ Король', 'Q': '♕ Ферзь', 'R': '♖ Ладья',
            'B': '♗ Слон', 'N': '♘ Конь', 'P': '♙ Пешка',
            'k': '♚ Король', 'q': '♛ Ферзь', 'r': '♜ Ладья',
            'b': '♝ Слон', 'n': '♞ Конь', 'p': '♟ Пешка'
        }
        return names.get(piece, piece)
        
    def add_to_history(self, move_text):
        self.history_text.config(state=tk.NORMAL)
        self.history_text.insert(tk.END, move_text + "\n")
        self.history_text.see(tk.END)
        self.history_text.config(state=tk.DISABLED)
        
    def new_game(self):
        self.current_board = self.get_initial_board()
        self.selected_square = None
        self.move_history = []
        self.update_board_display()
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        self.history_text.config(state=tk.DISABLED)
        self.turn_label.config(text="Белые")
        self.status_label.config(text="Новая игра начата")
        self.status_bar.config(text="Готов к игре")
        
    def undo_move(self):
        # Простая реализация отмены хода
        self.status_bar.config(text="Функция отмены хода в разработке")
            
    def resign(self):
        if messagebox.askyesno("Сдаться", "Вы уверены, что хотите сдаться?"):
            self.status_label.config(text="Вы сдались")
            self.status_bar.config(text="Игра завершена")
            
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ChessGUIWithIcons()
    app.run()