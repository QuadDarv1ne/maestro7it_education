# Урок 3: Условные операторы и циклы

### Цели урока:

- Изучить условные конструкции в `Python`
- Понять работу циклов `for` и `while`
- Ознакомиться с управляющими операторами `break`, `continue`, и `pass`

### 1. Условные конструкции (if, elif, else)

Условные операторы позволяют программе выполнять определённые действия в зависимости от выполнения условий.

В Python для этого используются операторы `if`, `elif` и `else`

**Синтаксис:**
```python
if условие1:
    # код, если условие1 истинно
elif условие2:
    # код, если условие1 ложно, но условие2 истинно
else:
    # код, если все условия ложны
```
**Пример:**
```python
age = 18

if age < 18:
    print("Ты еще несовершеннолетний.")
elif age == 18:
    print("Ты только что стал взрослым!")
else:
    print("Ты уже взрослый.")
```

### 2. Циклы (for, while)

Циклы позволяют многократно выполнять одну и ту же последовательность инструкций.

**В Python есть два типа циклов:** `for` и `while`

**Цикл for**

Цикл `for` используется для итерации по коллекциям (например, спискам, строкам).

**Пример:**
```python
# Цикл по списку
numbers = [1, 2, 3, 4, 5]

for number in numbers:
    print(number)
```

**Цикл while**

Цикл `while` продолжает выполняться, пока условие истинно.

**Пример:**
```python
# Цикл, который продолжается, пока x меньше 5
x = 0

while x < 5:
    print(x)
    x += 1  # Увеличиваем x на 1
```

### 3. Управляющие операторы (break, continue, pass)

Управляющие операторы используются для изменения поведения циклов или условных конструкций.

**Оператор break**

Останавливает выполнение цикла:

```python
for i in range(10):
    if i == 5:
        break  # Прерывает цикл, когда i равно 5
    print(i)
```

**Оператор continue**

Пропускает текущую итерацию и продолжает цикл со следующей итерации:

```python
for i in range(5):
    if i == 2:
        continue  # Пропускает вывод числа 2
    print(i)
```

**Оператор pass** - ничего не делает.

Используется, когда нужно оставить тело цикла или условного оператора пустым:

```python
for i in range(5):
    if i == 2:
        pass  # Здесь ничего не происходит
    else:
        print(i)
```

**Вот пример кода класса `Car` с реализованными методами и заглушками (`pass`):**

```python
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
```

**Пример использования:**

```python
my_car = Car("Tesla", "Model S")

print(my_car.start_engine())      # Двигатель запущен
print(my_car.accelerate(50))      # Скорость увеличена до 50 км/ч
print(my_car.toggle_lights())     # Фары включены
print(my_car.stop_engine())       # Двигатель остановлен

# Вызов методов с заглушками (ничего не произойдет)
my_car.activate_alarm(10)
my_car.enable_autopilot("Eco")
my_car.check_systems()
```

**Вот пример кода класса `WashingMachine` с реализованными методами и заглушками:**

```python
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
```

**Пример использования:**

```python
my_wm = WashingMachine("Bosch", 7.5)

print(my_wm.power_on())               # Стиральная машина включена
print(my_wm.select_program("Хлопок")) # Выбрана программа: Хлопок
print(my_wm.start_wash())             # Старт программы Хлопок. Осталось: 120 мин
print(my_wm.check_status())           # Статус: Включена
                                      # Идет стирка (Хлопок)
                                      # Осталось времени: 120 мин

# Вызов методов с заглушками
my_wm.set_delayed_start(3)
my_wm.child_lock(True)
my_wm.self_clean()

print(my_wm.pause_wash())         # Стирка приостановлена
print(my_wm.unlock_door())        # Дверь разблокирована
print(my_wm.power_off())          # Стиральная машина выключена
```

### 4. Заключение

На этом уроке вы узнали, как использовать условные конструкции и циклы в `Python`

Теперь вы умеете писать программы, которые могут принимать решения и выполнять повторяющиеся задачи.

В следующем уроке мы рассмотрим функции и их использование.

---

**Автор:** Дуплей Максим Игоревич

**Дата:** 07.09.2024

**Версия 1.0**
