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

# from typing import List
from collections import deque

class Solution:
    def findOrder(self, numCourses, prerequisites):
        """
        Находит порядок прохождения курсов с учетом предварительных требований.
        
        Args:
            numCourses: количество курсов (вершины графа)
            prerequisites: список предварительных условий [a, b], где b -> a (b должен быть пройден до a)
            
        Returns:
            Порядок прохождения курсов или пустой список, если невозможно пройти все курсы.
            
        Алгоритм (Топологическая сортировка - алгоритм Кана):
        1. Строим граф зависимостей и массив входящих степеней
        2. Находим все вершины с нулевой входящей степенью (начальные курсы)
        3. Последовательно обрабатываем вершины, уменьшая входящие степени их потомков
        4. Если все вершины обработаны - возвращаем порядок, иначе - пустой список
        
        Сложность: O(V + E) по времени и памяти
        """
        # Инициализация графа и массива входящих степеней
        graph = [[] for _ in range(numCourses)]
        in_degree = [0] * numCourses
        
        # Построение графа и подсчет входящих степеней
        for course, prereq in prerequisites:
            graph[prereq].append(course)  # prereq -> course
            in_degree[course] += 1
        
        # Очередь для вершин с нулевой входящей степенью
        queue = deque([i for i in range(numCourses) if in_degree[i] == 0])
        order = []
        
        # Обработка вершин в порядке топологической сортировки
        while queue:
            node = queue.popleft()
            order.append(node)
            
            # Уменьшаем входящие степени соседей
            for neighbor in graph[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        # Проверяем, прошли ли все курсы
        return order if len(order) == numCourses else []