package main

import (
	"fmt"
	"os"

	"github.com/your-username/temperature-converter/internal/converter"
)

func main() {
	// Получение параметров из CLI
	from, to, value, err := converter.ParseFlags()
	if err != nil {
		fmt.Printf("Ошибка: %v\n", err)
		os.Exit(1)
	}

	// Конвертация температуры
	result, err := converter.Convert(from, to, value)
	if err != nil {
		fmt.Printf("Ошибка: %v\n", err)
		os.Exit(1)
	}

	// Вывод результата
	fmt.Printf("%.2f°%s\n", result, to)
}
