import random
import time
import os
import threading
import sys

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COLORS = True
except ImportError:
    COLORS = False
    print("Для ярких цветов: pip install colorama")

# Глобальные переменные
player_spam_count = 0  # Считаем нажатия Enter во время гонки
running = True
lock = threading.Lock()

# Конфиг
RUNNERS = ["🎅 Дед Мороз (ты)", "🦌 Дэнсер", "🦌 Прансер", "🦌 Виксен", "🦌 Комета"]
SYMBOLS = ["🎅", "🦌", "🦌", "🦌", "🦌"]
TRACK_LENGTH = 50

def beep():
    print('\a', end='', flush=True)
    if os.name == 'nt':
        try:
            import winsound
            winsound.Beep(900, 150)
        except:
            pass

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def color_text(text, color="WHITE"):
    if not COLORS:
        return text
    colors = {
        "RED": Fore.RED, 
        "GREEN": Fore.GREEN, 
        "YELLOW": Fore.YELLOW,
        "CYAN": Fore.CYAN, 
        "MAGENTA": Fore.MAGENTA, 
        "WHITE": Style.RESET_ALL
    }
    return colors.get(color, "") + text + Style.RESET_ALL

def draw_track(positions, events=None):
    clear_screen()
    print(color_text("""
   ___              _          ___           _     
  / __|__ _ _ _  __| |_ __ _  |   \\  __ _ ___| |__
  \\__ \\ _` | ' \\/ _` | ' \\ || | |) / _` / _ \\ '_ \\
  |___/__,_|_||_\\__,_|_|_|_| |___/\\__,_\\___/_.__/

          🎅🦌 🏁 SANTA DASH 2025 🏁 🦌🎅
""", "RED"))

    for i, name in enumerate(RUNNERS):
        pos = min(positions[i], TRACK_LENGTH)
        track = " " * pos + SYMBOLS[i] + "—" * (TRACK_LENGTH - pos) + "🎄"
        progress = f"{pos}/{TRACK_LENGTH}"
        name_col = color_text(f"{name:24}", "CYAN" if i == 0 else "WHITE")
        print(f"{name_col} |{track}| {color_text(progress, 'YELLOW')}")

    if events:
        print(color_text("\n🎲 События:", "MAGENTA"))
        for e in events:
            print(f"   → {e}")

    print(color_text(f"\n🔥 Спамь Enter — ускоряй Деда Мороза. Текущий бонус: +{player_spam_count // 3}", "GREEN"))

def random_event():
    global victim
    events = []
    et = random.choice(["none", "snow", "gift", "wolf", "aurora"])
    if et == "snow":
        events.append("❄️ Метель! Все -1..2 шага")
        return events, lambda p: [max(0, x - random.randint(1,2)) for x in p]
    elif et == "gift":
        events.append("🎁 Подарок! Ты +4 шага")
        return events, "gift"
    elif et == "wolf":
        victim = random.randint(1, len(RUNNERS)-1)
        events.append(f"🐺 Волк атакует {RUNNERS[victim]}! -4 шага")
        return events, "wolf"
    elif et == "aurora":
        events.append("🌟 Северное сияние! ИИ +3 шага")
        return events, "aurora"
    return ["Всё тихо..."], None

# Неблокирующий спам Enter (только во время гонки!)
def spam_thread():
    global player_spam_count, running
    print(color_text("\n🚀 Гонка началась ... Спамь Enter как можно быстрее !!!\n", "YELLOW"))
    time.sleep(2)  # Время на подготовку рук

    while running:
        if sys.platform == "win32":
            import msvcrt
            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key in (b'\r', b'\n'):
                    with lock:
                        player_spam_count += 1
        else:  # Linux/macOS
            import select
            if select.select([sys.stdin], [], [], 0.01) == ([sys.stdin], [], []):
                key = sys.stdin.read(1)
                if key in ('\r', '\n'):
                    with lock:
                        player_spam_count += 1
        time.sleep(0.01)

def race():
    global player_spam_count, running, DIFFICULTY
    DIFFICULTY = 2
    positions = [0] * len(RUNNERS)
    events_log = []
    turn = 0

    clear_screen()
    print(color_text("🎄 Добро пожаловать в SANTA DASH 🎄\n", "GREEN"))
    print("Сложность:")
    print("1 — Легко")
    print("2 — Нормально (рекомендую)")
    print("3 — Хардкор")
    try:
        ch = input(color_text("\nВыбор [1-3, Enter=2]: ", "YELLOW")).strip()
        DIFFICULTY = int(ch) if ch in '123' else 2
    except:
        DIFFICULTY = 2

    print(color_text("\n3... 2... 1... СТАРТ!!!", "RED"))
    beep()
    time.sleep(1)

    player_spam_count = 0
    running = True
    threading.Thread(target=spam_thread, daemon=True).start()

    while max(positions) < TRACK_LENGTH:
        draw_track(positions, events_log)
        time.sleep(0.1)

        with lock:
            bonus = player_spam_count // 3
            player_move = random.randint(2, 4) + bonus
            positions[0] = min(positions[0] + player_move, TRACK_LENGTH)
            player_spam_count %= 3  # Остаток

        # ИИ ходы
        for i in range(1, len(RUNNERS)):
            ai_move = random.randint(2, 4 + DIFFICULTY)
            positions[i] = min(positions[i] + ai_move, TRACK_LENGTH)

        # Случайные события
        turn += 1
        if random.random() < 0.25:  # ~ каждые 4 хода
            events_log, effect = random_event()
            if effect == "gift":
                positions[0] = min(positions[0] + 4, TRACK_LENGTH)
            elif effect == "wolf" and victim is not None:
                positions[victim] = max(0, positions[victim] - 4)
            elif effect == "aurora":
                for i in range(1, len(RUNNERS)):
                    positions[i] = min(positions[i] + 3, TRACK_LENGTH)
            elif callable(effect):
                positions = effect(positions)
            time.sleep(1.2)

        events_log = []

    running = False
    beep(); time.sleep(0.2); beep()

    draw_track(positions)
    winner = max(range(len(positions)), key=lambda i: positions[i])
    if winner == 0:
        print(color_text("\n🎉🎄 ТЫ ПОБЕДИЛ. С НОВЫМ 2026 ГОДОМ 🎄🎉", "GREEN"))
        print(color_text("   Легенда спама Enter 🏆✨", "YELLOW"))
    else:
        print(color_text(f"\n🏆 Победил: {RUNNERS[winner]}", "RED"))
        print(color_text("   Спамь быстрее в следующий раз 🔥", "YELLOW"))

    print(color_text("\nСыграть ещё раз? (да / любой ключ — выход): ", "CYAN"), end='')
    try:
        if input().strip().lower().startswith('д'):
            race()
    except:
        pass

if __name__ == "__main__":
    race()