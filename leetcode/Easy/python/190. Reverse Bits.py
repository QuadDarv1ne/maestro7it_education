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
    def reverseBits(self, n):
        """
        Обращает биты 32-битного беззнакового целого числа.
        
        Args:
            n: Исходное 32-битное беззнаковое целое число
            
        Returns:
            Число с обращенным порядком битов
            
        Пример:
            Вход:  00000010100101000001111010011100
            Выход: 00111001011110000010100101000000
        """
        result = 0
        
        for i in range(32):
            # Сдвигаем результат влево для освобождения места под следующий бит
            result <<= 1
            
            # Получаем младший бит числа n
            bit = n & 1
            
            # Добавляем бит к результату
            result |= bit
            
            # Сдвигаем n вправо для обработки следующего бита
            n >>= 1
        
        return result