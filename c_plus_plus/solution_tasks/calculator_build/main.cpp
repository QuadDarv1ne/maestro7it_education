#include <iostream>
#include <locale>
#include <clocale>
#include "calculator.h"

#ifdef _WIN32
#include <windows.h>
#endif

using namespace std;

/**
 * @brief Функция для настройки кодировки консоли
 * 
 * Настраивает консоль для корректного отображения UTF-8 символов
 * на разных операционных системах.
 */
void setupConsoleEncoding() {
    #ifdef _WIN32
    // Для Windows устанавливаем кодовую страницу UTF-8
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);
    #else
    // Для Linux используем более простой подход с локалями
    // Пробуем установить стандартную UTF-8 локаль
    try {
        std::locale::global(std::locale("C.UTF-8"));
    } catch (const std::exception& e) {
        try {
            // Альтернативный вариант для некоторых систем
            std::locale::global(std::locale("en_US.UTF-8"));
        } catch (const std::exception& e) {
            // Если не удалось установить локаль, продолжаем без нее
            std::cerr << "Предупреждение: не удалось установить локаль UTF-8: " 
                      << e.what() << std::endl;
        }
    }
    std::cout.imbue(std::locale());
    #endif
}

/**
 * @brief Основная функция калькулятора
 * 
 * Программа предоставляет консольный интерфейс для выполнения базовых
 * арифметических операций: сложения, вычитания, умножения и деления.
 * 
 * @return int Код возврата приложения (0 - успешное завершение)
 */
int main() {
    // Настройка кодировки консоли
    setupConsoleEncoding();
    
    Calculator calc;        ///< Экземпляр калькулятора
    double num_1, num_2;    ///< Операнды для вычислений
    char operation;         ///< Оператор для выбранной операции
        
    // Выбор операции
    cout << "Выберите операцию (+, -, *, /): ";
    cin >> operation;
    
    // Ввод первого операнда
    cout << "Введите первое число: ";
    cin >> num_1;

    // Ввод второго операнда
    cout << "Введите второе число: ";
    cin >> num_2;
    
    /**
     * @brief Блок выполнения операций с обработкой исключений
     * 
     * Выполняет выбранную арифметическую операцию через соответствующий
     * метод калькулятора. Обрабатывает исключение деления на ноль.
     */
    try {
        switch (operation) {
            case '+':
                /// Сложение двух чисел
                cout << "Результат: " << calc.add(num_1, num_2) << endl;
                break;
            case '-':
                /// Вычитание второго числа из первого
                cout << "Результат: " << calc.subtract(num_1, num_2) << endl;
                break;
            case '*':
                /// Умножение двух чисел
                cout << "Результат: " << calc.multiply(num_1, num_2) << endl;
                break;
            case '/':
                /**
                 * @brief Деление первого числа на второе
                 * @throws std::runtime_error при попытке деления на ноль
                 */
                cout << "Результат: " << calc.divide(num_1, num_2) << endl;
                break;
            default:
                /// Обработка неверного оператора
                cout << "Неверно выбран оператор" << endl;
                break;
        }
    } catch (const std::runtime_error& e) {
        /// Обработка исключений (в основном деления на ноль)
        cout << "Ошибка: " << e.what() << endl;
    }

    return 0;
}
