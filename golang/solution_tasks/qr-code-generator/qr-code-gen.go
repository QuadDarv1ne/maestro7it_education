/*
Генератор QR-кодов с настройкой цветов, размеров и закругленных углов.
*/

package main

import (
	"flag"
	"fmt"
	"image"
	"image/color"
	"image/draw"
	"image/png"
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
	radius := flag.Int("radius", 50, "Радиус закругленных углов")
	flag.Parse()

	if *content == "" {
		fmt.Println("Ошибка: укажите текст/URL через -content")
		flag.Usage()
		os.Exit(1)
	}

	// Конвертация цветов из HEX в RGBA
	fg := parseHexColor(*fgColor)
	bg := parseHexColor(*bgColor)

	// Генерация QR-кода и сохранение во временный файл
	tempFile, err := os.CreateTemp("", "temp-qrcode-*.png")
	if err != nil {
		log.Fatal("Ошибка создания временного файла:", err)
	}
	defer os.Remove(tempFile.Name()) // Удаление временного файла после использования

	err = qrcode.WriteColorFile(*content, qrcode.Highest, *size, fg, bg, tempFile.Name())
	if err != nil {
		log.Fatal("Ошибка генерации QR-кода:", err)
	}

	// Чтение временного файла
	tempImgFile, err := os.Open(tempFile.Name())
	if err != nil {
		log.Fatal("Ошибка открытия временного файла:", err)
	}
	defer tempImgFile.Close()

	tempImg, err := png.Decode(tempImgFile)
	if err != nil {
		log.Fatal("Ошибка декодирования временного файла:", err)
	}

	// Применение закругленных углов
	imgWithRoundedCorners := roundCorners(tempImg, *radius)

	// Сохранение изображения с закругленными углами
	outputFile, err := os.Create(*output)
	if err != nil {
		log.Fatal("Ошибка создания выходного файла:", err)
	}
	defer outputFile.Close()

	err = png.Encode(outputFile, imgWithRoundedCorners)
	if err != nil {
		log.Fatal("Ошибка сохранения изображения:", err)
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

// Применение закругленных углов к изображению
func roundCorners(img image.Image, radius int) *image.RGBA {
	bounds := img.Bounds()
	rounded := image.NewRGBA(bounds)
	draw.Draw(rounded, bounds, img, image.Point{}, draw.Src)

	for y := 0; y < bounds.Dy(); y++ {
		for x := 0; x < bounds.Dx(); x++ {
			if x < radius || y < radius || x >= bounds.Dx()-radius || y >= bounds.Dy()-radius {
				if !isInCircle(x, y, radius, bounds.Dx(), bounds.Dy()) {
					rounded.Set(x, y, color.Transparent)
				}
			}
		}
	}

	return rounded
}

// Проверка, находится ли пиксель внутри окружности
func isInCircle(x, y, radius, width, height int) bool {
	if x < radius && y < radius {
		return (x-radius)*(x-radius)+(y-radius)*(y-radius) <= radius*radius
	}
	if x >= width-radius && y < radius {
		return (x-(width-radius))*(x-(width-radius))+(y-radius)*(y-radius) <= radius*radius
	}
	if x < radius && y >= height-radius {
		return (x-radius)*(x-radius)+(y-(height-radius))*(y-(height-radius)) <= radius*radius
	}
	if x >= width-radius && y >= height-radius {
		return (x-(width-radius))*(x-(width-radius))+(y-(height-radius))*(y-(height-radius)) <= radius*radius
	}
	return true
}
