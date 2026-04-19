#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                         sorting_animation.py                                  ║
║                                                                               ║
║  A comprehensive sorting algorithm animation with visual feedback.            ║
║  Sorts a shelf of 10 blocks using multiple sorting algorithms.                ║
║                                                                               ║
║  Author: Dupley Maxim Igorevich - AGLA                                        ║
║  ORCID:  https://orcid.org/0009-0007-7605-539X                                ║
║  GitHub: https://github.com/QuadDarv1ne/                                      ║
║  Date:   19.04.2026                                                           ║
║                                                                               ║
║  Implemented algorithms:                                                      ║
║    • Bubble Sort      (b)    • Shell Sort      (h)                            ║
║    • Insertion Sort   (i)    • Cocktail Sort   (c)                            ║
║    • Selection Sort   (s)    • Merge Sort      (m)                            ║
║    • Quicksort        (q)                                                    ║
║                                                                               ║
║  Color indicators:                                                            ║
║    🟠 Orange  — element is being moved/changed position                        ║
║    🟣 Purple  — element stays in place / not moved                             ║
║    ⚫ Black   — normal state                                                   ║
║                                                                               ║
║  Controls:                                                                    ║
║    SPACE — quit                     R — randomize array                       ║
║    T     — show performance table   A — run all algorithms (sequential)       ║
║    M     — run all algorithms (multithreaded)                                 ║
║    ESC   — return to main screen                                              ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""
from turtle import *
import random
import time
from collections import defaultdict
import threading
import queue
import copy


