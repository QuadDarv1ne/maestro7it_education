import pygame

# Константы отображения
BOARD_SIZE = 512
SQUARE_SIZE = BOARD_SIZE // 8
LIGHT_SQUARE = (240, 217, 181)
DARK_SQUARE = (181, 136, 99)
HIGHLIGHT_COLOR = (124, 252, 0, 180)

# Инициализация шрифта
try:
    FONT = pygame.font.SysFont('Segoe UI Symbol', SQUARE_SIZE - 10)
except:
    FONT = pygame.font.SysFont('Arial', SQUARE_SIZE - 10)

PIECE_UNICODE = {
    'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',
    'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚'
}

class BoardRenderer:
    def __init__(self, screen, player_color='white'):
        self.screen = screen
        self.player_color = player_color
        self.selected_square = None

    def set_selected(self, square):
        self.selected_square = square

    def clear_selected(self):
        self.selected_square = None

    def _fen_to_display(self, row, col):
        """Преобразует FEN-координаты в экранные с учётом стороны игрока"""
        if self.player_color == 'black':
            return 7 - row, 7 - col
        return row, col

    def draw(self, board_state):
        for row in range(8):
            for col in range(8):
                color = LIGHT_SQUARE if (row + col) % 2 == 0 else DARK_SQUARE
                rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(self.screen, color, rect)

                if self.selected_square == (row, col):
                    highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                    highlight.fill(HIGHLIGHT_COLOR)
                    self.screen.blit(highlight, rect.topleft)

                piece = board_state[row][col]
                if piece:
                    disp_row, disp_col = self._fen_to_display(row, col)
                    screen_rect = pygame.Rect(
                        disp_col * SQUARE_SIZE, 
                        disp_row * SQUARE_SIZE, 
                        SQUARE_SIZE, 
                        SQUARE_SIZE
                    )
                    text_color = (0, 0, 0) if piece.isupper() else (50, 50, 50)
                    try:
                        text = FONT.render(PIECE_UNICODE[piece], True, text_color)
                    except:
                        text = FONT.render(piece, True, text_color)
                    text_rect = text.get_rect(center=screen_rect.center)
                    self.screen.blit(text, text_rect)