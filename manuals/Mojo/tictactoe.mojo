# tictactoe.mojo — Крестики-нолики против непобедимого ИИ (минимакс)
# Демонстрирует: рекурсию, minimax, работу с состоянием, ввод пользователя

from std.str import atoi


# ── Типы ──
alias Board = List[String]


# ── Создание пустой доски ──
def make_board() -> Board:
    var b: Board = []
    for i in range(9):
        b.append(t"{i + 1}")  # Ячейки 1-9, чтобы игрок мог вводить номер
    return b


# ── Отрисовка доски ──
def render(board: Board, message: String = "") -> String:
    var out = String("\x1b[H")
    out += "╔═══════════════════════╗\n"
    out += "║  КРЕСТИКИ-НОЛИКИ      ║\n"
    out += "╠═══════════════════════╣\n"
    out += t"║   {board[0]}  │  {board[1]}  │  {board[2]}    ║\n"
    out += "║  ───┼───┼───          ║\n"
    out += t"║   {board[3]}  │  {board[4]}  │  {board[5]}    ║\n"
    out += "║  ───┼───┼───          ║\n"
    out += t"║   {board[6]}  │  {board[7]}  │  {board[8]}    ║\n"
    out += "╚═══════════════════════╝\n"
    if len(message) > 0:
        out += t"  {message}\n"
    return out


# ── Проверка победителя ──
# Возвращает "X", "O" или "" (пусто)
def check_winner(board: Board) -> String:
    let lines: List[(Int, Int, Int)] = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),   # горизонтали
        (0, 3, 6), (1, 4, 7), (2, 5, 8),   # вертикали
        (0, 4, 8), (2, 4, 6)                # диагонали
    ]
    for (a, b, c) in lines:
        if board[a] == board[b] and board[b] == board[c]:
            if board[a] == "X" or board[a] == "O":
                return board[a]
    return ""


# ── Проверка заполненности ──
def is_full(board: Board) -> Bool:
    for cell in board:
        if cell != "X" and cell != "O":
            return False
    return True


# ── Получить список свободных ячеек ──
def available_moves(board: Board) -> List[Int]:
    var moves: List[Int] = []
    for i in range(9):
        if board[i] != "X" and board[i] != "O":
            moves.append(i)
    return moves


# ── Минимакс ──
# Возвращает оценку позиции: +10 (победа AI), -10 (победа человека), 0 (ничья)
def minimax(board: Board, depth: Int, is_maximizing: Bool) -> Int:
    let winner = check_winner(board)

    if winner == "O":       # AI победил
        return 10 - depth
    elif winner == "X":     # Игрок победил
        return depth - 10
    elif is_full(board):    # Ничья
        return 0

    if is_maximizing:
        # Ход AI — максимизируем оценку
        var best = -1000
        for move in available_moves(board):
            board[move] = "O"
            let score = minimax(board, depth + 1, False)
            board[move] = t"{move + 1}"  # откат
            if score > best:
                best = score
        return best
    else:
        # Ход игрока — минимизируем оценку
        var best = 1000
        for move in available_moves(board):
            board[move] = "X"
            let score = minimax(board, depth + 1, True)
            board[move] = t"{move + 1}"  # откат
            if score < best:
                best = score
        return best


# ── Лучший ход для AI ──
def best_move(board: Board) -> Int:
    var best_score = -1000
    var best = -1

    for move in available_moves(board):
        board[move] = "O"
        let score = minimax(board, 0, False)
        board[move] = t"{move + 1}"  # откат
        if score > best_score:
            best_score = score
            best = move

    return best


# ── Ход игрока ──
def player_move(board: Board) -> Int:
    while True:
        print("\n  Ваш ход (1-9): ", end="")
        let input = input()
        try:
            let choice = atoi(input.strip()) - 1
            if 0 <= choice < 9:
                if board[choice] != "X" and board[choice] != "O":
                    return choice
                else:
                    print("  Эта клетка уже занята. Попробуйте другую.")
            else:
                print("  Введите число от 1 до 9.")
        except:
            print("  Некорректный ввод. Введите число от 1 до 9.")


# ── Точка входа ──
def main():
    print("\x1b[2J", end="")

    var board = make_board()
    var moves_count = 0

    print(render(board, "Вы — X, компьютер — O. Введите номер клетки."))

    while True:
        # Ход игрока
        let pm = player_move(board)
        board[pm] = "X"
        moves_count += 1

        var winner = check_winner(board)
        if winner == "X":
            print(render(board, "🎉 Вы победили"))
            break
        if is_full(board):
            print(render(board, "🤝 Ничья"))
            break

        # Ход AI
        print(render(board, "Компьютер думает..."))
        let ai = best_move(board)
        board[ai] = "O"
        moves_count += 1

        winner = check_winner(board)
        if winner == "O":
            print(render(board, "💻 Компьютер победил. Попробуйте ещё раз"))
            break
        if is_full(board):
            print(render(board, "🤝 Ничья"))
            break

        print(render(board, t"Ваш ход. Сделано ходов: {moves_count}"))

    print("\n  Спасибо за игру 👍\n")


if __name__ == "__main__":
    main()
