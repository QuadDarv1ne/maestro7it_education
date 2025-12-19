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

# Глобальные
player_spam_count = 0
running = True
lock = threading.Lock()
victim = None

# Конфиг
RUNNERS = ["🎅 Дед Мороз (ты)", "🦌 Дэнсер", "🦌 Прансер", "🦌 Виксен", "🦌 Комета"]
SYMBOLS = ["🎅", "🦌", "🦌", "🦌", "🦌"]
TRACK_LENGTH = 50
DIFFICULTY = 2

def beep(frequency=900, duration=150):
    print('\a', end='', flush=True)
    if os.name == 'nt':
        try:
            import winsound
            winsound.Beep(frequency, duration)
        except:
            pass

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def color_text(text, color="WHITE"):
    if not COLORS:
        return text
    colors = {
        "RED": Fore.RED, "GREEN": Fore.GREEN, "YELLOW": Fore.YELLOW,
        "CYAN": Fore.CYAN, "MAGENTA": Fore.MAGENTA, "BLUE": Fore.BLUE,
        "WHITE": Style.RESET_ALL
    }
    return colors.get(color, "") + text + Style.RESET_ALL

def countdown():
    clear_screen()
    print(color_text("\n\n     🎄 Приготовьтесь к старту 🎄\n", "GREEN"))
    print(color_text("          Положи пальцы на Enter...\n\n", "YELLOW"))
    
    for i in range(5, 0, -1):
        clear_screen()
        print(color_text("\n\n     🎄 Приготовьтесь к старту 🎄\n", "GREEN"))
        print(color_text(f"               {i}  ", "RED" if i <= 3 else "YELLOW"))
        beep(600 + i*100, 300)
        time.sleep(1)
    
    clear_screen()
    print(color_text("\n\n               ПОЕХАЛИ!!!\n", "RED"))
    beep(1200, 500)
    time.sleep(0.8)

def draw_track(positions, events=None, elapsed="0.0"):
    clear_screen()
    print(color_text("""
   ___              _          ___           _     
  / __|__ _ _ _  __| |_ __ _  |   \\  __ _ ___| |__
  \\__ \\ _` | ' \\/ _` | ' \\ || | |) / _` / _ \\ '_ \\
  |___/__,_|_||_\\__,_|_|_|_| |___/\\__,_\\___/_.__/

          🎅🦌 🏁 SANTA DASH 2025 🏁 🦌🎅
""", "RED"))
    print(color_text(f"                Время: {elapsed}s\n", "BLUE"))

    for i, name in enumerate(RUNNERS):
        pos = min(positions[i], TRACK_LENGTH)
        # Пробел в начале трассы — бегуны появляются только после старта
        runner = SYMBOLS[i] if pos > 0 else " "
        track = " " * pos + runner + "—" * (TRACK_LENGTH - pos) + "🎄"
        progress = f"{pos}/{TRACK_LENGTH}"
        name_col = color_text(f"{name:24}", "CYAN" if i == 0 else "WHITE")
        print(f"{name_col} |{track}| {color_text(progress, 'YELLOW')}")

    if events:
        print(color_text("\n🎲 Случайное событие:", "MAGENTA"))
        for e in events:
            print(f"   → {e}")

    bonus = player_spam_count // 3
    print(color_text(f"\n🔥 Спам Enter ... Бонус к ходу: +{bonus}  (нажато: {player_spam_count})", "GREEN"))

def random_event():
    global victim
    et = random.choice(["none", "snow", "gift", "wolf", "aurora"])
    if et == "snow":
        return ["❄️ Метель! Все -1..3 шага"], lambda p: [max(0, x - random.randint(1,3)) for x in p]
    elif et == "gift":
        return ["🎁 Подарок от Снегурочки ... Ты +5 шагов"], "gift"
    elif et == "wolf":
        victim = random.randint(1, len(RUNNERS)-1)
        return [f"🐺 Волк! {RUNNERS[victim]} теряет 5 шагов"], "wolf"
    elif et == "aurora":
        return ["🌟 Северное сияние ... ИИ ускоряются (+3)"], "aurora"
    return ["Всё спокойно..."], None

def spam_thread():
    global player_spam_count, running
    while running:
        if sys.platform == "win32":
            import msvcrt
            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key in (b'\r', b'\n'):
                    with lock:
                        player_spam_count += 1
        else:
            import select
            if select.select([sys.stdin], [], [], 0.01) == ([sys.stdin], [], []):
                key = sys.stdin.read(1)
                if key in ('\r', '\n'):
                    with lock:
                        player_spam_count += 1
        time.sleep(0.008)  # Оптимально: быстро реагирует, не жрёт CPU

def race():
    global player_spam_count, running, DIFFICULTY, victim
    DIFFICULTY = 2
    positions = [0] * len(RUNNERS)

    clear_screen()
    print(color_text("🎄 SANTA DASH — Новогодняя гонка оленей 🎄\n", "GREEN"))
    print("Сложность:\n1 — Легко\n2 — Нормально\n3 — Хардкор")
    try:
        ch = input(color_text("\nВыбор [1-3, Enter = 2]: ", "YELLOW")).strip()
        DIFFICULTY = int(ch) if ch in '123' else 2
    except:
        DIFFICULTY = 2

    countdown()  # 5 секунд + отсчёт

    player_spam_count = 0
    running = True
    threading.Thread(target=spam_thread, daemon=True).start()

    start_time = time.time()
    turn = 0

    while max(positions) < TRACK_LENGTH:
        elapsed = f"{time.time() - start_time:.1f}"
        draw_track(positions, [], elapsed)
        time.sleep(0.1)

        with lock:
            bonus = player_spam_count // 3
            player_move = random.randint(2, 4) + bonus
            positions[0] = min(positions[0] + player_move, TRACK_LENGTH)
            player_spam_count %= 3

        for i in range(1, len(RUNNERS)):
            ai_move = random.randint(2, 4 + DIFFICULTY)
            positions[i] = min(positions[i] + ai_move, TRACK_LENGTH)

        turn += 1
        if random.random() < 0.22:  # ~каждые 4-5 ходов
            events, effect = random_event()
            draw_track(positions, events, f"{time.time() - start_time:.1f}")
            time.sleep(1.5)
            if effect == "gift":
                positions[0] = min(positions[0] + 5, TRACK_LENGTH)
            elif effect == "wolf" and victim is not None:
                positions[victim] = max(0, positions[victim] - 5)
            elif effect == "aurora":
                for i in range(1, len(RUNNERS)): positions[i] = min(positions[i] + 3, TRACK_LENGTH)
            elif callable(effect):
                positions = effect(positions)

    running = False
    final_time = time.time() - start_time
    beep(1200, 200); time.sleep(0.1); beep(1400, 300)

    draw_track(positions, [f"Гонка окончена за {final_time:.1f} секунд!"], f"{final_time:.1f}")

    winner = max(range(len(positions)), key=lambda i: positions[i])
    if winner == 0:
        print(color_text(f"\n🎉🎄 ТЫ ПОБЕДИЛ за {final_time:.1f} секунд 🎄🎉", "GREEN"))
        print(color_text("   Король спама и повелитель оленей 🏆✨", "YELLOW"))
    else:
        print(color_text(f"\n🏆 Победил: {RUNNERS[winner]}", "RED"))
        print(color_text(f"   Твоё время: {final_time:.1f}с — тренируйся", "YELLOW"))

    print(color_text("\nСыграть ещё? (да / любой ключ — выход): ", "CYAN"), end='')
    try:
        if input().strip().lower().startswith('д'):
            race()
    except:
        pass

if __name__ == "__main__":
    race()