#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading
import time
import os
import sys

class SynchronizedChessGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Шахматный движок - Синхронизированный интерфейс")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Игровое состояние
        self.current_board = self.get_initial_board()
        self.selected_square = None
        self.move_history = []
        self.engine_process = None
        self.is_engine_running = False
        
        # Настройки движка
        self.search_depth = 6
        self.thinking_time = 5
        
        self.setup_ui()
        self.start_engine()
        
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
        
        # Настройки движка
        engine_frame = ttk.LabelFrame(main_frame, text="Настройки движка", padding="10")
        engine_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=10, pady=5)
        
        ttk.Label(engine_frame, text="Глубина поиска:").grid(row=0, column=0, sticky=tk.W)
        self.depth_var = tk.StringVar(value=str(self.search_depth))
        depth_spinbox = ttk.Spinbox(engine_frame, from_=1, to=12, textvariable=self.depth_var, width=10)
        depth_spinbox.grid(row=0, column=1, padx=5)
        
        ttk.Label(engine_frame, text="Время на ход (сек):").grid(row=1, column=0, sticky=tk.W)
        self.time_var = tk.StringVar(value=str(self.thinking_time))
        time_spinbox = ttk.Spinbox(engine_frame, from_=1, to=30, textvariable=self.time_var, width=10)
        time_spinbox.grid(row=1, column=1, padx=5)
        
        # Информационная панель
        info_frame = ttk.LabelFrame(main_frame, text="Информация", padding="10")
        info_frame.grid(row=0, column=2, rowspan=3, sticky=(tk.N, tk.S, tk.E), padx=10, pady=10)
        
        self.status_label = ttk.Label(info_frame, text="Готов к игре", font=("Arial", 10, "bold"))
        self.status_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        ttk.Label(info_frame, text="Ход:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.turn_label = ttk.Label(info_frame, text="Белые")
        self.turn_label.grid(row=1, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(info_frame, text="Оценка позиции:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.eval_label = ttk.Label(info_frame, text="0.0")
        self.eval_label.grid(row=2, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(info_frame, text="Лучший ход:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.best_move_label = ttk.Label(info_frame, text="-")
        self.best_move_label.grid(row=3, column=1, sticky=tk.W, pady=2)
        
        # История ходов
        history_frame = ttk.LabelFrame(info_frame, text="История ходов", padding="5")
        history_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        self.history_text = tk.Text(history_frame, width=25, height=15, state=tk.DISABLED)
        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.history_text.yview)
        self.history_text.configure(yscrollcommand=scrollbar.set)
        
        self.history_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Статус бар
        self.status_bar = ttk.Label(self.root, text="Готов", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Настройка весов для растягивания
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        info_frame.rowconfigure(4, weight=1)
        
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
                    font=("Arial", 12, "bold"),
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
                
                # Установка текста фигуры
                btn.config(text=piece if piece != ' ' else '')
                
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
        self.add_to_history(f"Игрок: {move}")
        
        # Обновление статуса
        self.status_label.config(text="Движок думает...")
        self.status_bar.config(text=f"Выполнен ход: {move}")
        
        # Запрос хода от движка
        self.request_engine_move()
        
    def square_to_notation(self, square):
        row, col = square // 8, square % 8
        file_char = chr(ord('a') + col)
        rank_char = str(8 - row)
        return file_char + rank_char
        
    def start_engine(self):
        try:
            # Запуск шахматного движка
            engine_path = "build/chess_engine.exe" if os.name == 'nt' else "./build/chess_engine"
            
            if not os.path.exists(engine_path):
                messagebox.showerror("Ошибка", "Движок не найден. Пожалуйста, сначала соберите проект.")
                return
                
            self.engine_process = subprocess.Popen(
                [engine_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            self.is_engine_running = True
            self.status_bar.config(text="Движок запущен")
            
            # Инициализация UCI
            self.send_to_engine("uci")
            self.send_to_engine("isready")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось запустить движок: {str(e)}")
            
    def send_to_engine(self, command):
        if self.engine_process and self.engine_process.stdin:
            try:
                self.engine_process.stdin.write(command + '\n')
                self.engine_process.stdin.flush()
            except Exception as e:
                print(f"Ошибка отправки команды движку: {e}")
                
    def request_engine_move(self):
        # Запуск потока для получения хода от движка
        threading.Thread(target=self.get_engine_move, daemon=True).start()
        
    def get_engine_move(self):
        try:
            # Установка параметров
            self.send_to_engine(f"go depth {self.search_depth}")
            
            # Ожидание ответа
            start_time = time.time()
            while time.time() - start_time < self.thinking_time:
                if self.engine_process.poll() is not None:
                    break
                time.sleep(0.1)
                
            # Чтение лучшего хода
            self.send_to_engine("stop")
            
            # Здесь должна быть логика получения хода от движка
            # Пока используем случайный ход для демонстрации
            import random
            legal_moves = self.get_legal_moves()
            if legal_moves:
                engine_move = random.choice(legal_moves)
                self.root.after(0, lambda: self.execute_engine_move(engine_move))
                
        except Exception as e:
            print(f"Ошибка получения хода от движка: {e}")
            self.root.after(0, lambda: self.status_label.config(text="Ошибка движка"))
            
    def get_legal_moves(self):
        # Упрощенная реализация получения_legalных ходов
        # В реальной реализации нужно интегрировать с движком
        moves = []
        for from_square in range(64):
            piece = self.current_board[from_square]
            if piece.islower():  # Черные фигуры
                for to_square in range(64):
                    if self.is_valid_move(from_square, to_square):
                        moves.append((from_square, to_square))
        return moves
        
    def is_valid_move(self, from_square, to_square):
        # Упрощенная проверка хода
        if from_square == to_square:
            return False
        if self.current_board[from_square] == ' ':
            return False
        return True
        
    def execute_engine_move(self, move):
        from_square, to_square = move
        from_notation = self.square_to_notation(from_square)
        to_notation = self.square_to_notation(to_square)
        move_notation = f"{from_notation}{to_notation}"
        
        # Выполнение хода движка
        piece = self.current_board[from_square]
        self.current_board[to_square] = piece
        self.current_board[from_square] = ' '
        
        # Обновление интерфейса
        self.update_board_display()
        self.add_to_history(f"Движок: {move_notation}")
        self.status_label.config(text="Ваш ход")
        self.status_bar.config(text=f"Движок сделал ход: {move_notation}")
        
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
        self.status_label.config(text="Новая игра начата")
        self.status_bar.config(text="Готов к игре")
        
    def undo_move(self):
        if self.move_history:
            # Отмена последнего хода
            self.move_history.pop()
            # Здесь должна быть логика восстановления позиции
            self.status_bar.config(text="Ход отменен")
        else:
            self.status_bar.config(text="Нет ходов для отмены")
            
    def resign(self):
        if messagebox.askyesno("Сдаться", "Вы уверены, что хотите сдаться?"):
            self.status_label.config(text="Вы сдались")
            self.status_bar.config(text="Игра завершена")
            
    def run(self):
        self.root.mainloop()
        
        # Завершение работы движка
        if self.engine_process:
            try:
                self.send_to_engine("quit")
                self.engine_process.terminate()
                self.engine_process.wait(timeout=2)
            except:
                self.engine_process.kill()

if __name__ == "__main__":
    app = SynchronizedChessGUI()
    app.run()