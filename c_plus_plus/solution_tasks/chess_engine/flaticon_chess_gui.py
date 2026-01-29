
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os

class FlaticonChessGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Шахматы с Flaticon иконками")
        self.root.geometry("900x750")
        
        # Загрузка иконок
        self.piece_images = self.load_flaticon_images()
        
        # Игровое состояние
        self.current_board = self.get_initial_board()
        self.selected_square = None
        
        self.setup_ui()
        
    def get_initial_board(self):
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
    
    def load_flaticon_images(self):
        """Загрузка Flaticon иконок"""
        images = {}
        image_files = {
            'K': 'white_king.png', 'Q': 'white_queen.png', 'R': 'white_rook.png',
            'B': 'white_bishop.png', 'N': 'white_knight.png', 'P': 'white_pawn.png',
            'k': 'black_king.png', 'q': 'black_queen.png', 'r': 'black_rook.png',
            'b': 'black_bishop.png', 'n': 'black_knight.png', 'p': 'black_pawn.png'
        }
        
        for piece, filename in image_files.items():
            try:
                if os.path.exists(f'flaticon_icons/{filename}'):
                    # Загрузка и изменение размера
                    image = Image.open(f'flaticon_icons/{filename}')
                    image = image.resize((40, 40), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(image)
                    images[piece] = photo
                    print(f"Загружена иконка: {filename}")
                else:
                    print(f"Файл не найден: {filename}")
                    images[piece] = None
            except Exception as e:
                print(f"Ошибка загрузки {filename}: {e}")
                images[piece] = None
                
        return images
    
    def setup_ui(self):
        # Доска
        self.board_frame = ttk.Frame(self.root, borderwidth=2, relief="ridge")
        self.board_frame.pack(pady=20, padx=20)
        
        self.create_board()
        
        # Панель управления
        control_frame = ttk.Frame(self.root)
        control_frame.pack(pady=10)
        
        ttk.Button(control_frame, text="Новая игра", command=self.new_game).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Выйти", command=self.root.quit).pack(side=tk.LEFT, padx=5)
        
        # Статус
        self.status_label = ttk.Label(self.root, text="Готов к игре")
        self.status_label.pack(pady=5)
        
    def create_board(self):
        self.buttons = []
        for row in range(8):
            button_row = []
            for col in range(8):
                color = "white" if (row + col) % 2 == 0 else "lightgray"
                btn = tk.Button(
                    self.board_frame,
                    width=60,
                    height=60,
                    bg=color,
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
                
                # Очистка кнопки
                btn.config(image='', text='')
                
                # Установка иконки
                if piece != ' ' and piece in self.piece_images and self.piece_images[piece]:
                    btn.config(image=self.piece_images[piece])
                elif piece != ' ':
                    # Fallback на текст если иконка не загружена
                    btn.config(text=piece, font=("Arial", 20))
                    
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
                self.clear_selection()
            else:
                self.make_move(self.selected_square, square_index)
                
    def clear_selection(self):
        if self.selected_square is not None:
            row, col = self.selected_square // 8, self.selected_square % 8
            color = "white" if (row + col) % 2 == 0 else "lightgray"
            self.buttons[row][col].config(relief=tk.RAISED, bg=color)
            self.selected_square = None
            
    def make_move(self, from_square, to_square):
        # Выполнение хода
        piece = self.current_board[from_square]
        self.current_board[to_square] = piece
        self.current_board[from_square] = ' '
        
        # Обновление интерфейса
        self.clear_selection()
        self.update_board_display()
        self.status_label.config(text=f"Ход: {piece}")
        
    def new_game(self):
        self.current_board = self.get_initial_board()
        self.selected_square = None
        self.update_board_display()
        self.status_label.config(text="Новая игра")
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    # Проверка наличия PIL
    try:
        from PIL import Image, ImageTk
    except ImportError:
        print("Ошибка: Требуется библиотека PIL (Pillow)")
        print("Установите командой: pip install Pillow")
        exit(1)
    
    app = FlaticonChessGUI()
    app.run()
