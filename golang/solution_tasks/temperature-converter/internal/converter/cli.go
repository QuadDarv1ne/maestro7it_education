package converter

import (
	"flag"
	"fmt"
)

// ParseFlags обрабатывает флаги командной строки и возвращает параметры конвертации.
// Возвращает ошибку при отсутствии обязательных флагов.
func ParseFlags() (from TemperatureScale, to TemperatureScale, value float64, err error) {
	// Определение флагов
	fromFlag := flag.String("from", "", "Исходная шкала (C, F, K)")
	toFlag := flag.String("to", "", "Целевая шкала (C, F, K)")
	valueFlag := flag.Float64("value", 0, "Значение температуры")

	flag.Parse()

	// Проверка обязательных флагов
	if *fromFlag == "" || *toFlag == "" {
		flag.Usage()
		return "", "", 0, fmt.Errorf("флаги -from и -to обязательны")
	}

	// Приведение к TemperatureScale
	from = TemperatureScale(*fromFlag)
	to = TemperatureScale(*toFlag)
	value = *valueFlag

	return from, to, value, nil
}
