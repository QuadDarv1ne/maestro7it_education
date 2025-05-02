/*
Генератор QR-кодов с настройкой цветов и размеров.
*/

package main

import (
    "flag"
    "fmt"
    "image/color"
    "log"
    "os"

    "github.com/skip2/go-qrcode"
)

func main() {
    content := flag.String("content", "", "Текст/URL для кодирования")
    output := flag.String("output", "qrcode.png", "Путь для сохранения")
    size := flag.Int("size", 256, "Размер изображения (пиксели)")
    fgColor := flag.String("fg", "#000000", "Цвет QR-кода (HEX)")
    bgColor := flag.String("bg", "#FFFFFF", "Цвет фона (HEX)")
    flag.Parse()

    if *content == "" {
        fmt.Println("Ошибка: укажите текст/URL через -content")
        flag.Usage()
        os.Exit(1)
    }

    // Конвертация цветов из HEX в RGBA
    fg := parseHexColor(*fgColor)
    bg := parseHexColor(*bgColor)

    // Генерация QR-кода
    qr, err := qrcode.New(*content, qrcode.Highest)
    if err != nil {
        log.Fatal("Ошибка генерации:", err)
    }

    qr.ForegroundColor = fg
    qr.BackgroundColor = bg

    // Сохранение изображения
    err = qr.WriteFile(*size, *output)
    if err != nil {
        log.Fatal("Ошибка сохранения:", err)
    }

    fmt.Printf("✅ QR-код сохранён в: %s\n", *output)
}

// Конвертация HEX в color.RGBA
func parseHexColor(hex string) color.RGBA {
    var c color.RGBA
    _, err := fmt.Sscanf(hex, "#%02x%02x%02x", &c.R, &c.G, &c.B)
    if err != nil {
        log.Fatal("Неверный цвет:", hex)
    }
    c.A = 255
    return c
}