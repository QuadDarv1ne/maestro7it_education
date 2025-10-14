/**
 * 🎮 Улучшенная игра «Поиск сокровища» с документацией
 */

#include <iostream>
#include <limits>
#include <array>
#include <clocale>
#include <windows.h>  // Windows API для управления консолью

/**
 * @brief Константы игры.
 * 
 * MAP_SIZE — размер квадратной карты (10x10).
 * TREASURE_X, TREASURE_Y — координаты сокровища.
 * EMPTY_CELL — символ пустой клетки.
 * TREASURE_CELL — символ сокровища.
 * PLAYER_SYMBOL — символ игрока.
 */
constexpr int MAP_SIZE = 10;
constexpr int TREASURE_X = 7;
constexpr int TREASURE_Y = 7;
constexpr char EMPTY_CELL = '.';
constexpr char TREASURE_CELL = '#';
constexpr char PLAYER_SYMBOL = '+';

/// Тип данных для карты: двумерный массив символов фиксированного размера.
using Map = std::array<std::array<char, MAP_SIZE>, MAP_SIZE>;

/**
 * @brief Очищает консоль в зависимости от операционной системы.
 * 
 * Использует system("cls") в Windows и system("clear") в Unix-подобных системах.
 * Предупреждение: system() не рекомендуется в production-коде из соображений безопасности,
 * но допустим для учебных и консольных приложений.
 */
void clearScreen() {
#ifdef _WIN32
    std::system("cls");
#else
    std::system("clear");
#endif
}

/**
 * @brief Инициализирует игровую карту.
 * 
 * Заполняет всю карту символами EMPTY_CELL ('.'),
 * затем устанавливает сокровище в заданной позиции (TREASURE_Y, TREASURE_X).
 * 
 * @param map — ссылка на игровую карту, которую нужно инициализировать.
 */
void initMap(Map& map) {
    for (auto& row : map) {
        for (auto& cell : row) {
            cell = EMPTY_CELL;
        }
    }
    map[TREASURE_Y][TREASURE_X] = TREASURE_CELL;
}

/**
 * @brief Отображает текущее состояние карты в консоли.
 * 
 * На месте игрока рисуется PLAYER_SYMBOL ('+'),
 * остальные клетки отображаются как есть (пусто или сокровище).
 * 
 * @param map — константная ссылка на карту.
 * @param playerX — текущая координата игрока по оси X (столбец).
 * @param playerY — текущая координата игрока по оси Y (строка).
 */
void drawMap(const Map& map, int playerX, int playerY) {
    for (int i = 0; i < MAP_SIZE; ++i) {
        for (int j = 0; j < MAP_SIZE; ++j) {
            if (i == playerY && j == playerX) {
                std::cout << ' ' << PLAYER_SYMBOL;
            } else {
                std::cout << ' ' << map[i][j];
            }
        }
        std::cout << '\n';
    }
}

/**
 * @brief Проверяет, достиг ли игрок сокровища.
 * 
 * Сравнивает текущие координаты игрока с координатами сокровища.
 * 
 * @param x — координата игрока по X.
 * @param y — координата игрока по Y.
 * @return true, если игрок на клетке с сокровищем; иначе false.
 */
bool checkWin(int x, int y) {
    return (x == TREASURE_X && y == TREASURE_Y);
}

/**
 * @brief Запрашивает у пользователя действие и читает его из стандартного ввода.
 * 
 * Обрабатывает ошибки ввода (например, ввод букв вместо чисел).
 * В случае ошибки очищает поток и возвращает false.
 * 
 * @param action — ссылка на переменную, куда сохраняется введённое число.
 * @return true, если ввод успешен; false — при ошибке.
 */
bool getAction(int& action) {
    std::cout << "\nУправление:\n"
              << "1 - Вверх\n"
              << "2 - Вниз\n"
              << "3 - Влево\n"
              << "4 - Вправо\n"
              << "5 - Выйти\n"
              << "Ваш выбор: ";
    if (std::cin >> action) {
        return true;
    } else {
        std::cin.clear();
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        return false;
    }
}

/**
 * @brief Перемещает игрока в зависимости от выбранного действия.
 * 
 * Проверяет границы карты, чтобы игрок не вышел за пределы.
 * 
 * @param x — ссылка на координату игрока по X (изменяется при движении).
 * @param y — ссылка на координату игрока по Y (изменяется при движении).
 * @param action — выбранное действие (1–4).
 */
void movePlayer(int& x, int& y, int action) {
    switch (action) {
        case 1: // Вверх
            if (y > 0) y--;
            break;
        case 2: // Вниз
            if (y < MAP_SIZE - 1) y++;
            break;
        case 3: // Влево
            if (x > 0) x--;
            break;
        case 4: // Вправо
            if (x < MAP_SIZE - 1) x++;
            break;
        default:
            break; // Ничего не делаем для недопустимых действий
    }
}

/**
 * @brief Главная функция игры.
 * 
 * Инициализирует игру, запускает игровой цикл,
 * обрабатывает ввод, перемещение, проверку победы и вывод сообщений.
 * Поддерживает подсчёт ходов и корректный выход.
 */
int main() {
#ifdef _WIN32
    // Устанавливаем UTF-8 кодовую страницу для консоли Windows
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);
    // std::setlocale не требуется при использовании CP_UTF8
#endif

    Map map;
    initMap(map);

    int playerX = 3;
    int playerY = 5;
    int moves = 0;
    bool win = false;

    while (true) {
        clearScreen();
        drawMap(map, playerX, playerY);

        if (win) {
            std::cout << "\n🏆 Поздравляем! Вы нашли сокровище!\n";
            std::cout << "Совершено ходов: " << moves << "\n";
            break;
        }

        int action = -1;
        if (!getAction(action)) {
            std::cout << "\n❌ Ошибка ввода! Пожалуйста, введите число от 1 до 5.\n";
            std::cin.get();
            continue;
        }

        if (action < 1 || action > 5) {
            std::cout << "\n⚠️  Неверный выбор. Допустимые значения: 1–5.\n";
            std::cin.get();
            continue;
        }

        if (action == 5) {
            std::cout << "\n👋 До свидания! Спасибо за игру.\n";
            break;
        }

        movePlayer(playerX, playerY, action);
        moves++;
        win = checkWin(playerX, playerY);
    }

    return 0;
}