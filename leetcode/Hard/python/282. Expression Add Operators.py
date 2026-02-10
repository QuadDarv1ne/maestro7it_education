"""
Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Полезные ссылки:
1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
2. Telegram №1 @quadd4rv1n7
3. Telegram №2 @dupley_maxim_1999
4. Rutube канал: https://rutube.ru/channel/4218729/
5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
6. YouTube канал: https://www.youtube.com/@it-coders
7. ВК группа: https://vk.com/science_geeks
"""

class Solution:
    def addOperators(self, num, target):
        """
        Генерирует все комбинации операторов +, -, *, которые дают target.
        
        Args:
            num: Строка цифр (например, "123")
            target: Целевое значение выражения
            
        Returns:
            Список строк с валидными выражениями
            
        Примеры:
            >>> addOperators("123", 6)
            ["1+2+3", "1*2*3"]
            >>> addOperators("232", 8)
            ["2*3+2", "2+3*2"]
            
        Сложность:
            Время: O(4^n) — на каждой позиции 4 варианта (+, -, *, пропуск)
            Память: O(n) для рекурсии
        """
        result = []
        
        def backtrack(index, path, current_val, prev_operand):
            if index == len(num):
                if current_val == target:
                    result.append(path)
                return
            
            for i in range(index, len(num)):
                # Пропускаем числа с ведущим нулем (кроме самого нуля)
                if i > index and num[index] == '0':
                    break
                
                current_str = num[index:i+1]
                current_num = int(current_str)
                
                if index == 0:
                    # Первое число, просто добавляем
                    backtrack(i + 1, current_str, current_num, current_num)
                else:
                    # Сложение (без f-строки)
                    backtrack(i + 1, path + "+" + current_str, 
                             current_val + current_num, current_num)
                    
                    # Вычитание (без f-строки)
                    backtrack(i + 1, path + "-" + current_str, 
                             current_val - current_num, -current_num)
                    
                    # Умножение: отменяем предыдущую операцию (без f-строки)
                    backtrack(i + 1, path + "*" + current_str, 
                             current_val - prev_operand + prev_operand * current_num, 
                             prev_operand * current_num)
        
        backtrack(0, "", 0, 0)
        return result