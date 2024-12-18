# Объектно-Ориентированное Программирование (ООП) в Python

**Объектно-Ориентированное Программирование (ООП)** — это парадигма программирования, основанная на представлении данных в виде объектов.

В Python ООП играет важную роль, позволяя создавать удобные и структурированные программы.

### 1. Основы ООП

**ООП основано на следующих ключевых концепциях:**
- `Класс` — это шаблон (или чертёж) для создания объектов.
- `Объект` — это экземпляр класса, который содержит данные (атрибуты) и методы (функции, связанные с объектом).
- `Инкапсуляция` — механизм, который объединяет данные и методы, защищая их от внешнего вмешательства.
- `Наследование` — процесс создания нового класса на основе существующего.
- `Полиморфизм` — способность объекта использовать методы, общие для всех классов в его иерархии.

### 2. Классы и объекты

В Python классы определяются с помощью ключевого слова `class`

После определения класса можно создавать его объекты.

**Пример создания класса и объекта:**
```python
class Car:
    """
    Класс, представляющий обычный автомобиль.

    Атрибуты:
        brand (str): Марка автомобиля.
        model (str): Модель автомобиля.
        year (int): Год выпуска автомобиля.
    """

    def __init__(self, brand, model, year):
        """
        Инициализация объекта класса Car.

        Аргументы:
            brand (str): Марка автомобиля.
            model (str): Модель автомобиля.
            year (int): Год выпуска автомобиля.
        """
        self.brand = brand
        self.model = model
        self.year = year

    def drive(self):
        """Выводит сообщение о движении автомобиля."""
        print(f"{self.brand} {self.model} едет.")


class Vehicle:
    """
    Класс, представляющий транспортное средство.

    Атрибуты:
        brand (str): Марка транспортного средства.
        model (str): Модель транспортного средства.
    """

    def __init__(self, brand, model):
        """
        Инициализация объекта класса Vehicle.

        Аргументы:
            brand (str): Марка транспортного средства.
            model (str): Модель транспортного средства.
        """
        self.brand = brand
        self.model = model

    def drive(self):
        """Выводит сообщение о движении транспортного средства."""
        print(f"{self.brand} {self.model} едет.")


class ElectricCar(Vehicle):
    """
    Класс, представляющий электрический автомобиль (наследует Vehicle).

    Атрибуты:
        brand (str): Марка автомобиля.
        model (str): Модель автомобиля.
        battery_capacity (int): Ёмкость батареи в кВт/ч.
    """

    def __init__(self, brand, model, battery_capacity):
        """
        Инициализация объекта класса ElectricCar.

        Аргументы:
            brand (str): Марка автомобиля.
            model (str): Модель автомобиля.
            battery_capacity (int): Ёмкость батареи в кВт/ч.
        """
        super().__init__(brand, model)
        self.battery_capacity = battery_capacity

    def charge(self):
        """Выводит сообщение о начале зарядки автомобиля."""
        print(f"{self.brand} {self.model} заряжается на {self.battery_capacity} кВт/ч.")

    def calculate_charge_time(self, charge_percentage, charge_rate):
        """
        Рассчитывает время зарядки автомобиля до указанного процента.

        Аргументы:
            charge_percentage (int): Процент зарядки (от 0 до 100).
            charge_rate (int): Скорость зарядки в кВт/ч.

        Возвращает:
            float: Время зарядки в часах.
        """
        if charge_rate <= 0:
            raise ValueError("Скорость зарядки должна быть больше нуля.")

        energy_needed = (self.battery_capacity * charge_percentage) / 100
        charge_time = energy_needed / charge_rate
        return charge_time


# Создание объекта класса ElectricCar
my_electric_car = ElectricCar("Tesla", "Model S", 100)

# Демонстрация функциональности
my_electric_car.drive()  # Tesla Model S едет
my_electric_car.charge()  # Tesla Model S заряжается на 100 кВт/ч

# Расчёт времени зарядки
charge_percentage = 50  # Процент зарядки
charge_rate = 22  # Скорость зарядки в кВт/ч

charge_time = my_electric_car.calculate_charge_time(charge_percentage, charge_rate)
print(f"Для зарядки {charge_percentage}% батареи потребуется {charge_time:.2f} часов при скорости {charge_rate} кВт/ч.")
```

- **Атрибуты** — это данные, связанные с объектом. Они задаются в конструкторе `__init__()`

- **Методы** — это функции, связанные с объектом класса. Внутри методов первый параметр всегда должен быть `self`, чтобы иметь доступ к атрибутам объекта.

### 3. Наследование

Наследование позволяет одному классу наследовать свойства и методы другого класса.

Класс, от которого наследуются, называется родительским (или базовым), а класс, который наследует, называется дочерним.

