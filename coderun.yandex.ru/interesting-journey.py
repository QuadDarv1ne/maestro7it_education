'''
https://coderun.yandex.ru/selections/yandex-interview/problems/interesting-journey
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
'''

import sys
import bisect
from collections import deque


def main():
    """
    Решение задачи "Интересное путешествие" с Yandex CodeRun.
    На вход подаются координаты N городов, максимальное расстояние K, 
    и номера начального и конечного городов (A и B).
    Необходимо найти минимальное количество дорог (переездов) от A до B.
    Если путь невозможен, вывести -1.
    
    Оптимизация: используется BFS с динамическим поиском соседей через 
    сортировку по X-координате и бисекцию, что позволяет не строить 
    полный граф и экономит память и время.
    """
    input_data = sys.stdin.read().split()
    if not input_data:
        return
        
    N = int(input_data[0])
    pts = []
    idx = 1
    for i in range(N):
        x = int(input_data[idx])
        y = int(input_data[idx+1])
        pts.append((x, y))
        idx += 2
        
    K = int(input_data[idx]); idx += 1
    A = int(input_data[idx]) - 1  # Приводим к 0-индексации
    B = int(input_data[idx+1]) - 1
    
    if A == B:
        print(0)
        return
        
    # Сортируем непосещенные вершины по X-координате для быстрого поиска диапазона
    unvisited = sorted(range(N), key=lambda i: pts[i][0])
    unvisited_x = [pts[i][0] for i in unvisited]
    
    visited = [False] * N
    visited[A] = True
    
    dist = [-1] * N
    dist[A] = 0
    q = deque([A])
    
    # Функция для очистки массива от посещенных вершин (вызывается периодически)
    def rebuild():
        nonlocal unvisited, unvisited_x
        unvisited = [i for i in unvisited if not visited[i]]
        unvisited_x = [pts[i][0] for i in unvisited]
    
    total_dead_scanned = 0
    
    while q:
        u = q.popleft()
        xu, yu = pts[u]
        
        # Ищем все города, у которых X в диапазоне [xu - K, xu + K]
        left = bisect.bisect_left(unvisited_x, xu - K)
        right = bisect.bisect_right(unvisited_x, xu + K)
        
        new_neighbors = []
        dead_in_query = 0
        
        for i in range(left, right):
            v = unvisited[i]
            if visited[v]:
                dead_in_query += 1
                continue
                
            xv, yv = pts[v]
            # Проверяем Манхэттенское расстояние
            if abs(xu - xv) + abs(yu - yv) <= K:
                visited[v] = True
                dist[v] = dist[u] + 1
                if v == B:
                    print(dist[v])
                    return
                q.append(v)
                new_neighbors.append(v)
        
        total_dead_scanned += dead_in_query
        # Если мы слишком часто "натыкаемся" на уже посещенные вершины в списках,
        # очищаем массивы, чтобы ускорить следующие итерации
        if total_dead_scanned > N:
            rebuild()
            total_dead_scanned = 0
            
    print(-1)


if __name__ == '__main__':
    main()