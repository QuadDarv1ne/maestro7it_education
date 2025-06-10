class WashingMachine:
    def __init__(self, brand: str, capacity: float):
        self.brand = brand
        self.capacity = capacity  # кг
        self.is_on = False
        self.is_washing = False
        self.current_program = None
        self.remaining_time = 0
        self.door_locked = False

    # Основные методы
    def power_on(self) -> str:
        if not self.is_on:
            self.is_on = True
            return "Стиральная машина включена"
        return "Машина уже включена"

    def power_off(self) -> str:
        if self.is_on:
            self.is_on = False
            self.is_washing = False
            self.door_locked = False
            return "Стиральная машина выключена"
        return "Машина уже выключена"

    def select_program(self, program: str) -> str:
        if not self.is_washing:
            self.current_program = program
            return f"Выбрана программа: {program}"
        return "Невозможно изменить программу во время стирки"

    def start_wash(self) -> str:
        if not self.is_on:
            return "Сначала включите машину"
        if not self.current_program:
            return "Выберите программу стирки"
        if self.is_washing:
            return "Стирка уже идет"
        
        self.is_washing = True
        self.door_locked = True
        self.remaining_time = self._calculate_time()
        return f"Старт программы {self.current_program}. Осталось: {self.remaining_time} мин"

    # Вспомогательный метод
    def _calculate_time(self) -> int:
        """Рассчет времени стирки для разных программ"""
        programs = {
            "Хлопок": 120,
            "Синтетика": 90,
            "Шерсть": 60,
            "Быстрая": 30
        }
        return programs.get(self.current_program, 45)

    # Методы с заглушками
    def set_delayed_start(self, hours: int) -> None:
        """Установить отложенный старт"""
        # Заглушка для будущей реализации
        pass

    def child_lock(self, enable: bool) -> None:
        """Блокировка от детей"""
        # Заглушка для будущей реализации
        pass

    def self_clean(self) -> None:
        """Самоочистка машины"""
        # Заглушка для будущей реализации
        pass

    # Дополнительные реализованные методы
    def pause_wash(self) -> str:
        if self.is_washing:
            self.is_washing = False
            return "Стирка приостановлена"
        return "Стирка не активна"

    def unlock_door(self) -> str:
        if not self.is_washing:
            self.door_locked = False
            return "Дверь разблокирована"
        return "Невозможно открыть дверь во время стирки"

    def check_status(self) -> str:
        status = f"Статус: {'Включена' if self.is_on else 'Выключена'}"
        if self.is_washing:
            status += f"\nИдет стирка ({self.current_program})"
            status += f"\nОсталось времени: {self.remaining_time} мин"
        return status
