"""
Максимальная площадь квадратного поля после удаления заборов

@param m: Количество строк в поле
@param n: Количество столбцов в поле
@param hFences: Список горизонтальных заборов
@param vFences: Список вертикальных заборов
@return: Максимальная площадь квадрата (по модулю 10^9+7) или -1

Сложность: O(h² + v²), где h и v ≤ 600

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
    def maximizeSquareArea(self, m, n, hFences, vFences):
        MOD = 10**9 + 7
        
        # 1. Добавляем граничные значения
        h_list = sorted(hFences + [1, m])
        v_list = sorted(vFences + [1, n])
        
        # 2. Генерируем все возможные разницы
        h_diffs = set()
        v_diffs = set()
        
        for i in range(len(h_list)):
            for j in range(i + 1, len(h_list)):
                h_diffs.add(h_list[j] - h_list[i])
        
        for i in range(len(v_list)):
            for j in range(i + 1, len(v_list)):
                v_diffs.add(v_list[j] - v_list[i])
        
        # 3. Ищем максимальное пересечение
        max_side = 0
        for diff in h_diffs:
            if diff in v_diffs:
                max_side = max(max_side, diff)
        
        # 4. Возвращаем результат
        if max_side == 0:
            return -1
        return (max_side * max_side) % MOD