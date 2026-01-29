#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import os
from urllib.parse import urlparse
import time

def download_flaticon_icons():
    """Скачивание иконок фигур с Flaticon"""
    
    # URL иконок с Flaticon
    icon_urls = {
        'white_king.png': 'https://cdn-icons-png.flaticon.com/512/11497/11497350.png',
        'white_queen.png': 'https://cdn-icons-png.flaticon.com/512/11497/11497351.png',
        'white_rook.png': 'https://cdn-icons-png.flaticon.com/512/11497/11497352.png',
        'white_bishop.png': 'https://cdn-icons-png.flaticon.com/512/11497/11497353.png',
        'white_knight.png': 'https://cdn-icons-png.flaticon.com/512/11497/11497354.png',
        'white_pawn.png': 'https://cdn-icons-png.flaticon.com/512/11497/11497355.png',
        'black_king.png': 'https://cdn-icons-png.flaticon.com/512/11497/11497356.png',
        'black_queen.png': 'https://cdn-icons-png.flaticon.com/512/11497/11497357.png',
        'black_rook.png': 'https://cdn-icons-png.flaticon.com/512/11497/11497358.png',
        'black_bishop.png': 'https://cdn-icons-png.flaticon.com/512/11497/11497359.png',
        'black_knight.png': 'https://cdn-icons-png.flaticon.com/512/11497/11497360.png',
        'black_pawn.png': 'https://cdn-icons-png.flaticon.com/512/11497/11497361.png'
    }
    
    # Создание директории
    os.makedirs('flaticon_icons', exist_ok=True)
    
    print("Начинаю загрузку Flaticon иконок...")
    print("=" * 50)
    
    downloaded = 0
    failed = 0
    
    for filename, url in icon_urls.items():
        try:
            print(f"Загружаю {filename}...")
            
            # Загрузка файла
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                # Сохранение файла
                with open(f'flaticon_icons/{filename}', 'wb') as f:
                    f.write(response.content)
                
                # Проверка размера файла
                file_size = os.path.getsize(f'flaticon_icons/{filename}')
                print(f"  ✓ Успешно загружено ({file_size} bytes)")
                downloaded += 1
            else:
                print(f"  ✗ Ошибка: HTTP {response.status_code}")
                failed += 1
                
        except requests.exceptions.RequestException as e:
            print(f"  ✗ Ошибка сети: {e}")
            failed += 1
        except Exception as e:
            print(f"  ✗ Ошибка: {e}")
            failed += 1
            
        # Небольшая пауза между загрузками
        time.sleep(0.5)
    
    print("=" * 50)
    print(f"Загрузка завершена!")
    print(f"Успешно: {downloaded}")
    print(f"Ошибок: {failed}")
    
    # Проверка загруженных файлов
    print("\nЗагруженные файлы:")
    for filename in icon_urls.keys():
        if os.path.exists(f'flaticon_icons/{filename}'):
            size = os.path.getsize(f'flaticon_icons/{filename}')
            print(f"  {filename} ({size} bytes)")
        else:
            print(f"  {filename} - не найден")
            
    return downloaded, failed

def create_flaticon_gui():
    """Создание GUI с поддержкой Flaticon иконок"""
    
    gui_code = '''
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
'''
    
    with open('flaticon_chess_gui.py', 'w', encoding='utf-8') as f:
        f.write(gui_code)
    
    print("Создан файл flaticon_chess_gui.py")

if __name__ == "__main__":
    # Загрузка иконок
    downloaded, failed = download_flaticon_icons()
    
    # Создание GUI если иконки загружены
    if downloaded > 0:
        print("\n" + "=" * 50)
        create_flaticon_gui()
        print("Создан GUI с Flaticon иконками!")
        print("Запустите: python flaticon_chess_gui.py")
    else:
        print("Не удалось загрузить иконки")