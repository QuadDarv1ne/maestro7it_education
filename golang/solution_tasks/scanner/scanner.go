/*
Пакет main реализует параллельный сканер портов.

Сканер принимает хост и диапазон портов, проверяет доступность TCP-портов 
с ограничением количества одновременных подключений.
*/

package main

import (
	"fmt"
	"net"
	"os"
	"strconv"
	"strings"
	"sync"
)

// main - точка входа. Обрабатывает аргументы командной строки, запускает сканирование.
func main() {
	if len(os.Args) != 3 {
		fmt.Println("Usage: go run scanner.go <host> <start-end>")
		return
	}

	host := os.Args[1]
	ports := strings.Split(os.Args[2], "-")
	start, _ := strconv.Atoi(ports[0])
	end, _ := strconv.Atoi(ports[1])

	var wg sync.WaitGroup
	sem := make(chan struct{}, 100) // Ограничение горутин
	results := make(chan string)

	// Сбор результатов
	go func() {
		for res := range results {
			fmt.Println(res)
		}
	}()

	for port := start; port <= end; port++ {
		wg.Add(1)
		sem <- struct{}{}
		go func(p int) {
			defer wg.Done()
			addr := fmt.Sprintf("%s:%d", host, p)
			conn, err := net.Dial("tcp", addr)
			if err == nil {
				conn.Close()
				results <- fmt.Sprintf("[OPEN] %s", addr)
			}
			<-sem
		}(port)
	}

	wg.Wait()
	close(results)
	close(sem)
}