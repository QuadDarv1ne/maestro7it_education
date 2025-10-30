using System;
using System.Collections.Generic;

public static class SortingAlgorithms
{
    // 1. Пузырьковая сортировка (Bubble Sort)
    // Сложность: O(n²) — худший и средний случаи; O(n) — лучший (если оптимизировано)
    // Стабильная, in-place
    public static void BubbleSort<T>(T[] array) where T : IComparable<T>
    {
        if (array == null || array.Length <= 1) return;

        int n = array.Length;
        bool swapped;
        for (int i = 0; i < n - 1; i++)
        {
            swapped = false;
            for (int j = 0; j < n - i - 1; j++)
            {
                if (array[j].CompareTo(array[j + 1]) > 0)
                {
                    Swap(array, j, j + 1);
                    swapped = true;
                }
            }
            // Оптимизация: если не было обменов — массив отсортирован
            if (!swapped) break;
        }
    }

    // 2. Сортировка выбором (Selection Sort)
    // Сложность: O(n²) во всех случаях
    // Нестабильная, in-place
    public static void SelectionSort<T>(T[] array) where T : IComparable<T>
    {
        if (array == null || array.Length <= 1) return;

        int n = array.Length;
        for (int i = 0; i < n - 1; i++)
        {
            int minIndex = i;
            for (int j = i + 1; j < n; j++)
            {
                if (array[j].CompareTo(array[minIndex]) < 0)
                    minIndex = j;
            }
            if (minIndex != i)
                Swap(array, i, minIndex);
        }
    }

    // 3. Сортировка вставками (Insertion Sort)
    // Сложность: O(n²) — худший/средний; O(n) — лучший (почти отсортированный массив)
    // Стабильная, in-place, эффективна для малых массивов
    public static void InsertionSort<T>(T[] array) where T : IComparable<T>
    {
        if (array == null || array.Length <= 1) return;

        for (int i = 1; i < array.Length; i++)
        {
            T key = array[i];
            int j = i - 1;
            while (j >= 0 && array[j].CompareTo(key) > 0)
            {
                array[j + 1] = array[j];
                j--;
            }
            array[j + 1] = key;
        }
    }

    // 4. Быстрая сортировка (Quick Sort)
    // Сложность: O(n log n) — средний; O(n²) — худший (редко при случайном выборе опоры)
    // Нестабильная, in-place (рекурсивная, требует O(log n) стека)
    public static void QuickSort<T>(T[] array) where T : IComparable<T>
    {
        if (array == null || array.Length <= 1) return;
        QuickSortInternal(array, 0, array.Length - 1);
    }

    private static void QuickSortInternal<T>(T[] array, int left, int right) where T : IComparable<T>
    {
        if (left >= right) return;

        int pivotIndex = Partition(array, left, right);
        QuickSortInternal(array, left, pivotIndex - 1);
        QuickSortInternal(array, pivotIndex + 1, right);
    }

    private static int Partition<T>(T[] array, int left, int right) where T : IComparable<T>
    {
        // Выбор последнего элемента как опорного (можно улучшить рандомизацией)
        T pivot = array[right];
        int i = left - 1;

        for (int j = left; j < right; j++)
        {
            if (array[j].CompareTo(pivot) <= 0)
            {
                i++;
                Swap(array, i, j);
            }
        }
        Swap(array, i + 1, right);
        return i + 1;
    }

    // 5. Сортировка слиянием (Merge Sort)
    // Сложность: O(n log n) во всех случаях
    // Стабильная, не in-place (требует O(n) дополнительной памяти)
    public static void MergeSort<T>(T[] array) where T : IComparable<T>
    {
        if (array == null || array.Length <= 1) return;
        T[] temp = new T[array.Length];
        MergeSortInternal(array, temp, 0, array.Length - 1);
    }

    private static void MergeSortInternal<T>(T[] array, T[] temp, int left, int right) where T : IComparable<T>
    {
        if (left >= right) return;

        int mid = left + (right - left) / 2;
        MergeSortInternal(array, temp, left, mid);
        MergeSortInternal(array, temp, mid + 1, right);
        Merge(temp, array, left, mid, right);
    }

    private static void Merge<T>(T[] temp, T[] array, int left, int mid, int right) where T : IComparable<T>
    {
        Array.Copy(array, left, temp, left, right - left + 1);

        int i = left, j = mid + 1, k = left;

        while (i <= mid && j <= right)
        {
            if (temp[i].CompareTo(temp[j]) <= 0)
                array[k++] = temp[i++];
            else
                array[k++] = temp[j++];
        }

        while (i <= mid)
            array[k++] = temp[i++];

        while (j <= right)
            array[k++] = temp[j++];
    }

    // 6. Пирамидальная сортировка (Heap Sort)
    // Сложность: O(n log n) во всех случаях
    // Нестабильная, in-place
    public static void HeapSort<T>(T[] array) where T : IComparable<T>
    {
        if (array == null || array.Length <= 1) return;

        int n = array.Length;

        // Построение кучи (перегруппировка массива)
        for (int i = n / 2 - 1; i >= 0; i--)
            Heapify(array, n, i);

        // Извлечение элементов из кучи по одному
        for (int i = n - 1; i > 0; i--)
        {
            Swap(array, 0, i); // переместить текущий корень в конец
            Heapify(array, i, 0); // вызвать heapify на уменьшенной куче
        }
    }

    private static void Heapify<T>(T[] array, int heapSize, int rootIndex) where T : IComparable<T>
    {
        int largest = rootIndex;
        int left = 2 * rootIndex + 1;
        int right = 2 * rootIndex + 2;

        if (left < heapSize && array[left].CompareTo(array[largest]) > 0)
            largest = left;

        if (right < heapSize && array[right].CompareTo(array[largest]) > 0)
            largest = right;

        if (largest != rootIndex)
        {
            Swap(array, rootIndex, largest);
            Heapify(array, heapSize, largest);
        }
    }

    // Вспомогательный метод для обмена элементов
    private static void Swap<T>(T[] array, int i, int j)
    {
        T temp = array[i];
        array[i] = array[j];
        array[j] = temp;
    }
}

/*
 * 🧪 Пример использования
 * 
 * class Program
 * {
 *     static void Main()
 *     {
 *         int[] arr = { 64, 34, 25, 12, 22, 11, 90 };
 * 
 *         Console.WriteLine("Исходный массив: " + string.Join(", ", arr));
 * 
 *         // Выберите любой метод:
 *         SortingAlgorithms.QuickSort(arr);
 *         // SortingAlgorithms.MergeSort(arr);
 *         // SortingAlgorithms.HeapSort(arr);
 *         // и т.д.
 * 
 *         Console.WriteLine("Отсортированный массив: " + string.Join(", ", arr));
 *     }
 * }
 */