package converter

import "fmt"

// TemperatureScale представляет поддерживаемую шкалу температуры.
type TemperatureScale string

const (
	Celsius    TemperatureScale = "C"
	Fahrenheit TemperatureScale = "F"
	Kelvin     TemperatureScale = "K"
)

// Validate проверяет, что шкала соответствует одной из поддерживаемых (C, F, K).
func (ts TemperatureScale) Validate() error {
	switch ts {
	case Celsius, Fahrenheit, Kelvin:
		return nil
	default:
		return fmt.Errorf("неподдерживаемая шкала: %s", ts)
	}
}
