import math

def advanced_calculator():
    history = []
    
    def add_to_history(expression, result):
        history.append(f"{expression} = {result}")
    
    print("Продвинутый калькулятор")
    print("Доступные операции: +, -, *, /, ^, sqrt, sin, cos, tan, log, log10")
    
    while True:
        try:
            operation = input("\nОперация (или 'history'/'exit'): ").strip().lower()
            
            if operation == 'exit':
                break
            elif operation == 'history':
                print("\nИстория вычислений:")
                for item in history:
                    print(item)
                continue
            
            # Одноаргументные операции
            if operation in ('sqrt', 'sin', 'cos', 'tan', 'log', 'log10'):
                num = float(input("Введите число: "))
                
                if operation == 'sqrt':
                    if num < 0:
                        print("Ошибка: отрицательное число")
                        continue
                    result = math.sqrt(num)
                    expr = f"√{num}"
                elif operation == 'sin':
                    result = math.sin(math.radians(num))
                    expr = f"sin({num}°)"
                elif operation == 'cos':
                    result = math.cos(math.radians(num))
                    expr = f"cos({num}°)"
                elif operation == 'tan':
                    result = math.tan(math.radians(num))
                    expr = f"tan({num}°)"
                elif operation == 'log':
                    if num <= 0:
                        print("Ошибка: логарифм от неположительного числа")
                        continue
                    result = math.log(num)
                    expr = f"ln({num})"
                elif operation == 'log10':
                    if num <= 0:
                        print("Ошибка: логарифм от неположительного числа")
                        continue
                    result = math.log10(num)
                    expr = f"log10({num})"
                
                print(f"{expr} = {result}")
                add_to_history(expr, result)
                
            # Двухаргументные операции
            elif operation in ('+', '-', '*', '/', '^'):
                num1 = float(input("Первое число: "))
                num2 = float(input("Второе число: "))
                
                if operation == '+':
                    result = num1 + num2
                elif operation == '-':
                    result = num1 - num2
                elif operation == '*':
                    result = num1 * num2
                elif operation == '/':
                    if num2 == 0:
                        print("Ошибка: деление на ноль")
                        continue
                    result = num1 / num2
                elif operation == '^':
                    result = num1 ** num2
                
                expr = f"{num1} {operation} {num2}"
                print(f"{expr} = {result}")
                add_to_history(expr, result)
                
            else:
                print("Неизвестная операция")
                
        except ValueError:
            print("Ошибка ввода числа")
        except Exception as e:
            print(f"Ошибка: {e}")

# Запуск продвинутого калькулятора
if __name__ == "__main__":
    advanced_calculator()