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
	APIKey  = "YOUR_API_KEY"  // Замените на свой ключ
	CacheTTL = 10 * time.Minute
)

// main обрабатывает аргументы, проверяет кэш и делает запрос к API.
func main() {
	cityPtr := flag.String("city", "London", "City name")
	flag.Parse()

	cacheFile := ".weather_cache.json"
	if cached := readCache(cacheFile, *cityPtr); cached != nil {
		fmt.Println("(cached)", cached)
		return
	}

	url := fmt.Sprintf("https://api.openweathermap.org/data/2.5/weather?q=%s&appid=%s&units=metric", *cityPtr, APIKey)
	resp, _ := http.Get(url)
	defer resp.Body.Close()

	body, _ := io.ReadAll(resp.Body)
	var data WeatherData
	json.Unmarshal(body, &data)

	fmt.Printf("Температура: %.1f°C, Влажность: %d%%, Описание: %s\n",
		data.Main.Temp, data.Main.Humidity, data.Weather[0].Description)
	
	saveCache(cacheFile, *cityPtr, string(body))
}

// readCache читает закэшированные данные из файла, если они актуальны.
// Возвращает данные или nil, если кэш устарел.
func readCache(file, city string) string {
	info, err := os.Stat(file)
	if err != nil || time.Since(info.ModTime()) > CacheTTL {
		return nil
	}
	// ... парсинг кэша
	return nil
}

// saveCache сохраняет данные в файл кэша.
func saveCache(file, city, data string) {
	os.WriteFile(file, []byte(data), 0644)
}