**Пример наследования:**
```python
class Vehicle:
    """
    Класс, представляющий транспортное средство.

    Атрибуты:
        brand (str): Марка транспортного средства.
        model (str): Модель транспортного средства.
    """

    def __init__(self, brand, model):
        """
        Инициализация объекта класса Vehicle.

        Аргументы:
            brand (str): Марка транспортного средства.
            model (str): Модель транспортного средства.
        """
        self.brand = brand
        self.model = model

    def drive(self):
        """Выводит сообщение о движении транспортного средства."""
        print(f"{self.brand} {self.model} едет.")

    def stop(self):
        """Выводит сообщение об остановке транспортного средства."""
        print(f"{self.brand} {self.model} остановился.")


class ElectricCar(Vehicle):
    """
    Класс, представляющий электрический автомобиль (наследует Vehicle).

    Атрибуты:
        brand (str): Марка автомобиля.
        model (str): Модель автомобиля.
        battery_capacity (int): Ёмкость батареи в кВт/ч.
    """

    def __init__(self, brand, model, battery_capacity):
        """
        Инициализация объекта класса ElectricCar.

        Аргументы:
            brand (str): Марка автомобиля.
            model (str): Модель автомобиля.
            battery_capacity (int): Ёмкость батареи в кВт/ч.
        """
        super().__init__(brand, model)
        self.battery_capacity = battery_capacity
        self.current_charge = 0  # Текущий заряд батареи в %

    def charge(self, percentage):
        """
        Заряжает батарею на заданный процент.

        Аргументы:
            percentage (int): Процент зарядки.
        """
        if self.current_charge + percentage > 100:
            self.current_charge = 100
        else:
            self.current_charge += percentage
        print(f"{self.brand} {self.model} заряжен на {self.current_charge}%.")

    def range(self):
        """Выводит предполагаемый запас хода на текущем заряде."""
        estimated_range = self.battery_capacity * (self.current_charge / 100) * 5  # 5 км на 1 кВт/ч
        print(f"{self.brand} {self.model} может проехать примерно {estimated_range:.2f} км на текущем заряде.")


class HybridCar(Vehicle):
    """
    Класс, представляющий гибридный автомобиль (наследует Vehicle).

    Атрибуты:
        brand (str): Марка автомобиля.
        model (str): Модель автомобиля.
        fuel_capacity (int): Ёмкость топливного бака в литрах.
        battery_capacity (int): Ёмкость батареи в кВт/ч.
    """

    def __init__(self, brand, model, fuel_capacity, battery_capacity):
        """
        Инициализация объекта класса HybridCar.

        Аргументы:
            brand (str): Марка автомобиля.
            model (str): Модель автомобиля.
            fuel_capacity (int): Ёмкость топливного бака в литрах.
            battery_capacity (int): Ёмкость батареи в кВт/ч.
        """
        super().__init__(brand, model)
        self.fuel_capacity = fuel_capacity
        self.battery_capacity = battery_capacity
        self.current_fuel = 0  # Текущий уровень топлива в литрах
        self.current_charge = 0  # Текущий заряд батареи в %

    def refuel(self, liters):
        """
        Заправляет автомобиль на заданное количество литров.

        Аргументы:
            liters (int): Количество литров для заправки.
        """
        if self.current_fuel + liters > self.fuel_capacity:
            self.current_fuel = self.fuel_capacity
        else:
            self.current_fuel += liters
        print(f"{self.brand} {self.model} заправлен на {self.current_fuel} литров.")

    def charge(self, percentage):
        """
        Заряжает батарею на заданный процент.

        Аргументы:
            percentage (int): Процент зарядки.
        """
        if self.current_charge + percentage > 100:
            self.current_charge = 100
        else:
            self.current_charge += percentage
        print(f"{self.brand} {self.model} заряжен на {self.current_charge}%.")

    def range(self):
        """Выводит предполагаемый запас хода на текущем заряде и уровне топлива."""
        electric_range = self.battery_capacity * (self.current_charge / 100) * 5  # 5 км на 1 кВт/ч
        fuel_range = self.current_fuel * 15  # 15 км на 1 литр топлива
        total_range = electric_range + fuel_range
        print(f"{self.brand} {self.model} может проехать примерно {total_range:.2f} км на текущем заряде и топливе.")


# Тестирование классов
if __name__ == "__main__":
    # Электромобиль
    my_electric_car = ElectricCar("Tesla", "Model S", 100)
    my_electric_car.drive()
    my_electric_car.charge(50)
    my_electric_car.range()

    print("\n")

    # Гибридный автомобиль
    my_hybrid_car = HybridCar("Toyota", "Prius", 40, 20)
    my_hybrid_car.drive()
    my_hybrid_car.refuel(20)
    my_hybrid_car.charge(80)
    my_hybrid_car.range()
```

