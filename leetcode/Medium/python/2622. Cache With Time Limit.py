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

import time

class TimeLimitedCache:
    def __init__(self):
        # Словарь: ключ -> (значение, время_истечения)
        self.cache = {}

    def set(self, key: int, value: int, duration: int) -> bool:
        """
        Сохраняет ключ-значение с временем жизни duration (мс).
        Возвращает True, если ключ уже существовал и не истёк.
        """
        now = time.time() * 1000  # текущее время в миллисекундах
        expiration = now + duration

        # Проверяем, существует ли ключ и не истёк ли он
        existed = False
        if key in self.cache:
            old_value, old_exp = self.cache[key]
            if old_exp > now:
                existed = True
            # Старую запись можно перезаписать (или удалить)
        self.cache[key] = (value, expiration)
        return existed

    def get(self, key: int) -> int:
        """
        Возвращает значение, если ключ существует и не истёк, иначе -1.
        """
        now = time.time() * 1000
        if key in self.cache:
            value, exp = self.cache[key]
            if exp > now:
                return value
            else:
                # Удаляем истекший ключ
                del self.cache[key]
        return -1

    def count(self) -> int:
        """
        Возвращает количество неистекших ключей.
        """
        now = time.time() * 1000
        # Собираем истекшие ключи для удаления
        expired = [k for k, (_, exp) in self.cache.items() if exp <= now]
        for k in expired:
            del self.cache[k]
        return len(self.cache)