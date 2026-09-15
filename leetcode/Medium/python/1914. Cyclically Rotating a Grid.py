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
    def rotateGrid(self, grid, k):
        """
        Циклически сдвигает каждый слой матрицы на k шагов против часовой стрелки.

        Args:
            grid: Исходная матрица m x n (m и n - чётные).
            k: Количество циклических сдвигов.

        Returns:
            Матрица после выполнения k циклических сдвигов для каждого слоя.
        """
        m, n = len(grid), len(grid[0])
        layers = min(m, n) // 2  # Количество слоёв

        for layer in range(layers):
            # Извлекаем элементы текущего слоя в массив
            elements = []
            # Верхняя строка (слева направо)
            for col in range(layer, n - layer):
                elements.append(grid[layer][col])
            # Правый столбец (сверху вниз, без первого и последнего элемента)
            for row in range(layer + 1, m - layer):
                elements.append(grid[row][n - 1 - layer])
            # Нижняя строка (справа налево)
            if m - 1 - layer > layer:
                for col in range(n - 2 - layer, layer - 1, -1):
                    elements.append(grid[m - 1 - layer][col])
            # Левый столбец (снизу вверх)
            if n - 1 - layer > layer:
                for row in range(m - 2 - layer, layer, -1):
                    elements.append(grid[row][layer])

            # Вычисляем эффективный сдвиг
            length = len(elements)
            if length == 0:
                continue
            shift = k % length

            # Сдвигаем массив
            rotated = elements[shift:] + elements[:shift]

            # Записываем элементы обратно в слой
            idx = 0
            # Верхняя строка
            for col in range(layer, n - layer):
                grid[layer][col] = rotated[idx]
                idx += 1
            # Правый столбец
            for row in range(layer + 1, m - layer):
                grid[row][n - 1 - layer] = rotated[idx]
                idx += 1
            # Нижняя строка
            if m - 1 - layer > layer:
                for col in range(n - 2 - layer, layer - 1, -1):
                    grid[m - 1 - layer][col] = rotated[idx]
                    idx += 1
            # Левый столбец
            if n - 1 - layer > layer:
                for row in range(m - 2 - layer, layer, -1):
                    grid[row][layer] = rotated[idx]
                    idx += 1

        return grid