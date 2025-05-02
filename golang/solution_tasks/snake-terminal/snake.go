/*
Терминальная змейка с рекордами и асинхронным управлением.
*/

package main

import (
    "fmt"
    "log"
    "os"
    "time"
    "strconv"
    "github.com/gdamore/tcell/v2"
    "crypto/rand"
    "math/big"
)

// Game — структура состояния игры
type Game struct {
    Screen    tcell.Screen
    Snake     [][2]int
    Food      [2]int
    Dir       string
    Score     int
    HighScore int
    Quit      bool
    Speed     time.Duration
}

const (
    InitialSpeed = 150 * time.Millisecond
    HighScoreFile = "highscores.txt"
)

func main() {
    // Инициализация экрана
    screen, err := tcell.NewScreen()
    if err != nil {
        log.Fatalf("Ошибка инициализации экрана: %v", err)
    }
    if err := screen.Init(); err != nil {
        log.Fatal(err)
    }
    defer screen.Fini()

    game := &Game{
        Screen:    screen,
        Snake:     [][2]int{{10, 10}, {9, 10}, {8, 10}},
        Dir:       "RIGHT",
        Speed:     InitialSpeed,
        HighScore: loadHighScore(),
    }
    game.spawnFood()

    // Запуск обработки ввода
    inputChan := make(chan string)
    go handleInput(screen, inputChan)

    // Игровой цикл
    for !game.Quit {
        game.update(inputChan)
        game.draw()
        time.Sleep(game.Speed)
    }

    // Сохранение рекорда
    if game.Score > game.HighScore {
        saveHighScore(game.Score)
    }
}

// Обработка ввода
func handleInput(screen tcell.Screen, ch chan<- string) {
    for {
        ev := screen.PollEvent()
        switch ev := ev.(type) {
        case *tcell.EventKey:
            switch ev.Key() {
            case tcell.KeyEscape:
                ch <- "QUIT"
            case tcell.KeyRune:
                switch ev.Rune() {
                case 'w', 'W':
                    ch <- "UP"
                case 's', 'S':
                    ch <- "DOWN"
                case 'a', 'A':
                    ch <- "LEFT"
                case 'd', 'D':
                    ch <- "RIGHT"
                }
            }
        }
    }
}

// Обновление состояния игры
func (g *Game) update(inputChan <-chan string) {
    select {
    case cmd := <-inputChan:
        switch cmd {
        case "QUIT":
            g.Quit = true
        case "UP", "DOWN", "LEFT", "RIGHT":
            if (g.Dir == "UP" && cmd != "DOWN") ||
               (g.Dir == "DOWN" && cmd != "UP") ||
               (g.Dir == "LEFT" && cmd != "RIGHT") ||
               (g.Dir == "RIGHT" && cmd != "LEFT") {
                g.Dir = cmd
            }
        }
    default:
    }

    // Движение змейки
    head := g.Snake[0]
    switch g.Dir {
    case "UP":
        head[1]--
    case "DOWN":
        head[1]++
    case "LEFT":
        head[0]--
    case "RIGHT":
        head[0]++
    }

    // Проверка столкновений
    if head[0] < 0 || head[0] >= 80 || 
       head[1] < 0 || head[1] >= 24 {
        g.Quit = true
        return
    }

    for _, seg := range g.Snake {
        if head[0] == seg[0] && head[1] == seg[1] {
            g.Quit = true
            return
        }
    }

    // Проверка еды
    if head[0] == g.Food[0] && head[1] == g.Food[1] {
        g.Score += 10
        g.Snake = append([][2]int{head}, g.Snake...)
        g.spawnFood()
        g.Speed = time.Duration(float64(g.Speed) * 0.95)
    } else {
        g.Snake = append([][2]int{head}, g.Snake[:len(g.Snake)-1]...)
    }
}

// Отрисовка игры
func (g *Game) draw() {
    g.Screen.Clear()
    style := tcell.StyleDefault.Foreground(tcell.ColorWhite)

    // Змейка
    for _, seg := range g.Snake {
        g.Screen.SetContent(seg[0], seg[1], '█', nil, style)
    }

    // Еда
    g.Screen.SetContent(g.Food[0], g.Food[1], '●', nil, style.Foreground(tcell.ColorRed))

    // Интерфейс
    info := fmt.Sprintf("Очки: %d | Рекорд: %d | Скорость: %.0f%%", 
        g.Score, g.HighScore, 100*(InitialSpeed.Seconds()/g.Speed.Seconds()))
    for i, ch := range info {
        g.Screen.SetContent(5+i, 0, ch, nil, style)
    }

    g.Screen.Show()
}

// Генерация еды
func (g *Game) spawnFood() {
    g.Food = [2]int{
        randInt(0, 79),
        randInt(0, 23),
    }
}

// Загрузка рекорда
func loadHighScore() int {
    if data, err := os.ReadFile(HighScoreFile); err == nil {
        if score, err := strconv.Atoi(string(data)); err == nil {
            return score
        }
    }
    return 0
}

// Сохранение рекорда
func saveHighScore(score int) {
    file, _ := os.Create(HighScoreFile)
    defer file.Close()
    file.WriteString(strconv.Itoa(score))
}

// Генератор случайных чисел
func randInt(min, max int) int {
    n, _ := rand.Int(rand.Reader, big.NewInt(int64(max-min+1)))
    return min + int(n.Int64())
}
