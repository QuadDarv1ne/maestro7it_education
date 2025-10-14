import pygame
from engine.stockfish_wrapper import StockfishWrapper
from ui.board_renderer import BoardRenderer

class ChessGame:
    def __init__(self, player_color='white', skill_level=5):
        self.player_color = player_color
        self.engine = StockfishWrapper(skill_level=skill_level)
        self.screen = pygame.display.set_mode((512, 512))
        pygame.display.set_caption("♟️ chess_stockfish — Maestro7IT")
        self.renderer = BoardRenderer(self.screen, player_color)
        self.clock = pygame.time.Clock()
        self.running = True

    def _coord_to_fen_square(self, x, y):
        col = x // 64
        row = y // 64
        if self.player_color == 'black':
            row = 7 - row
            col = 7 - col
        return row, col

    def _fen_square_to_uci(self, row, col):
        return chr(ord('a') + col) + str(8 - row)

    def _is_player_turn(self):
        side = self.engine.get_side_to_move()
        return (
            (self.player_color == 'white' and side == 'w') or
            (self.player_color == 'black' and side == 'b')
        )

    def _is_player_piece(self, piece):
        if not piece:
            return False
        is_white = piece.isupper()
        return (self.player_color == 'white') == is_white

    def handle_click(self, x, y):
        row, col = self._coord_to_fen_square(x, y)
        board = self.engine.get_board_state()
        piece = board[row][col]

        if self._is_player_turn() and self._is_player_piece(piece):
            self.renderer.set_selected((row, col))
        elif self.renderer.selected_square:
            from_sq = self.renderer.selected_square
            to_sq = (row, col)
            uci_move = self._fen_square_to_uci(*from_sq) + self._fen_square_to_uci(*to_sq)

            if self.engine.is_move_correct(uci_move):
                self.engine.make_move(uci_move)
                self.renderer.clear_selected()

                # Ход ИИ, если нужно
                if not self._is_player_turn() and not self.engine.is_game_over():
                    ai_move = self.engine.get_best_move()
                    if ai_move:
                        self.engine.make_move(ai_move)
            else:
                self.renderer.clear_selected()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x, y = pygame.mouse.get_pos()
                        self.handle_click(x, y)

            self.screen.fill((0, 0, 0))
            board = self.engine.get_board_state()
            self.renderer.draw(board)
            pygame.display.flip()
            self.clock.tick(60)

            if self.engine.is_game_over():
                fen = self.engine.get_fen()
                if 'mate' in fen:
                    print("🏆 Шах и мат!")
                else:
                    print("🤝 Пат!")
                pygame.time.wait(3000)
                self.running = False