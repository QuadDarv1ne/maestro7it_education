import math
import re

def calculate_expression(expression, x_value=None):
    """
    Вычисляет математическое выражение с поддержкой функций
    
    Args:
        expression: строка с выражением (например, "sin(x) + cos(x)")
        x_value: значение переменной x (если есть)
    
    Returns:
        Результат вычисления
    """
    try:
        # Заменяем функции на их математические эквиваленты
        expression = expression.lower()
        
        # Если есть переменная x, заменяем её на значение
        if x_value is not None:
            expression = expression.replace('x', str(x_value))
        
        # Обрабатываем специальные функции
        # Синус, косинус, тангенс (работают с радианами)
        expression = re.sub(r'sin\(([^)]+)\)', r'math.sin(\1)', expression)
        expression = re.sub(r'cos\(([^)]+)\)', r'math.cos(\1)', expression)
        expression = re.sub(r'tan\(([^)]+)\)', r'math.tan(\1)', expression)
        
        # Синус, косинус, тангенс в градусах
        expression = re.sub(r'sind\(([^)]+)\)', r'math.sin(math.radians(\1))', expression)
        expression = re.sub(r'cosd\(([^)]+)\)', r'math.cos(math.radians(\1))', expression)
        expression = re.sub(r'tand\(([^)]+)\)', r'math.tan(math.radians(\1))', expression)
        
        # Экспонента и логарифмы
        expression = re.sub(r'exp\(([^)]+)\)', r'math.exp(\1)', expression)
        expression = re.sub(r'ln\(([^)]+)\)', r'math.log(\1)', expression)
        expression = re.sub(r'log10\(([^)]+)\)', r'math.log10(\1)', expression)
        expression = re.sub(r'log\(([^)]+)\)', r'math.log(\1)', expression)
        
        # Квадратный корень и модуль
        expression = re.sub(r'sqrt\(([^)]+)\)', r'math.sqrt(\1)', expression)
        expression = re.sub(r'abs\(([^)]+)\)', r'abs(\1)', expression)
        
        # Степень (обработка ^ как **)
        expression = expression.replace('^', '**')
        
        # Математические константы
        expression = expression.replace('pi', str(math.pi))
        expression = expression.replace('e', str(math.e))
        
        # Безопасное вычисление выражения
        # Создаем безопасное окружение для eval
        safe_dict = {
            'math': math,
            'abs': abs,
            'round': round,
            'int': int,
            'float': float
        }
        
        # Добавляем все функции из math в безопасный словарь
        for func in dir(math):
            if not func.startswith('_'):
                safe_dict[func] = getattr(math, func)
        
        result = eval(expression, {"__builtins__": {}}, safe_dict)
        return result
        
    except ZeroDivisionError:
        raise ValueError("Ошибка: деление на ноль")
    except ValueError as e:
        raise ValueError(f"Ошибка в вычислении: {e}")
    except Exception as e:
        raise ValueError(f"Ошибка в выражении: {e}")

def calculator_with_functions():
    """
    Калькулятор с поддержкой функций и переменных
    """
    print("=" * 50)
    print("КАЛЬКУЛЯТОР С ПОДДЕРЖКОЙ ФУНКЦИЙ")
    print("=" * 50)
    print("\nПоддерживаемые функции:")
    print("  Тригонометрия (радианы): sin(x), cos(x), tan(x)")
    print("  Тригонометрия (градусы): sind(x), cosd(x), tand(x)")
    print("  Экспонента/логарифмы: exp(x), ln(x), log10(x), log(x, base)")
    print("  Корни/степени: sqrt(x), x^y (x**y)")
    print("  Прочие: abs(x), round(x)")
    print("\nКонстанты: pi, e")
    print("Операции: +, -, *, /, ** (степень)")
    print("Примеры: sin(pi/2) + cos(0), sqrt(16) + log10(100)")
    print("         exp(1) * ln(e), sind(30) + cosd(60)")
    print("         sin(x) + cos(x) (при запросе введите значение x)")
    print("\nДля выхода введите 'exit'")
    print("=" * 50)
    
    while True:
        try:
            # Ввод выражения
            expression = input("\nВведите выражение: ").strip()
            
            if expression.lower() == 'exit':
                print("Выход из калькулятора.")
                break
            
            if not expression:
                continue
            
            # Проверяем, есть ли в выражении переменная x
            has_variable = 'x' in expression.lower()
            x_value = None
            
            if has_variable:
                # Запрашиваем значение x
                x_input = input("Введите значение x: ").strip()
                try:
                    x_value = float(x_input)
                except ValueError:
                    print("Ошибка: x должно быть числом")
                    continue
            
            # Вычисляем результат
            result = calculate_expression(expression, x_value)
            
            # Красивый вывод
            if has_variable and x_value is not None:
                print(f"\nРезультат: {expression} при x = {x_value} = {result}")
            else:
                print(f"\nРезультат: {expression} = {result}")
            
            # Округление до разумного количества знаков
            if isinstance(result, float):
                if abs(result) < 1e-10:
                    result = 0.0
                print(f"Округленно: {round(result, 10)}")
            
        except ValueError as e:
            print(f"Ошибка: {e}")
        except KeyboardInterrupt:
            print("\n\nВыход из калькулятора.")
            break
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")

