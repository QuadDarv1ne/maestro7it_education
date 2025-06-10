class Car:
    def __init__(self, make: str, model: str):
        self.make = make
        self.model = model
        self.engine_on = False
        self.speed = 0
        self.lights_on = False

    # Реализованные методы
    def start_engine(self) -> str:
        if not self.engine_on:
            self.engine_on = True
            return "Двигатель запущен"
        return "Двигатель уже работает"

    def stop_engine(self) -> str:
        if self.engine_on:
            self.engine_on = False
            self.speed = 0
            return "Двигатель остановлен"
        return "Двигатель уже выключен"

    def accelerate(self, kmh: int) -> str:
        if self.engine_on:
            self.speed += kmh
            return f"Скорость увеличена до {self.speed} км/ч"
        return "Сначала запустите двигатель"

    # Методы с заглушками (pass)
    def activate_alarm(self, duration: int) -> None:
        """Активировать сигнализацию на указанное время"""
        # Заглушка для будущей реализации
        pass

    def enable_autopilot(self, mode: str) -> None:
        """Включить режим автопилота"""
        # Заглушка для будущей реализации
        pass

    def check_systems(self) -> None:
        """Провести самодиагностику систем"""
        # Заглушка для будущей реализации
        pass

    # Еще один реализованный метод
    def toggle_lights(self) -> str:
        self.lights_on = not self.lights_on
        status = "включены" if self.lights_on else "выключены"
        return f"Фары {status}"
