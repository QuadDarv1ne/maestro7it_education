import time
import sys
try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    HAS_COLORAMA = True
except ImportError:
    HAS_COLORAMA = False

class Car:
    def __init__(self, model="Tesla Model S"):
        self.model = model
        self.doors_locked = True
        self.fuel_cap_open = False
        self.fuel_level = 0
        self.engine_on = False
        self.speed = 0
        self.headlights_on = False
        self.odometer = 0
        self.fuel_consumption = 0.08  # литров на км

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

    def show_progress(self, action, duration, emoji="", final_value=""):
        """Отображение анимированного прогресс-бара"""
        total_ticks = 20
        symbols = ['◐', '◓', '◑', '◒']
        
        color = Fore.GREEN if HAS_COLORAMA else ""
        sys.stdout.write("\n")
        
        for i in range(total_ticks):
            progress = int((i + 1) / total_ticks * 100)
            bar = '[' + '■' * (i + 1) + ' ' * (total_ticks - i - 1) + ']'
            spinner = symbols[i % len(symbols)]
            
            status_line = f"{color}{spinner} {emoji}{action} {bar} {progress}%"
            if final_value:
                status_line += f" | {final_value}"
            
            sys.stdout.write("\r" + status_line)
            sys.stdout.flush()
            time.sleep(duration / total_ticks)
        
        if HAS_COLORAMA:
            print(Fore.GREEN + f"\n✓ {action} завершено!")
        else:
            print(f"\n✓ {action} завершено!")

    def unlock_doors(self):
        """Разблокировка дверей"""
        if not self.doors_locked:
            return "Двери уже разблокированы"
        
        self.show_progress("Разблокировка дверей", 2, "🔓")
        self.doors_locked = False
        return "Двери разблокированы"

    def open_fuel_cap(self):
        """Открытие крышки бензобака"""
        if self.fuel_cap_open:
            return "Крышка бензобака уже открыта"
        
        if self.engine_on:
            return "Нельзя открывать бензобак при работающем двигателе"
        
        self.show_progress("Открытие крышки бензобака", 1, "⛽")
        self.fuel_cap_open = True
        return "Крышка бензобака открыта"

    def refuel(self, amount):
        """Заправка автомобиля"""
        if not self.fuel_cap_open:
            return "Сначала откройте крышку бензобака"
        
        self.show_progress(f"Заправка {amount} литров", 5, "⛽", f"Топливо: {self.fuel_level} → {self.fuel_level + amount}L")
        self.fuel_level += amount
        return f"Заправлено {amount} литров. Топливо: {self.fuel_level}L"

    def close_fuel_cap(self):
        """Закрытие крышки бензобака"""
        if not self.fuel_cap_open:
            return "Крышка бензобака уже закрыта"
        
        self.show_progress("Закрытие крышки бензобака", 1, "⛽")
        self.fuel_cap_open = False
        return "Крышка бензобака закрыта"

    def start_engine(self):
        """Запуск двигателя"""
        if self.engine_on:
            return "Двигатель уже работает"
        
        if self.fuel_level <= 0:
            return "Невозможно запустить двигатель: нет топлива"
        
        self.show_progress("Запуск двигателя", 3, "🚗", "V8: 🔊🔊🔊")
        self.engine_on = True
        return "Двигатель запущен"

    def accelerate(self, target_speed):
        """Набор скорости"""
        if not self.engine_on:
            return "Сначала запустите двигатель"
        
        speed_emoji = "🏁" if target_speed > 100 else "🚗"
        
        # Анимация разгона
        steps = 10
        step_size = (target_speed - self.speed) / steps
        
        print()
        for i in range(steps):
            self.speed += step_size
            speed_bar = '|' + '■' * int(self.speed / 5) + ' ' * (20 - int(self.speed / 5)) + '|'
            
            if HAS_COLORAMA:
                color = Fore.GREEN if self.speed < 60 else Fore.YELLOW if self.speed < 100 else Fore.RED
                sys.stdout.write(f"\r{color}{speed_emoji} Разгон: {speed_bar} {int(self.speed)} км/ч")
            else:
                sys.stdout.write(f"\r{speed_emoji} Разгон: {speed_bar} {int(self.speed)} км/ч")
            
            sys.stdout.flush()
            time.sleep(0.3)
        
        self.speed = target_speed
        print("\n✓ Достигнута скорость:", target_speed, "км/ч")
        return f"Едем на скорости {target_speed} км/ч"

    def drive(self, distance):
        """Движение автомобиля"""
        if not self.engine_on:
            return "Сначала запустите двигатель"
        
        if self.speed == 0:
            return "Сначала наберите скорость"
        
        time_needed = distance / self.speed * 3.6  # время в секундах
        fuel_needed = distance * self.fuel_consumption
        
        if fuel_needed > self.fuel_level:
            return "Недостаточно топлива для поездки"
        
        self.print_header(f"Поездка на {distance} км")
        
        # Анимация движения
        distance_covered = 0
        step = distance / 20
        
        for i in range(20):
            distance_covered += step
            self.fuel_level -= fuel_needed / 20
            self.odometer += step
            
            road = '—' * 20
            car_pos = int((distance_covered / distance) * 20)
            road_with_car = road[:car_pos] + '🚗' + road[car_pos+1:]
            
            if HAS_COLORAMA:
                print(Fore.CYAN + f"\rПройдено: {int(distance_covered)}/{distance} км | " +
                      Fore.YELLOW + f"Топливо: {self.fuel_level:.1f}L | " +
                      Fore.GREEN + f"Спидометр: {int(self.odometer)} км")
                print(Fore.BLUE + road_with_car)
            else:
                print(f"\rПройдено: {int(distance_covered)}/{distance} км | " +
                      f"Топливо: {self.fuel_level:.1f}L | " +
                      f"Спидометр: {int(self.odometer)} км")
                print(road_with_car)
            
            time.sleep(time_needed / 20)
        
        return f"Поездка завершена! Пройдено {distance} км"

    def brake(self):
        """Торможение"""
        if self.speed == 0:
            return "Автомобиль уже остановлен"
        
        print()
        while self.speed > 0:
            self.speed = max(0, self.speed - 20)
            speed_bar = '|' + '■' * int(self.speed / 5) + ' ' * (20 - int(self.speed / 5)) + '|'
            
            if HAS_COLORAMA:
                color = Fore.RED if self.speed > 50 else Fore.YELLOW if self.speed > 20 else Fore.GREEN
                sys.stdout.write(f"\r{color}🛑 Торможение: {speed_bar} {int(self.speed)} км/ч")
            else:
                sys.stdout.write(f"\r🛑 Торможение: {speed_bar} {int(self.speed)} км/ч")
            
            sys.stdout.flush()
            time.sleep(0.3)
        
        print("\n✓ Автомобиль полностью остановился")
        return "Торможение завершено"

    def stop_engine(self):
        """Остановка двигателя"""
        if not self.engine_on:
            return "Двигатель уже выключен"
        
        if self.speed > 0:
            return "Сначала остановите автомобиль"
        
        self.show_progress("Остановка двигателя", 2, "🔇", "Двигатель: OFF")
        self.engine_on = False
        return "Двигатель выключен"

    def lock_doors(self):
        """Блокировка дверей"""
        if self.doors_locked:
            return "Двери уже заблокированы"
        
        self.show_progress("Блокировка дверей", 1.5, "🔒")
        self.doors_locked = True
        return "Двери заблокированы"

    def status(self):
        """Отображение состояния автомобиля"""
        status = f"\nСостояние {self.model}:\n"
        status += f"🔒 Двери: {'Заблокированы' if self.doors_locked else 'Разблокированы'}\n"
        status += f"⛽ Крышка бензобака: {'Открыта' if self.fuel_cap_open else 'Закрыта'}\n"
        status += f"🛢️ Топливо: {self.fuel_level:.1f}L\n"
        status += f"🚗 Двигатель: {'Работает 🔊' if self.engine_on else 'Выключен 🔇'}\n"
        status += f"📏 Скорость: {self.speed} км/ч\n"
        status += f"📊 Спидометр: {self.odometer} км\n"
        status += f"💡 Фары: {'Включены' if self.headlights_on else 'Выключены'}"
        
        if HAS_COLORAMA:
            return (Fore.CYAN + "="*60 + "\n" + 
                    Fore.YELLOW + status + 
                    Fore.CYAN + "\n" + "="*60)
        return "="*60 + "\n" + status + "\n" + "="*60

# Демонстрация работы
if __name__ == "__main__":
    # Инициализация
    print("\n" + "="*60)
    print("АВТОМОБИЛЬНАЯ СИМУЛЯЦИЯ С ПРОДВИНУТОЙ ИНДИКАЦИЕЙ".center(60))
    print("="*60)
    
    if not HAS_COLORAMA:
        print("\nДля цветной индикации установите colorama: pip install colorama")
    
    car = Car("Tesla Model S")
    
    # Последовательность действий
    print(car.status())
    car.unlock_doors()
    car.open_fuel_cap()
    car.refuel(50)
    car.close_fuel_cap()
    car.start_engine()
    car.accelerate(80)
    car.drive(20)
    car.brake()
    car.stop_engine()
    car.lock_doors()
    
    print(car.status())