def calculator_with_graph():
    """
    Расширенный калькулятор с возможностью построения графиков
    """
    try:
        import numpy as np
        import matplotlib.pyplot as plt
    except ImportError:
        print("Для построения графиков установите библиотеки:")
        print("pip install numpy matplotlib")
        return
    
    print("=" * 50)
    print("КАЛЬКУЛЯТОР С ПОСТРОЕНИЕМ ГРАФИКОВ")
    print("=" * 50)
    
    while True:
        print("\n1. Вычислить выражение")
        print("2. Построить график функции")
        print("3. Выйти")
        
        choice = input("\nВыберите действие (1-3): ").strip()
        
        if choice == '3':
            break
        elif choice == '1':
            expression = input("Введите выражение: ").strip()
            if 'x' in expression.lower():
                x_val = float(input("Введите значение x: "))
                result = calculate_expression(expression, x_val)
                print(f"Результат: {result}")
            else:
                result = calculate_expression(expression)
                print(f"Результат: {result}")
        elif choice == '2':
            func_expr = input("Введите функцию f(x): ").strip()
            x_min = float(input("Начало интервала x: "))
            x_max = float(input("Конец интервала x: "))
            
            # Создаем массив значений x
            x_values = np.linspace(x_min, x_max, 400)
            y_values = []
            
            # Вычисляем значения функции для каждого x
            for x_val in x_values:
                try:
                    y_val = calculate_expression(func_expr, x_val)
                    y_values.append(y_val)
                except:
                    y_values.append(np.nan)
            
            # Построение графика
            plt.figure(figsize=(10, 6))
            plt.plot(x_values, y_values, 'b-', linewidth=2, label=f"f(x) = {func_expr}")
            plt.xlabel('x')
            plt.ylabel('f(x)')
            plt.title(f'График функции f(x) = {func_expr}')
            plt.grid(True, alpha=0.3)
            plt.legend()
            plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
            plt.axvline(x=0, color='k', linestyle='-', alpha=0.3)
            
            # Добавляем точки пересечения с осями
            for x_val in np.linspace(x_min, x_max, 20):
                try:
                    y_val = calculate_expression(func_expr, x_val)
                    if abs(y_val) < 0.1:  # Приближенный ноль
                        plt.plot(x_val, y_val, 'ro', markersize=5)
                except:
                    pass
            
            plt.show()

def main():
    """
    Главное меню калькулятора
    """
    print("=" * 50)
    print("ВЫБЕРИТЕ РЕЖИМ КАЛЬКУЛЯТОРА")
    print("=" * 50)
    print("1. Базовый калькулятор с функциями")
    print("2. Калькулятор с построением графиков (нужен numpy и matplotlib)")
    print("3. Выйти")
    
    while True:
        choice = input("\nВыберите режим (1-3): ").strip()
        
        if choice == '1':
            calculator_with_functions()
        elif choice == '2':
            calculator_with_graph()
        elif choice == '3':
            print("До свидания!")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

# Примеры использования функций калькулятора
def examples():
    """
    Примеры использования калькулятора
    """
    print("\nПримеры вычислений:")
    examples = [
        ("sin(pi/2) + cos(0)", None),
        ("sqrt(16) + log10(100)", None),
        ("exp(1) * ln(e)", None),
        ("sind(30) + cosd(60)", None),
        ("sin(x) + cos(x)", math.pi/4),
        ("tan(pi/4)", None),
        ("2**3 + 3**2", None),
        ("abs(-5) + sqrt(9)", None),
    ]
    
    for expr, x_val in examples:
        try:
            result = calculate_expression(expr, x_val)
            if x_val is not None:
                print(f"{expr} при x = {x_val} = {result}")
            else:
                print(f"{expr} = {result}")
        except Exception as e:
            print(f"Ошибка в {expr}: {e}")

if __name__ == "__main__":
    # Показать примеры
    examples()
    
    # Запустить главное меню
    main()