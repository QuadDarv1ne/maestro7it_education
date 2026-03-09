/*
Пакет main предоставляет консольного клиента для API OpenWeatherMap 
с кэшированием результатов в файл.
*/

package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"io"
	"net/http"
	"os"
	"time"
)

// WeatherData структура для парсинга JSON-ответа от API.
type WeatherData struct {
	Main struct {
		Temp     float64 `json:"temp"`
		Humidity int     `json:"humidity"`
	} `json:"main"`
	Weather []struct {
		Description string `json:"description"`
	} `json:"weather"`
}

const (
	CacheTTL = 10 * time.Minute
)

// main обрабатывает аргументы, проверяет кэш и делает запрос к API.
func main() {
	cityPtr := flag.String("city", "London", "City name")
	apiKey := flag.String("api-key", "", "OpenWeatherMap API key (or set WEATHER_API_KEY env var)")
	flag.Parse()

	// Получение API ключа
	key := *apiKey
	if key == "" {
		key = os.Getenv("WEATHER_API_KEY")
	}
	if key == "" || key == "YOUR_API_KEY" {
		fmt.Println("Error: API key required. Use -api-key or set WEATHER_API_KEY environment variable.")
		fmt.Println("Get free key at: https://openweathermap.org/api")
		os.Exit(1)
	}

	cacheFile := ".weather_cache.json"
	if cached := readCache(cacheFile, *cityPtr); cached != "" {
		fmt.Println("(cached)", cached)
		return
	}

	url := fmt.Sprintf("https://api.openweathermap.org/data/2.5/weather?q=%s&appid=%s&units=metric", *cityPtr, key)
	resp, err := http.Get(url)
	if err != nil {
		fmt.Printf("Error fetching data: %v\n", err)
		os.Exit(1)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		fmt.Printf("API error: %s\n", resp.Status)
		os.Exit(1)
	}

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		fmt.Printf("Error reading response: %v\n", err)
		os.Exit(1)
	}

	var data WeatherData
	if err := json.Unmarshal(body, &data); err != nil {
		fmt.Printf("Error parsing JSON: %v\n", err)
		os.Exit(1)
	}

	if len(data.Weather) == 0 {
		fmt.Println("Error: no weather data available")
		os.Exit(1)
	}

	fmt.Printf("Температура: %.1f°C, Влажность: %d%%, Описание: %s\n",
		data.Main.Temp, data.Main.Humidity, data.Weather[0].Description)

	saveCache(cacheFile, *cityPtr, string(body))
}

// readCache читает закэшированные данные из файла, если они актуальны.
// Возвращает отформатированную строку или пустую строку если кэш устарел.
func readCache(file, city string) string {
	info, err := os.Stat(file)
	if err != nil || time.Since(info.ModTime()) > CacheTTL {
		return ""
	}

	data, err := os.ReadFile(file)
	if err != nil {
		return ""
	}

	var cached WeatherData
	if err := json.Unmarshal(data, &cached); err != nil {
		return ""
	}

	if len(cached.Weather) == 0 {
		return ""
	}

	return fmt.Sprintf("Температура: %.1f°C, Влажность: %d%%, Описание: %s",
		cached.Main.Temp, cached.Main.Humidity, cached.Weather[0].Description)
}

// saveCache сохраняет данные в файл кэша.
func saveCache(file, city, data string) {
	os.WriteFile(file, []byte(data), 0644)
}