В этом примере класс `ElectricCar` наследует от класса `Vehicle`, что позволяет использовать методы и атрибуты родительского класса.

Метод `super()` используется для вызова конструктора родительского класса.

### 4. Полиморфизм

Полиморфизм позволяет использовать методы, общие для всех классов в иерархии, даже если конкретная реализация метода различна.

**Пример полиморфизма:**
```python
class Animal:
    """
    Базовый класс для всех животных.
    
    Методы:
        sound(): Возвращает звук, издаваемый животным (определяется в подклассах).
    """

    def sound(self):
        raise NotImplementedError("Этот метод должен быть реализован в подклассах")


class Dog(Animal):
    """
    Класс, представляющий собаку (наследует Animal).
    """

    def sound(self):
        return "Гав"


class Cat(Animal):
    """
    Класс, представляющий кошку (наследует Animal).
    """

    def sound(self):
        return "Мяу"


class Cow(Animal):
    """
    Класс, представляющий корову (наследует Animal).
    """

    def sound(self):
        return "Муу"


class Bird(Animal):
    """
    Класс, представляющий птицу (наследует Animal).
    """

    def sound(self):
        return "Чирик"


# Используем полиморфизм

def make_sound(animal):
    """
    Вызывает метод sound() у переданного объекта animal.

    Аргументы:
        animal (Animal): Объект класса Animal или его подкласса.
    """
    print(f"{animal.__class__.__name__}: {animal.sound()}")


if __name__ == "__main__":
    # Создаем список животных
    animals = [Dog(), Cat(), Cow(), Bird()]

    # Вызываем звуки для каждого животного
    for animal in animals:
        make_sound(animal)
```

В этом примере метод `sound` реализован по-разному для каждого подкласса, но мы можем использовать их одинаково через общую функцию `make_sound`, что является примером полиморфизма.

### 5. Инкапсуляция

**Инкапсуляция** — это концепция сокрытия внутренней реализации объекта.

В Python атрибуты и методы могут быть защищены от внешнего доступа с помощью соглашения о наименовании.

**Пример инкапсуляции:**
```python
class Person:
    """
    Класс для представления человека с именем и возрастом.

    Атрибуты:
        name (str): Имя человека.
        age (int): Возраст человека. Доступен через геттер и сеттер с проверкой.

    Методы:
        __str__: Возвращает строковое представление объекта.
    """

    def __init__(self, name: str, age: int):
        """
        Инициализирует объект класса Person.

        Args:
            name (str): Имя человека.
            age (int): Возраст человека. Проверяется на корректность.
        """
        self.name = name
        self.__age = None
        self.age = age  # Установка через сеттер для проверки

    @property
    def age(self) -> int:
        """
        Возвращает возраст человека.

        Returns:
            int: Возраст человека.
        """
        return self.__age

    @age.setter
    def age(self, value: int):
        """
        Устанавливает возраст человека с проверкой на корректность.

        Args:
            value (int): Новый возраст человека.

        Raises:
            ValueError: Если возраст отрицательный.
        """
        if not isinstance(value, int):
            raise TypeError("Возраст должен быть целым числом.")
        if value < 0:
            raise ValueError("Возраст не может быть отрицательным.")
        self.__age = value

    def __str__(self) -> str:
        """
        Возвращает строковое представление объекта.

        Returns:
            str: Имя и возраст человека.
        """
        return f"Имя: {self.name}\nВозраст: {self.age}"


# Пример использования
if __name__ == "__main__":
    # Создание объекта
    person = Person("Алиса", 30)
    print(person)  # Имя: Алиса, Возраст: 30

    # Изменение возраста
    person.age = 35
    print("Новый возраст:", person.age,"\n")  # 35

    # Пример обработки исключения
    try:
        person.age = -5  # Ошибка: ValueError
    except ValueError as e:
        print(f"Ошибка: {e}")

    try:
        person.age = "двадцать"  # Ошибка: TypeError
    except TypeError as e:
        print(f"Ошибка: {e}")
```

В Python приватные атрибуты и методы обозначаются двумя подчёркиваниями в начале имени `(__)`.

Прямой доступ к ним извне невозможен, но можно создать специальные методы для получения или изменения этих данных.

### Выводы

ООП позволяет создавать более структурированные программы, в которых данные и методы объединены в классы.

Важные концепции ООП, такие как наследование, инкапсуляция и полиморфизм, помогают организовать код таким образом, чтобы он был легче читаемым, поддерживаемым и расширяемым.



**Автор:** Дуплей Максим Игоревич

**Дата:** 07.09.2024

**Версия 1.0**