class SortingTimer:
    """
    Класс для измерения времени выполнения алгоритмов сортировки.
    Хранит историю запусков и предоставляет аналитику.
    """
    
    def __init__(self):
        self.history = defaultdict(list)
        self.threaded_history = defaultdict(list)
    
    def measure(self, algorithm_name, sort_function, shelf):
        """
        Измеряет время выполнения функции сортировки.
        """
        start_time = time.perf_counter()
        sort_function(shelf)
        end_time = time.perf_counter()
        
        elapsed_time = end_time - start_time
        self.history[algorithm_name].append(elapsed_time)
        
        return elapsed_time
    
    def add_threaded_result(self, algorithm_name, elapsed_time):
        """Добавляет результат многопоточного выполнения"""
        self.threaded_history[algorithm_name].append(elapsed_time)
    
    def get_average(self, algorithm_name, threaded=False):
        """Возвращает среднее время выполнения алгоритма"""
        hist = self.threaded_history if threaded else self.history
        if algorithm_name in hist and hist[algorithm_name]:
            return sum(hist[algorithm_name]) / len(hist[algorithm_name])
        return 0.0
    
    def get_best(self, algorithm_name, threaded=False):
        """Возвращает лучшее время выполнения алгоритма"""
        hist = self.threaded_history if threaded else self.history
        if algorithm_name in hist and hist[algorithm_name]:
            return min(hist[algorithm_name])
        return 0.0
    
    def get_worst(self, algorithm_name, threaded=False):
        """Возвращает худшее время выполнения алгоритма"""
        hist = self.threaded_history if threaded else self.history
        if algorithm_name in hist and hist[algorithm_name]:
            return max(hist[algorithm_name])
        return 0.0
    
    def get_runs_count(self, algorithm_name, threaded=False):
        """Возвращает количество запусков алгоритма"""
        hist = self.threaded_history if threaded else self.history
        return len(hist.get(algorithm_name, []))
    
    def clear_history(self):
        """Очищает историю измерений"""
        self.history.clear()
        self.threaded_history.clear()
    
    def generate_table(self, threaded=False):
        """
        Генерирует текстовую таблицу с результатами измерений.
        """
        hist = self.threaded_history if threaded else self.history
        mode_str = "(Многопоточный режим)" if threaded else "(Последовательный режим)"
        
        if not hist:
            return f"Нет данных для отображения. {mode_str}"
        
        algorithms = list(hist.keys())
        
        # Заголовок таблицы
        table = "╔══════════════════════╦═══════════╦═══════════╦═══════════╦═══════════╦═══════════╗\n"
        table += f"║ Алгоритм {mode_str:29}║ Запусков  ║ Среднее   ║ Лучшее    ║ Худшее    ║ Последнее ║\n"
        table += "╠══════════════════════╬═══════════╬═══════════╬═══════════╬═══════════╬═══════════╣\n"
        
        # Данные таблицы
        for algo in sorted(algorithms):
            runs = self.get_runs_count(algo, threaded)
            avg = self.get_average(algo, threaded)
            best = self.get_best(algo, threaded)
            worst = self.get_worst(algo, threaded)
            last = hist[algo][-1] if hist[algo] else 0.0
            
            algo_name = algo.ljust(20)[:20]
            table += f"║ {algo_name} ║ {runs:^9d} ║ {avg:^9.4f} ║ {best:^9.4f} ║ {worst:^9.4f} ║ {last:^9.4f} ║\n"
        
        table += "╚══════════════════════╩═══════════╩═══════════╩═══════════╩═══════════╩═══════════╝\n"
        table += "\n📊 Все времена указаны в секундах.\n"
        
        return table
    
    def generate_comparison_chart(self, threaded=False):
        """
        Генерирует сравнительную диаграмму средних времен.
        """
        hist = self.threaded_history if threaded else self.history
        mode_str = "МНОГОПОТОЧНЫЙ" if threaded else "ПОСЛЕДОВАТЕЛЬНЫЙ"
        
        if not hist:
            return f"Нет данных для построения диаграммы ({mode_str})."
        
        chart = f"\n📈 Сравнение среднего времени выполнения ({mode_str}):\n"
        chart += "─" * 60 + "\n"
        
        max_avg = max(self.get_average(algo, threaded) for algo in hist.keys())
        
        for algo in sorted(hist.keys()):
            avg = self.get_average(algo, threaded)
            runs = self.get_runs_count(algo, threaded)
            
            bar_length = int((avg / max_avg) * 30) if max_avg > 0 else 0
            bar = "█" * bar_length + "░" * (30 - bar_length)
            chart += f"{algo:20} [{bar}] {avg:.4f}s ({runs} запусков)\n"
        
        chart += "─" * 60
        return chart
    
    def generate_comparison_between_modes(self):
        """
        Сравнивает последовательный и многопоточный режимы.
        """
        if not self.history and not self.threaded_history:
            return "Нет данных для сравнения режимов."
        
        chart = "\n📊 СРАВНЕНИЕ РЕЖИМОВ ВЫПОЛНЕНИЯ:\n"
        chart += "═" * 70 + "\n"
        chart += f"{'Алгоритм':20} {'Послед. (с)':12} {'Многопот. (с)':12} {'Ускорение':10}\n"
        chart += "─" * 70 + "\n"
        
        all_algos = set(list(self.history.keys()) + list(self.threaded_history.keys()))
        
        for algo in sorted(all_algos):
            seq_avg = self.get_average(algo, threaded=False)
            thread_avg = self.get_average(algo, threaded=True)
            
            if seq_avg > 0 and thread_avg > 0:
                speedup = seq_avg / thread_avg
                speedup_str = f"{speedup:.2f}x"
            else:
                speedup_str = "N/A"
            
            chart += f"{algo:20} {seq_avg:12.4f} {thread_avg:12.4f} {speedup_str:>10}\n"
        
        chart += "═" * 70
        return chart


class Block(Turtle):
    """
    Визуальный блок для анимации сортировки.
    """
    
    def __init__(self, size):
        self.size = size
        self.original_position = None
        Turtle.__init__(self, shape="square", visible=False)
        self.pu()
        self.shapesize(size * 1.5, 1.5, 2)
        self.fillcolor("black")
        self.st()

    def glow_moving(self):
        """Подсветка оранжевым — элемент перемещается/меняет позицию"""
        self.fillcolor("orange")

    def glow_static(self):
        """Подсветка фиолетовым — элемент остаётся на месте"""
        self.fillcolor("purple")

    def unglow(self):
        """Возврат к нормальному цвету (чёрный)"""
        self.fillcolor("black")
    
    def mark_position(self):
        """Запоминает текущую позицию для отслеживания перемещения"""
        self.original_position = self.pos()
    
    def has_moved(self):
        """Проверяет, переместился ли блок относительно запомненной позиции"""
        if self.original_position is None:
            return False
        return self.pos() != self.original_position

    def __repr__(self):
        return f"Block(size={self.size})"


