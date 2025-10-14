from stockfish import Stockfish

class StockfishWrapper:
    def __init__(self, skill_level=5, depth=10, path=None):
        try:
            self.engine = Stockfish(path=path)
        except Exception as e:
            raise RuntimeError(f"Не удалось запустить Stockfish: {e}")
        
        self.engine.set_skill_level(skill_level)
        self.engine.set_depth(depth)

    def get_board_state(self):
        """Возвращает доску 8x8 из FEN"""
        fen = self.engine.get_fen_position()
        board_str = fen.split()[0]
        rows = board_str.split('/')
        board = []
        for row in rows:
            new_row = []
            for char in row:
                if char.isdigit():
                    new_row.extend([None] * int(char))
                else:
                    new_row.append(char)
            board.append(new_row)
        return board

    def is_move_correct(self, uci_move):
        return self.engine.is_move_correct(uci_move)

    def make_move(self, uci_move):
        self.engine.make_moves_from_current_position([uci_move])

    def get_best_move(self):
        return self.engine.get_best_move()

    def get_side_to_move(self):
        return self.engine.get_fen_position().split()[1]  # 'w' or 'b'

    def is_game_over(self):
        fen = self.engine.get_fen_position()
        return 'mate' in fen or 'stalemate' in fen

    def get_fen(self):
        return self.engine.get_fen_position()