'''
https://leetcode.com/problems/count-and-say/description/
Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Решение задачи "Count and Say"

Полезные ссылки:
1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
2. Telegram №1 @quadd4rv1n7
3. Telegram №2 @dupley_maxim_1999
4. Rutube канал: https://rutube.ru/channel/4218729/
5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
6. YouTube канал: https://www.youtube.com/@it-coders
7. ВК группа: https://vk.com/science_geeks
'''

class Solution:
    def countAndSay(self, n):
        """
        Генерирует n-й элемент последовательности "Count and Say".
        
        Последовательность:
        - countAndSay(1) = "1"
        - countAndSay(2) = "11" (одна единица)
        - countAndSay(3) = "21" (две единицы)
        - countAndSay(4) = "1211" (одна двойка, одна единица)
        - countAndSay(5) = "111221" (одна единица, одна двойка, две единицы)
        
        Args:
            n (int): Номер элемента последовательности
            
        Returns:
            str: n-й элемент последовательности
        """
        if n == 1:
            return "1"
        
        # Начинаем с базового случая
        result = "1"
        
        # Генерируем последовательность до n-го элемента
        for _ in range(n - 1):
            current = ""
            count = 1
            prev_char = result[0]
            
            # Обрабатываем каждый символ в текущей строке
            for i in range(1, len(result)):
                if result[i] == prev_char:
                    count += 1
                else:
                    current += str(count) + prev_char
                    count = 1
                    prev_char = result[i]
            
            # Добавляем последнюю группу символов
            current += str(count) + prev_char
            result = current
        
        return result