class Shelf(list):
    """
    Полка для хранения и визуализации блоков.
    """
    
    def __init__(self, y):
        self.y = y
        self.x = -150

    def push(self, d):
        width, _, _ = d.shapesize()
        y_offset = width / 2 * 20
        d.sety(self.y + y_offset)
        d.setx(self.x + 34 * len(self))
        self.append(d)

    def _close_gap_from_i(self, i):
        for b in self[i:]:
            xpos, _ = b.pos()
            b.setx(xpos - 34)

    def _open_gap_from_i(self, i):
        for b in self[i:]:
            xpos, _ = b.pos()
            b.setx(xpos + 34)

    def pop(self, key):
        b = list.pop(self, key)
        b.glow_moving()
        b.sety(200)
        self._close_gap_from_i(key)
        return b

    def insert(self, key, b):
        self._open_gap_from_i(key)
        list.insert(self, key, b)
        b.setx(self.x + 34 * key)
        width, _, _ = b.shapesize()
        y_offset = width / 2 * 20
        b.sety(self.y + y_offset)
        b.unglow()

    def swap(self, i, j):
        if i == j:
            return
        
        self[i].glow_moving()
        self[j].glow_moving()
        
        for _ in range(5):
            self[i].sety(self[i].ycor() + 4)
            self[j].sety(self[j].ycor() + 4)
            update()
            time.sleep(0.02)
        
        xi = self[i].xcor()
        xj = self[j].xcor()
        self[i].setx(xj)
        self[j].setx(xi)
        self[i], self[j] = self[j], self[i]
        
        for _ in range(5):
            self[i].sety(self[i].ycor() - 4)
            self[j].sety(self[j].ycor() - 4)
            update()
            time.sleep(0.02)
        
        self[i].unglow()
        self[j].unglow()
    
    def mark_all_positions(self):
        for block in self:
            block.mark_position()
    
    def highlight_changes(self):
        for block in self:
            if block.has_moved():
                block.glow_moving()
            else:
                block.glow_static()
    
    def reset_highlights(self):
        for block in self:
            block.unglow()
    
    def get_state(self):
        return [block.size for block in self]
    
    def restore_state(self, state):
        self.clear()
        clear()
        for size in state:
            self.push(Block(size))
    
    def clone_for_threading(self):
        """
        Создаёт копию полки для использования в отдельном потоке.
        Возвращает ShelfData с размерами блоков.
        """
        return ShelfData([block.size for block in self])


class ShelfData:
    """
    Класс для хранения данных полки без визуальных элементов.
    Используется в многопоточном режиме.
    """
    
    def __init__(self, sizes):
        self.sizes = sizes
        self.length = len(sizes)
    
    def get_state(self):
        return self.sizes.copy()
    
    def __len__(self):
        return self.length


# Глобальный таймер
timer = SortingTimer()


# ═══════════════════════════════════════════════════════════════════════════════
#                    MULTITHREADED ALGORITHM IMPLEMENTATIONS
#                    (без анимации, только для измерения времени)
# ═══════════════════════════════════════════════════════════════════════════════

def bubble_sort_data(data):
    """Пузырьковая сортировка для данных"""
    arr = data.sizes
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr


def insertion_sort_data(data):
    """Сортировка вставками для данных"""
    arr = data.sizes
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def selection_sort_data(data):
    """Сортировка выбором для данных"""
    arr = data.sizes
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


def quick_sort_data_helper(arr, low, high):
    if low < high:
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        pi = i + 1
        quick_sort_data_helper(arr, low, pi - 1)
        quick_sort_data_helper(arr, pi + 1, high)


