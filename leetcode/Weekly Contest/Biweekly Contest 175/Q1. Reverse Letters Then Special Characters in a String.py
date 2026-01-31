class Solution:
    def reverseByType(self, s):
        # Шаг 1: Извлекаем буквы и их позиции
        letters = []
        letter_positions = []
        
        for i, char in enumerate(s):
            if char.isalpha():
                letters.append(char)
                letter_positions.append(i)
        
        # Шаг 2: Извлекаем специальные символы и их позиции
        special_chars = []
        special_positions = []
        
        for i, char in enumerate(s):
            if not char.isalpha():
                special_chars.append(char)
                special_positions.append(i)
        
        # Шаг 3: Разворачиваем буквы
        letters.reverse()
        
        # Шаг 4: Разворачиваем специальные символы
        special_chars.reverse()
        
        # Шаг 5: Собираем результат
        result = [''] * len(s)
        
        for i, pos in enumerate(letter_positions):
            result[pos] = letters[i]
        
        for i, pos in enumerate(special_positions):
            result[pos] = special_chars[i]
        
        return ''.join(result)©leetcode