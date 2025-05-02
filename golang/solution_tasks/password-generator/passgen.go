/*
Генератор безопасных паролей с поддержкой TOML-конфигов.
Позволяет создавать пароли для сервисов, API-ключей и систем аутентификации.
*/

package main

import (
	"crypto/rand"
	"flag"
	"fmt"
	"log"
	"math/big"
	"os"
	"strings"

	"github.com/BurntSushi/toml"
)

// Config — структура для парсинга TOML-конфига
type Config struct {
	Length   int    `toml:"length"`
	Upper    bool   `toml:"upper"`
	Lower    bool   `toml:"lower"`
	Numbers  bool   `toml:"numbers"`
	Symbols  bool   `toml:"symbols"`
	Exclude  string `toml:"exclude"`
	Output   string `toml:"output"`
}

const (
	upperChars  = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	lowerChars  = "abcdefghijklmnopqrstuvwxyz"
	numberChars = "0123456789"
	symbolChars = "!@#$%^&*()-_=+[]{}<>?"
)

var (
	configFile = flag.String("config", "", "Путь к TOML-конфигу (например, config.toml)")
	length     = flag.Int("length", 12, "Длина пароля")
	upper      = flag.Bool("upper", true, "Включать заглавные буквы")
	lower      = flag.Bool("lower", true, "Включать строчные буквы")
	numbers    = flag.Bool("numbers", true, "Включать цифры")
	symbols    = flag.Bool("symbols", false, "Включать спецсимволы")
	exclude    = flag.String("exclude", "0OoIl", "Исключаемые символы")
	output     = flag.String("output", "", "Куда сохранить пароль (например, secret.txt)")
)

func main() {
	flag.Parse()
	cfg := loadConfig()

	password, err := generatePassword(cfg)
	if err != nil {
		log.Fatalf("Ошибка генерации: %v", err)
	}

	if cfg.Output != "" {
		if err := os.WriteFile(cfg.Output, []byte(password), 0600); err != nil {
			log.Fatalf("Ошибка записи: %v", err)
		}
		fmt.Printf("🔑 Пароль сохранён в: %s\n", cfg.Output)
	} else {
		fmt.Printf("🔒 Сгенерированный пароль: %s\n", password)
	}
}

// Загрузка конфига из файла или флагов
func loadConfig() Config {
	if *configFile != "" {
		var cfg Config
		data, err := os.ReadFile(*configFile)
		if err != nil {
			log.Fatal("Ошибка чтения конфига:", err)
		}
		if _, err := toml.Decode(string(data), &cfg); err != nil {
			log.Fatal("Ошибка разбора TOML:", err)
		}
		return cfg
	}

	return Config{
		Length:   *length,
		Upper:    *upper,
		Lower:    *lower,
		Numbers:  *numbers,
		Symbols:  *symbols,
		Exclude:  *exclude,
		Output:   *output,
	}
}

// Генерация пароля с учётом настроек
func generatePassword(cfg Config) (string, error) {
	var builder strings.Builder

	if cfg.Upper {
		builder.WriteString(filterChars(upperChars, cfg.Exclude))
	}
	if cfg.Lower {
		builder.WriteString(filterChars(lowerChars, cfg.Exclude))
	}
	if cfg.Numbers {
		builder.WriteString(filterChars(numberChars, cfg.Exclude))
	}
	if cfg.Symbols {
		builder.WriteString(filterChars(symbolChars, cfg.Exclude))
	}

	charset := builder.String()
	if charset == "" {
		return "", fmt.Errorf("не выбрано ни одного набора символов")
	}

	password := make([]byte, cfg.Length)
	max := big.NewInt(int64(len(charset)))

	for i := range password {
		num, err := rand.Int(rand.Reader, max)
		if err != nil {
			return "", err
		}
		password[i] = charset[num.Int64()]
	}

	return string(password), nil
}

// Фильтрация нежелательных символов
func filterChars(chars, exclude string) string {
	return strings.Map(func(r rune) rune {
		if strings.ContainsRune(exclude, r) {
			return -1
		}
		return r
	}, chars)
}