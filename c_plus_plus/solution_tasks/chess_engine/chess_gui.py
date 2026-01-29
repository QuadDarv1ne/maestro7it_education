import tkinter as tk
from tkinter import messagebox

class ChessGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Шахматная доска")
        self.root.geometry("500x500")
        self.root.configure(bg='white')
        
        # Начальная позиция
        self.board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]
        
        self.selected_piece = None
        self.selected_pos = None
        
        self.create_board()
        self.create_menu()
        
    def create_board(self):
        # Заголовок
        title = tk.Label(self.root, text="ШАХМАТНАЯ ДОСКА", 
                        font=("Arial", 16, "bold"), bg='white')
        title.pack(pady=10)
        
        # Доска
        self.board_frame = tk.Frame(self.root, bg='white')
        self.board_frame.pack(expand=True)
        
        self.buttons = []
        for row in range(8):
            button_row = []
            for col in range(8):
                color = 'tan' if (row + col) % 2 == 0 else 'saddle brown'
                btn = tk.Button(self.board_frame, 
                               width=4, height=2,
                               bg=color,
                               font=("Arial", 12, "bold"))
                
                piece = self.board[row][col]
                if piece != '.':
                    btn.config(text=piece)
                    if piece.isupper():
                        btn.config(fg='white')
                    else:
                        btn.config(fg='black')
                
                btn.grid(row=row, column=col, padx=1, pady=1)
                btn.bind('<Button-1>', lambda e, r=row, c=col: self.on_click(r, c))
                button_row.append(btn)
            self.buttons.append(button_row)
        
        # Координаты
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        for i, letter in enumerate(letters):
            lbl = tk.Label(self.board_frame, text=letter, font=("Arial", 10))
            lbl.grid(row=8, column=i)
        
        for i in range(8):
            lbl = tk.Label(self.board_frame, text=str(8-i), font=("Arial", 10))
            lbl.grid(row=i, column=8)
    
    def create_menu(self):
        menu_frame = tk.Frame(self.root, bg='white')
        menu_frame.pack(pady=10)
        
        tk.Button(menu_frame, text="Новая игра", 
                 command=self.new_game).pack(side=tk.LEFT, padx=5)
        tk.Button(menu_frame, text="Выход", 
                 command=self.root.quit).pack(side=tk.LEFT, padx=5)
    
    def on_click(self, row, col):
        piece = self.board[row][col]
        
        if self.selected_piece is None:
            # Выбор фигуры
            if piece != '.':
                self.selected_piece = piece
                self.selected_pos = (row, col)
                self.buttons[row][col].config(relief='sunken')
        else:
            # Перемещение фигуры
            old_row, old_col = self.selected_pos
            
            # Обновляем доску
            self.board[row][col] = self.selected_piece
            self.board[old_row][old_col] = '.'
            
            # Обновляем кнопки
            self.update_button(old_row, old_col)
            self.update_button(row, col)
            
            # Сбрасываем выделение
            self.buttons[old_row][old_col].config(relief='raised')
            self.selected_piece = None
            self.selected_pos = None
    
    def update_button(self, row, col):
        btn = self.buttons[row][col]
        piece = self.board[row][col]
        
        if piece == '.':
            btn.config(text='', bg='tan' if (row + col) % 2 == 0 else 'saddle brown')
        else:
            btn.config(text=piece)
            if piece.isupper():
                btn.config(fg='white')
            else:
                btn.config(fg='black')
    
    def new_game(self):
        self.board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]
        
        for row in range(8):
            for col in range(8):
                self.update_button(row, col)
        
        self.selected_piece = None
        self.selected_pos = None
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ChessGUI()
    app.run()