/**
 * Решение задачи "Count Square Sum Triples" (LeetCode 1925)
 * 
 * @file count_square_sum_triples.go
 * @brief Подсчёт упорядоченных троек Пифагора в диапазоне [1, n]
 * 
 * @author Дулей Максим Игоревич
 * @see ORCID: https://orcid.org/0009-0007-7605-539X
 * @see GitHub: https://github.com/QuadDarv1ne/
 * 
 * @details
 * Алгоритм: Перебор всех пар (a, b) с проверкой через sqrt
 * Сложность: O(n²) времени, O(1) памяти
 * 
 * @approach
 * 1. Генерируем все пары (a, b) с помощью двойного цикла
 * 2. Для каждой пары вычисляем c = √(a² + b²)
 * 3. Проверяем, что c - целое число и не превышает n
 * 4. Считаем все подходящие тройки
 */

package main

import (
	"fmt"
	"math"
)

/**
 * Подсчитывает количество упорядоченных троек (a, b, c)
 * 
 * @param n Верхняя граница для значений a, b, c (1 ≤ n ≤ 250)
 * @return int Количество троек, удовлетворяющих условию a² + b² = c²
 * 
 * @example
 * result := countTriples(5)   // возвращает 2
 * result := countTriples(10)  // возвращает 4
 * 
 * @note
 * - Учитываются упорядоченные тройки: (3,4,5) и (4,3,5) - разные
 * - Используется математическая библиотека для вычисления sqrt
 * - Проверка целочисленности: c*c == a*a + b*b
 */
func countTriples(n int) int {
	count := 0

	// Перебираем все возможные значения a и b
	for a := 1; a <= n; a++ {
		for b := 1; b <= n; b++ {
			cSq := a*a + b*b
			c := int(math.Sqrt(float64(cSq)))

			// Проверяем условия Пифагоровой тройки
			if c <= n && c*c == cSq {
				count++
			}
		}
	}

	return count
}

/**
 * Оптимизированная версия с предварительным вычислением квадратов
 * 
 * @param n Верхняя граница диапазона
 * @return int Количество троек
 * 
 * @complexity
 * - Время: O(n²)
 * - Память: O(n²) для хранения карты квадратов
 */
func countTriplesOptimized(n int) int {
	// Создаём карту для быстрой проверки квадратов
	squares := make(map[int]bool)
	for i := 1; i <= n; i++ {
		squares[i*i] = true
	}

	count := 0
	maxSquare := n * n

	// Перебираем все пары квадратов
	for aSq := range squares {
		for bSq := range squares {
			sum := aSq + bSq
			if sum <= maxSquare && squares[sum] {
				count++
			}
		}
	}

	return count
}

/**
 * Версия с использованием массива вместо карты
 * Более эффективна по памяти для небольших n
 */
func countTriplesArray(n int) int {
	maxSquare := n * n
	isPerfectSquare := make([]bool, maxSquare+1)

	// Отмечаем все совершенные квадраты
	for i := 1; i <= n; i++ {
		isPerfectSquare[i*i] = true
	}

	count := 0

	// Перебираем все пары (a, b)
	for a := 1; a <= n; a++ {
		aSq := a * a
		for b := 1; b <= n; b++ {
			sum := aSq + b*b
			if sum <= maxSquare && isPerfectSquare[sum] {
				count++
			}
		}
	}

	return count
}

/**
 * Конкурентная версия для больших n
 * Использует горутины для параллельных вычислений
 */
func countTriplesConcurrent(n int) int {
	var count int32
	var wg sync.WaitGroup

	// Обрабатываем каждое a в отдельной горутине
	for a := 1; a <= n; a++ {
		wg.Add(1)
		go func(a int) {
			defer wg.Done()
			localCount := 0
			aSq := a * a

			for b := 1; b <= n; b++ {
				cSq := aSq + b*b
				c := int(math.Sqrt(float64(cSq)))
				if c <= n && c*c == cSq {
					localCount++
				}
			}

			atomic.AddInt32(&count, int32(localCount))
		}(a)
	}

	wg.Wait()
	return int(count)
}