def quick_sort_data(data):
    """Быстрая сортировка для данных"""
    arr = data.sizes
    quick_sort_data_helper(arr, 0, len(arr) - 1)
    return arr


def shell_sort_data(data):
    """Сортировка Шелла для данных"""
    arr = data.sizes
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2
    return arr


def cocktail_sort_data(data):
    """Шейкерная сортировка для данных"""
    arr = data.sizes
    n = len(arr)
    swapped = True
    start = 0
    end = n - 1
    while swapped:
        swapped = False
        for i in range(start, end):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True
        if not swapped:
            break
        swapped = False
        end -= 1
        for i in range(end - 1, start - 1, -1):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True
        start += 1
    return arr


def merge_sort_data_helper(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort_data_helper(arr[:mid])
    right = merge_sort_data_helper(arr[mid:])
    return merge_data(left, right)


def merge_data(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def merge_sort_data(data):
    """Сортировка слиянием для данных"""
    arr = data.sizes
    sorted_arr = merge_sort_data_helper(arr)
    data.sizes[:] = sorted_arr
    return data.sizes


# ═══════════════════════════════════════════════════════════════════════════════
#                    VISUAL ALGORITHM IMPLEMENTATIONS
# ═══════════════════════════════════════════════════════════════════════════════

def bubble_sort(shelf):
    length = len(shelf)
    shelf.mark_all_positions()
    
    for i in range(length):
        swapped = False
        for j in range(0, length - i - 1):
            shelf[j].glow_static()
            shelf[j + 1].glow_static()
            update()
            time.sleep(0.1)
            
            if shelf[j].size > shelf[j + 1].size:
                shelf.swap(j, j + 1)
                swapped = True
            
            shelf[j].unglow()
            shelf[j + 1].unglow()
        
        if not swapped:
            break
    
    shelf.highlight_changes()
    update()
    time.sleep(1)
    shelf.reset_highlights()


def insertion_sort(shelf):
    length = len(shelf)
    shelf.mark_all_positions()
    
    for i in range(1, length):
        hole = i
        shelf[i].glow_static()
        update()
        time.sleep(0.1)
        
        while hole > 0 and shelf[i].size < shelf[hole - 1].size:
            shelf[hole - 1].glow_static()
            update()
            time.sleep(0.1)
            shelf[hole - 1].unglow()
            hole = hole - 1
        
        shelf[i].unglow()
        if hole != i:
            shelf.insert(hole, shelf.pop(i))
    
    shelf.highlight_changes()
    update()
    time.sleep(1)
    shelf.reset_highlights()


def selection_sort(shelf):
    length = len(shelf)
    shelf.mark_all_positions()
    
    for j in range(0, length - 1):
        imin = j
        shelf[j].glow_static()
        
        for i in range(j + 1, length):
            shelf[i].glow_static()
            update()
            time.sleep(0.05)
            
            if shelf[i].size < shelf[imin].size:
                if imin != j:
                    shelf[imin].unglow()
                imin = i
            else:
                shelf[i].unglow()
        
        if imin != j:
            shelf[imin].glow_moving()
            shelf.insert(j, shelf.pop(imin))
        
        shelf[j].unglow()
        if imin != j:
            shelf[imin].unglow()
    
    shelf.highlight_changes()
    update()
    time.sleep(1)
    shelf.reset_highlights()


def partition(shelf, left, right, pivot_index):
    pivot = shelf[pivot_index]
    pivot.glow_static()
    update()
    time.sleep(0.1)
    
    shelf.insert(right, shelf.pop(pivot_index))
    store_index = left
    
    for i in range(left, right):
        shelf[i].glow_static()
        update()
        time.sleep(0.05)
        
        if shelf[i].size < pivot.size:
            shelf.insert(store_index, shelf.pop(i))
            store_index = store_index + 1
        
        shelf[i].unglow()
    
    shelf.insert(store_index, shelf.pop(right))
    shelf[store_index].unglow()
    return store_index


def quick_sort(shelf, left, right):
    if left < right:
        pivot_index = left
        pivot_new_index = partition(shelf, left, right, pivot_index)
        quick_sort(shelf, left, pivot_new_index - 1)
        quick_sort(shelf, pivot_new_index + 1, right)


def quick_sort_wrapper(shelf):
    shelf.mark_all_positions()
    quick_sort(shelf, 0, len(shelf) - 1)
    shelf.highlight_changes()
    update()
    time.sleep(1)
    shelf.reset_highlights()


def shell_sort(shelf):
    length = len(shelf)
    shelf.mark_all_positions()
    gap = length // 2
    
    while gap > 0:
        for i in range(gap, length):
            temp = shelf[i]
            temp.glow_static()
            update()
            time.sleep(0.05)
            
            j = i
            while j >= gap:
                shelf[j - gap].glow_static()
                update()
                time.sleep(0.05)
                
                if shelf[j - gap].size > temp.size:
                    shelf[j - gap].glow_moving()
                    shelf[j] = shelf[j - gap]
                    shelf[j].unglow()
                    shelf[j - gap].unglow()
                    j -= gap
                else:
                    shelf[j - gap].unglow()
                    break
            
            shelf[j] = temp
            temp.unglow()
        
        gap //= 2
    
    shelf.highlight_changes()
    update()
    time.sleep(1)
    shelf.reset_highlights()


def cocktail_sort(shelf):
    length = len(shelf)
    shelf.mark_all_positions()
    swapped = True
    start = 0
    end = length - 1
    
    while swapped:
        swapped = False
        for i in range(start, end):
            shelf[i].glow_static()
            shelf[i + 1].glow_static()
            update()
            time.sleep(0.05)
            
            if shelf[i].size > shelf[i + 1].size:
                shelf.swap(i, i + 1)
                swapped = True
            
            shelf[i].unglow()
            shelf[i + 1].unglow()
        
        if not swapped:
            break
        
        swapped = False
        end -= 1
        for i in range(end - 1, start - 1, -1):
            shelf[i].glow_static()
            shelf[i + 1].glow_static()
            update()
            time.sleep(0.05)
            
            if shelf[i].size > shelf[i + 1].size:
                shelf.swap(i, i + 1)
                swapped = True
            
            shelf[i].unglow()
            shelf[i + 1].unglow()
        
        start += 1
    
    shelf.highlight_changes()
    update()
    time.sleep(1)
    shelf.reset_highlights()


def merge(shelf, left, mid, right):
    left_part = []
    right_part = []
    
    for i in range(left, mid + 1):
        left_part.append(shelf[i])
        shelf[i].glow_static()
        shelf[i].sety(100)
    
    for i in range(mid + 1, right + 1):
        right_part.append(shelf[i])
        shelf[i].glow_static()
        shelf[i].sety(100)
    
    update()
    time.sleep(0.3)
    
    i = j = 0
    k = left
    
    while i < len(left_part) and j < len(right_part):
        left_part[i].glow_static()
        right_part[j].glow_static()
        update()
        time.sleep(0.1)
        
        if left_part[i].size <= right_part[j].size:
            shelf[k] = left_part[i]
            left_part[i].unglow()
            i += 1
        else:
            shelf[k] = right_part[j]
            right_part[j].unglow()
            j += 1
        
        shelf[k].sety(s.y)
        shelf[k].glow_moving()
        k += 1
    
    while i < len(left_part):
        shelf[k] = left_part[i]
        shelf[k].sety(s.y)
        shelf[k].glow_moving()
        i += 1
        k += 1
    
    while j < len(right_part):
        shelf[k] = right_part[j]
        shelf[k].sety(s.y)
        shelf[k].glow_moving()
        j += 1
        k += 1
    
    for idx in range(left, right + 1):
        shelf[idx].setx(s.x + 34 * idx)


def merge_sort_helper(shelf, left, right):
    if left < right:
        mid = (left + right) // 2
        merge_sort_helper(shelf, left, mid)
        merge_sort_helper(shelf, mid + 1, right)
        merge(shelf, left, mid, right)


def merge_sort(shelf):
    shelf.mark_all_positions()
    merge_sort_helper(shelf, 0, len(shelf) - 1)
    shelf.highlight_changes()
    update()
    time.sleep(1)
    shelf.reset_highlights()


# ═══════════════════════════════════════════════════════════════════════════════
#                           INTERFACE FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def randomize():
    disable_keys()
    clear()
    target = list(range(10))
    random.shuffle(target)
    for i, t in enumerate(target):
        for j in range(i, len(s)):
            if s[j].size == t + 1:
                s.insert(i, s.pop(j))
    s.reset_highlights()
    show_main_screen()
    enable_keys()


def show_main_screen():
    clear()
    show_text(instructions1)
    show_text(instructions2, line=1)
    show_text(instructions3, line=2)
    show_text(instructions4, line=3)


def show_text(text, line=0):
    line = 20 * line
    goto(0, -250 - line)
    write(text, align="center", font=("Courier", 12, "bold"))


def return_to_main():
    clear()
    show_main_screen()
    enable_keys()
    listen()


def show_performance_table():
    disable_keys()
    clear()
    
    # Генерируем таблицы
    table_seq = timer.generate_table(threaded=False)
    table_thread = timer.generate_table(threaded=True)
    chart_seq = timer.generate_comparison_chart(threaded=False)
    chart_thread = timer.generate_comparison_chart(threaded=True)
    comparison = timer.generate_comparison_between_modes()
    
    # Выводим в консоль
    print("\n" + "=" * 80)
    print("                    📊 PERFORMANCE ANALYTICS")
    print("=" * 80)
    print(table_seq)
    print(chart_seq)
    print("\n" + "=" * 80)
    print(table_thread)
    print(chart_thread)
    print(comparison)
    print("=" * 80 + "\n")
    
    # Показываем на экране
    goto(0, 200)
    write("📊 Таблицы результатов выведены в консоль", align="center", font=("Arial", 14, "bold"))
    
    goto(0, 150)
    write("Последовательный режим:", align="center", font=("Arial", 12, "bold"))
    
    y_pos = 120
    if timer.history:
        for algo in sorted(timer.history.keys()):
            if timer.history[algo]:
                last_time = timer.history[algo][-1]
                goto(0, y_pos)
                write(f"{algo}: {last_time:.4f}s", align="center", font=("Courier", 11, "normal"))
                y_pos -= 25
    else:
        goto(0, y_pos)
        write("Нет данных", align="center", font=("Arial", 11, "normal"))
        y_pos -= 25
    
    y_pos -= 10
    goto(0, y_pos)
    write("Многопоточный режим:", align="center", font=("Arial", 12, "bold"))
    y_pos -= 25
    
    if timer.threaded_history:
        for algo in sorted(timer.threaded_history.keys()):
            if timer.threaded_history[algo]:
                last_time = timer.threaded_history[algo][-1]
                goto(0, y_pos)
                write(f"{algo}: {last_time:.4f}s", align="center", font=("Courier", 11, "normal"))
                y_pos -= 25
    
    goto(0, -150)
    write("ESC - главный экран | SPACE - выход", align="center", font=("Arial", 11, "bold"))
    
    onkey(return_to_main, "Escape")
    onkey(bye, "space")
    listen()


def run_all_algorithms_sequential():
    """
    Запускает все алгоритмы последовательно с полной анимацией.
    """
    disable_keys()
    
    algorithms = [
        ("Bubble Sort", bubble_sort),
        ("Insertion Sort", insertion_sort),
        ("Selection Sort", selection_sort),
        ("Quicksort", quick_sort_wrapper),
        ("Shell Sort", shell_sort),
        ("Cocktail Sort", cocktail_sort),
        ("Merge Sort", merge_sort)
    ]
    
    original_state = s.get_state()
    cancelled = False
    
    def cancel_execution():
        nonlocal cancelled
        cancelled = True
    
    onkey(cancel_execution, "Escape")
    listen()
    
    results = []
    
    for i, (name, sort_func) in enumerate(algorithms):
        if cancelled:
            break
        
        # Восстанавливаем состояние и показываем анимацию
        s.restore_state(original_state)
        clear()
        goto(0, 200)
        write(f"⏳ {name} ({i+1}/{len(algorithms)})", align="center", font=("Arial", 14, "bold"))
        goto(0, 150)
        write("ESC - отмена", align="center", font=("Arial", 11, "normal"))
        update()
        time.sleep(0.5)
        
        # Запускаем с измерением времени
        elapsed = timer.measure(name, sort_func, s)
        results.append((name, elapsed))
    
    # Восстанавливаем исходное состояние
    s.restore_state(original_state)
    
    if not cancelled and results:
        clear()
        goto(0, 200)
        write("📊 Последовательное выполнение завершено!", align="center", font=("Arial", 14, "bold"))
        
        y_pos = 150
        for name, elapsed in results:
            goto(0, y_pos)
            write(f"{name}: {elapsed:.4f} сек", align="center", font=("Courier", 11, "normal"))
            y_pos -= 25
        
        goto(0, -150)
        write("ESC - главный экран | SPACE - выход", align="center", font=("Arial", 11, "bold"))
        
        # Вывод в консоль
        print("\n" + "=" * 80)
        print("       📊 РЕЗУЛЬТАТЫ ПОСЛЕДОВАТЕЛЬНОГО ВЫПОЛНЕНИЯ")
        print("=" * 80)
        for name, elapsed in results:
            print(f"  {name:20} : {elapsed:.4f} сек")
        print("=" * 80)
    
    onkey(return_to_main, "Escape")
    onkey(bye, "space")
    listen()


def run_all_algorithms_multithreaded():
    """
    Запускает все алгоритмы в многопоточном режиме (без анимации).
    """
    disable_keys()
    clear()
    
    goto(0, 200)
    write("🚀 Многопоточный запуск всех алгоритмов...", align="center", font=("Arial", 14, "bold"))
    goto(0, 150)
    write("(без анимации для точного измерения)", align="center", font=("Arial", 11, "normal"))
    update()
    
    algorithms = [
        ("Bubble Sort", bubble_sort_data),
        ("Insertion Sort", insertion_sort_data),
        ("Selection Sort", selection_sort_data),
        ("Quicksort", quick_sort_data),
        ("Shell Sort", shell_sort_data),
        ("Cocktail Sort", cocktail_sort_data),
        ("Merge Sort", merge_sort_data)
    ]
    
    # Получаем данные для сортировки
    original_sizes = [block.size for block in s]
    data = ShelfData(original_sizes)
    
    results = {}
    threads = []
    result_queue = queue.Queue()
    
    def run_in_thread(name, sort_func, data_copy):
        start_time = time.perf_counter()
        sort_func(data_copy)
        end_time = time.perf_counter()
        result_queue.put((name, end_time - start_time))
    
    # Запускаем все алгоритмы в отдельных потоках
    for name, sort_func in algorithms:
        data_copy = ShelfData(original_sizes.copy())
        thread = threading.Thread(target=run_in_thread, args=(name, sort_func, data_copy))
        threads.append(thread)
        thread.start()
    
    # Ждём завершения всех потоков
    for thread in threads:
        thread.join()
    
    # Собираем результаты
    while not result_queue.empty():
        name, elapsed = result_queue.get()
        timer.add_threaded_result(name, elapsed)
        results[name] = elapsed
    
    # Показываем результаты
    clear()
    goto(0, 200)
    write("✅ Многопоточное выполнение завершено!", align="center", font=("Arial", 14, "bold"))
    
    y_pos = 150
    for name in sorted(results.keys()):
        goto(0, y_pos)
        write(f"{name}: {results[name]:.4f} сек", align="center", font=("Courier", 11, "normal"))
        y_pos -= 25
    
    goto(0, -150)
    write("ESC - главный экран | SPACE - выход", align="center", font=("Arial", 11, "bold"))
    
    # Вывод в консоль
    print("\n" + "=" * 80)
    print("        📊 РЕЗУЛЬТАТЫ МНОГОПОТОЧНОГО ВЫПОЛНЕНИЯ")
    print("=" * 80)
    for name in sorted(results.keys()):
        print(f"  {name:20} : {results[name]:.4f} сек")
    print("=" * 80)
    
    onkey(return_to_main, "Escape")
    onkey(bye, "space")
    listen()


def create_sort_wrapper(sort_func, name):
    def wrapper():
        disable_keys()
        clear()
        show_text(name)
        elapsed = timer.measure(name, sort_func, s)
        clear()
        show_main_screen()
        goto(0, -300)
        write(f"⏱️ Время выполнения: {elapsed:.4f} сек", align="center", font=("Arial", 11, "normal"))
        enable_keys()
        print(f"[TIMER] {name}: {elapsed:.4f} сек")
    return wrapper


# Создаём функции запуска
start_bubble = create_sort_wrapper(bubble_sort, "Bubble Sort")
start_insertion = create_sort_wrapper(insertion_sort, "Insertion Sort")
start_selection = create_sort_wrapper(selection_sort, "Selection Sort")
start_quick = create_sort_wrapper(quick_sort_wrapper, "Quicksort")
start_shell = create_sort_wrapper(shell_sort, "Shell Sort")
start_cocktail = create_sort_wrapper(cocktail_sort, "Cocktail Sort")
start_merge = create_sort_wrapper(merge_sort, "Merge Sort")


# ═══════════════════════════════════════════════════════════════════════════════
#                            INITIALIZATION
# ═══════════════════════════════════════════════════════════════════════════════

def init_shelf():
    global s
    s = Shelf(-200)
    vals = (4, 2, 8, 9, 1, 5, 10, 3, 7, 6)
    for i in vals:
        s.push(Block(i))


def disable_keys():
    for key in ["i", "s", "q", "b", "h", "c", "m", "r", "t", "a", "x"]:
        onkey(None, key)


def enable_keys():
    onkey(start_insertion, "i")
    onkey(start_selection, "s")
    onkey(start_quick, "q")
    onkey(start_bubble, "b")
    onkey(start_shell, "h")
    onkey(start_cocktail, "c")
    onkey(start_merge, "m")
    onkey(randomize, "r")
    onkey(show_performance_table, "t")
    onkey(run_all_algorithms_sequential, "a")
    onkey(run_all_algorithms_multithreaded, "x")
    onkey(bye, "space")


def main():
    getscreen().clearscreen()
    tracer(False)
    ht()
    penup()
    init_shelf()
    show_main_screen()
    enable_keys()
    listen()
    tracer(True)
    return "EVENTLOOP"


# ═══════════════════════════════════════════════════════════════════════════════
#                            GLOBAL STRINGS
# ═══════════════════════════════════════════════════════════════════════════════

instructions1 = "press i:insertion  s:selection  q:quicksort  b:bubble"
instructions2 = "press h:shell  c:cocktail  m:merge  r:randomize"
instructions3 = "t:show table  a:run all (seq)  x:run all (threaded)"
instructions4 = "space:quit  ESC:return  (orange=moved, purple=static)"


if __name__ == "__main__":
    print("""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                         SORTING ANIMATION v3.0                                ║
║                                                                               ║
║  Author: Dupley Maxim Igorevich - AGLA                                        ║
║  ORCID:  https://orcid.org/0009-0007-7605-539X                                ║
║  GitHub: https://github.com/QuadDarv1ne/                                      ║
║  Date:   19.04.2026                                                           ║
║                                                                               ║
║  Features:                                                                    ║
║    • Sequential mode with full animation (A)                                  ║
║    • Multithreaded mode for performance testing (X)                           ║
║    • Comparative analytics between modes                                      ║
╚═══════════════════════════════════════════════════════════════════════════════╝
    """)
    msg = main()
    mainloop()
