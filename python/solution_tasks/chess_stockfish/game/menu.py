def main_menu():
    print("\n" + "="*50)
    print("♟️  chess_stockfish — Maestro7IT")
    print("="*50)
    
    while True:
        side = input("Выберите сторону (white/black): ").strip().lower()
        if side in ('white', 'black'):
            break
        print("⚠️  Введите 'white' или 'black'.")

    while True:
        try:
            level = int(input("Уровень Stockfish (0–20): "))
            if 0 <= level <= 20:
                break
            print("⚠️  Введите число от 0 до 20.")
        except ValueError:
            print("⚠️  Неверный формат.")

    return side, level