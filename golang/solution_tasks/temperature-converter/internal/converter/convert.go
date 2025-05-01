package converter

import (
	"fmt"
	"math"
)

// Convert конвертирует значение температуры между шкалами.
// Возвращает ошибку при некорректных входных данных или отрицательном Кельвине.
func Convert(from, to TemperatureScale, value float64) (float64, error) {
	// Валидация шкал
	if err := from.Validate(); err != nil {
		return 0, fmt.Errorf("некорректная исходная шкала: %v", err)
	}
	if err := to.Validate(); err != nil {
		return 0, fmt.Errorf("некорректная целевая шкала: %v", err)
	}

	// Конвертация через промежуточное значение в Цельсиях
	celsius := toCelsius(from, value)
	result := fromCelsius(to, celsius)

	// Проверка на отрицательный Кельвин
	if to == Kelvin && result < 0 {
		return 0, fmt.Errorf("кельвин не может быть отрицательным: %.2f", result)
	}

	// Округление до двух знаков
	return math.Round(result*100) / 100, nil
}

// toCelsius конвертирует значение из исходной шкалы в Цельсий.
func toCelsius(from TemperatureScale, value float64) float64 {
	switch from {
	case Fahrenheit:
		return (value - 32) * 5 / 9
	case Kelvin:
		return value - 273.15
	default:
		return value // Celsius
	}
}

// fromCelsius конвертирует значение из Цельсия в целевую шкалу.
func fromCelsius(to TemperatureScale, celsius float64) float64 {
	switch to {
	case Fahrenheit:
		return celsius*9/5 + 32
	case Kelvin:
		return celsius + 273.15
	default:
		return celsius // Celsius
	}
}
