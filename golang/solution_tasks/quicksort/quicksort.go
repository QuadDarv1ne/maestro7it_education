/*
Пакет main сравнивает производительность параллельной 
и однопоточной версий алгоритма быстрой сортировки.
*/

package main

import (
	"fmt"
	"math/rand"
	"sync"
	"time"
)

func main() {
	data := make([]int, 1_000_000)
	for i := range data {
		data[i] = rand.Intn(1000)
	}

	// Параллельная сортировка
	start := time.Now()
	ParallelQuickSort(data)
	fmt.Printf("Parallel: %v\n", time.Since(start))

	// Однопоточная сортировка
	start = time.Now()
	QuickSort(data)
	fmt.Printf("Single: %v\n", time.Since(start))
}

// ParallelQuickSort реализует параллельную версию быстрой сортировки.
// При размере подмассива <= 1000 переключается на однопоточную сортировку.
func ParallelQuickSort(arr []int) {
	if len(arr) <= 1 {
		return
	}

	if len(arr) <= 1000 {
		QuickSort(arr)
		return
	}

	var wg sync.WaitGroup
	wg.Add(2)

	pivot := partition(arr)
	go func() {
		defer wg.Done()
		ParallelQuickSort(arr[:pivot])
	}()
	go func() {
		defer wg.Done()
		ParallelQuickSort(arr[pivot+1:])
	}()

	wg.Wait()
}

// QuickSort - классическая однопоточная реализация быстрой сортировки.
func QuickSort(arr []int) {
	if len(arr) <= 1 {
		return
	}
	pivot := partition(arr)
	QuickSort(arr[:pivot])
	QuickSort(arr[pivot+1:])
}

// partition разделяет массив на элементы меньше и больше опорного.
// Возвращает индекс опорного элемента.
func partition(arr []int) int {
	pivot := arr[len(arr)-1]
	i := 0
	for j := 0; j < len(arr); j++ {
		if arr[j] < pivot {
			arr[i], arr[j] = arr[j], arr[i]
			i++
		}
	}
	arr[i], arr[len(arr)-1] = arr[len(arr)-1], arr[i]
	return i
}