"""
euclid_gcd.py
Реализация алгоритма Евклида для вычисления НОД

Программа запрашивает два положительных целых числа,
вычисляет их НОД с помощью алгоритма Евклида и выводит результат.
Обрабатывает некорректный ввод и случай (0,0).
"""

def gcd(a: int, b: int) -> int | None:
    """
    Вычисляет НОД двух чисел по алгоритму Евклида
    
    Аргументы:
        a: первое число (неотрицательное)
        b: второе число (неотрицательное)
    
    Возвращает:
        int: НОД чисел, либо None для (0,0)
        
    Выбрасывает:
        ValueError: если числа отрицательные
    """
    if a < 0 or b < 0:
        raise ValueError("Числа должны быть неотрицательными")
    if a == 0 and b == 0:
        return None
    while b != 0:
        a, b = b, a % b
    return a

def main():
    """Основная функция обработки ввода и вывода"""
    while True:
        try:
            input_str = input("Введите два положительных целых числа: ")
            nums = input_str.split()
            if len(nums) != 2:
                raise ValueError("Требуется ровно два числа")
                
            num1, num2 = map(int, nums)
            if num1 < 0 or num2 < 0:
                raise ValueError("Числа должны быть положительными")
                
            break
        except ValueError as e:
            print(f"Ошибка: {e}. Повторите ввод.")
    
    result = gcd(num1, num2)
    if result is None:
        print("НОД(0, 0) не определён")
    else:
        print(f"НОД({num1}, {num2}) = {result}")

if __name__ == "__main__":
    main()
