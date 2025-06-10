import time
import sys
try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    HAS_COLORAMA = True
except ImportError:
    HAS_COLORAMA = False

class WashingMachine:
    def __init__(self):
        self.water_level = 0
        self.temperature = 0
        self.cycle_steps = [
            "Наполнение водой",
            "Нагрев воды",
            "Стирка",
            "Слив воды",
            "Полоскание",
            "Отжим",
            "Завершено"
        ]
        self.current_step = None
        self.delicate_mode = False
        self.step_durations = {
            "Наполнение водой": 5,
            "Нагрев воды": 10,
            "Стирка": 15,
            "Слив воды": 3,
            "Полоскание": 10,
            "Отжим": 8,
            "Завершено": 0
        }

    def print_header(self, text):
        """Печать заголовка с оформлением"""
        if HAS_COLORAMA:
            print(Fore.CYAN + "\n" + "="*60)
            print(Fore.YELLOW + f" {text.upper()} ".center(60, '★'))
            print(Fore.CYAN + "="*60 + Style.RESET_ALL)
        else:
            print("\n" + "="*60)
            print(f" {text.upper()} ".center(60, '*'))
            print("="*60)

    def show_progress(self, step_name, duration):
        """Отображение анимированного прогресс-бара"""
        total_ticks = 20
        symbols = ['◐', '◓', '◑', '◒']
        
        if HAS_COLORAMA:
            colors = {
                "Наполнение водой": Fore.BLUE,
                "Нагрев воды": Fore.RED,
                "Стирка": Fore.GREEN,
                "Слив воды": Fore.YELLOW,
                "Полоскание": Fore.CYAN,
                "Отжим": Fore.MAGENTA,
                "Завершено": Fore.WHITE
            }
            color = colors.get(step_name, Fore.WHITE)
        else:
            color = ""
        
        sys.stdout.write("\n")
        for i in range(total_ticks):
            progress = int((i + 1) / total_ticks * 100)
            bar = '[' + '■' * (i + 1) + ' ' * (total_ticks - i - 1) + ']'
            spinner = symbols[i % len(symbols)]
            
            sys.stdout.write(
                f"\r{color}{spinner} {step_name} {bar} {progress}% "
                f"(Вода: {self.water_level}% Темп: {self.temperature}°C)"
            )
            sys.stdout.flush()
            time.sleep(duration / total_ticks)
        
        if HAS_COLORAMA:
            print(Fore.GREEN + f"\n✓ {step_name} завершен!")
        else:
            print(f"\n✓ {step_name} завершен!")

    def run_cycle(self):
        """Запуск полного цикла стирки с индикацией"""
        self.print_header("Запуск цикла стирки")
        
        for step in self.cycle_steps:
            self.current_step = step
            duration = self.step_durations[step]
            
            # Пропустить этап нагрева, если воды недостаточно
            if step == "Нагрев воды" and self.water_level < 50:
                if HAS_COLORAMA:
                    print(Fore.RED + f"\n! Пропуск нагрева: недостаточно воды ({self.water_level}%)")
                else:
                    print(f"\n! Пропуск нагрева: недостаточно воды ({self.water_level}%)")
                continue
            
            # Пропустить отжим в деликатном режиме
            if step == "Отжим" and self.delicate_mode:
                if HAS_COLORAMA:
                    print(Fore.MAGENTA + "\n! Пропуск отжима: деликатный режим")
                else:
                    print("\n! Пропуск отжима: деликатный режим")
                continue
            
            # Выполняем логику для каждого этапа
            self.execute_step(step, duration)
        
        if HAS_COLORAMA:
            print(Fore.GREEN + "\n" + "="*60)
            print(Fore.GREEN + "★ ЦИКЛ СТИРКИ УСПЕШНО ЗАВЕРШЕН! ★".center(60))
            print(Fore.GREEN + "="*60 + Style.RESET_ALL)
        else:
            print("\n" + "="*60)
            print("★ ЦИКЛ СТИРКИ УСПЕШНО ЗАВЕРШЕН! ★".center(60))
            print("="*60)

    def execute_step(self, step, duration):
        """Выполнение конкретного этапа стирки"""
        if step == "Наполнение водой":
            self.water_level = 70
            self.show_progress(step, duration)
        
        elif step == "Нагрев воды":
            self.temperature = 40
            self.show_progress(step, duration)
        
        elif step == "Стирка":
            # Анимация "вращения" белья
            if HAS_COLORAMA:
                print(Fore.GREEN + "🌀 Белье вращается в барабане...")
            else:
                print("🌀 Белье вращается в барабане...")
            self.show_progress(step, duration)
        
        elif step == "Слив воды":
            self.water_level = 0
            self.show_progress(step, duration)
        
        elif step == "Полоскание":
            self.water_level = 60
            self.show_progress(step, duration)
        
        elif step == "Отжим":
            # Анимация быстрого вращения
            if HAS_COLORAMA:
                print(Fore.MAGENTA + "💨 Интенсивное вращение для отжима...")
            else:
                print("💨 Интенсивное вращение для отжима...")
            self.show_progress(step, duration)
        
        elif step == "Завершено":
            # Специальная анимация завершения
            if HAS_COLORAMA:
                print(Fore.GREEN + "🔔 Готово! Можно доставать белье")
                print(Fore.YELLOW + "✨ Белье чистое и свежее!")
            else:
                print("🔔 Готово! Можно доставать белье")
                print("✨ Белье чистое и свежее!")
            time.sleep(1)

# Демонстрация работы
if __name__ == "__main__":
    print("\n" + "="*60)
    print("СТИРАЛЬНАЯ МАШИНА С ПРОДВИНУТОЙ ИНДИКАЦИЕЙ".center(60))
    print("="*60)
    
    if not HAS_COLORAMA:
        print("\nДля цветной индикации установите colorama: pip install colorama")
    
    machine = WashingMachine()
    
    # Тест 1: Обычная стирка
    machine.delicate_mode = False
    machine.run_cycle()
    
    # Тест 2: Деликатный режим
    machine.delicate_mode = True
    machine.run_cycle()
    
    # Тест 3: Недостаток воды
    machine.water_level = 30
    machine.run_cycle()
