/**
 * Преподаватель: Дуплей Максим Игоревич
 * Студент: Каплин Кирилл Витальевич
 */

#include <iostream>
#include <chrono>
#include <iomanip>

/**
 * @brief Вычисляет факториал числа рекурсивно
 * 
 * @param n Число для вычисления факториала
 * @return unsigned long long Факториал числа n
 * 
 * @note Временная сложность: O(n)
 * @note Пространственная сложность: O(n) из-за стека вызовов
 * @warning Может вызвать переполнение стека для больших n
 */
unsigned long long factorialRecursive(int n) {
    if (n <= 1) return 1;
    return n * factorialRecursive(n - 1);
}

/**
 * @brief Вычисляет факториал числа итеративно
 * 
 * @param n Число для вычисления факториала
 * @return unsigned long long Факториал числа n
 * 
 * @note Временная сложность: O(n)
 * @note Пространственная сложность: O(1)
 */
unsigned long long factorialIterative(int n) {
    unsigned long long result = 1;
    for (int i = 2; i <= n; ++i) {
        result *= i;
    }
    return result;
}

/**
 * @brief Измеряет время выполнения функции
 * 
 * @tparam Func Тип функции
 * @param func Функция для измерения
 * @param n Аргумент функции
 * @param iterations Количество итераций для усреднения
 * @return double Среднее время выполнения в микросекундах
 */
template<typename Func>
double measureTime(Func func, int n, int iterations = 10000) {
    auto start = std::chrono::high_resolution_clock::now();
    
    for (int i = 0; i < iterations; ++i) {
        func(n);
    }
    
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    
    return duration.count() / static_cast<double>(iterations);
}

/**
 * @brief Точка входа в программу
 * 
 * Демонстрирует работу рекурсивной и итеративной версий вычисления факториала
 * и сравнивает их производительность.
 */
int main() {
    int n;
    std::cout << "Введите число для вычисления факториала: ";
    std::cin >> n;
    
    if (n < 0) {
        std::cout << "Факториал не определён для отрицательных чисел\n";
        return 1;
    }
    
    if (n > 20) {
        std::cout << "Предупреждение: для n > 20 возможно переполнение!\n";
    }
    
    // Вычисление результатов
    unsigned long long resultRecursive = factorialRecursive(n);
    unsigned long long resultIterative = factorialIterative(n);
    
    std::cout << "\n=== РЕЗУЛЬТАТЫ ===\n";
    std::cout << "Рекурсивный метод: " << n << "! = " << resultRecursive << "\n";
    std::cout << "Итеративный метод: " << n << "! = " << resultIterative << "\n";
    
    // Сравнение производительности
    std::cout << "\n=== СРАВНЕНИЕ ПРОИЗВОДИТЕЛЬНОСТИ ===\n";
    std::cout << std::fixed << std::setprecision(3);
    
    double timeRecursive = measureTime(factorialRecursive, n);
    double timeIterative = measureTime(factorialIterative, n);
    
    std::cout << "Рекурсивный метод: " << timeRecursive << " мкс\n";
    std::cout << "Итеративный метод: " << timeIterative << " мкс\n";
    
    double speedup = timeRecursive / timeIterative;
    std::cout << "\nИтеративный метод быстрее в " << speedup << " раз\n";
    
    // Дополнительное тестирование для разных значений
    std::cout << "\n=== ТЕСТИРОВАНИЕ ДЛЯ РАЗНЫХ ЗНАЧЕНИЙ ===\n";
    std::cout << std::setw(5) << "n" 
              << std::setw(15) << "Рекурсия (мкс)" 
              << std::setw(15) << "Итерация (мкс)" 
              << std::setw(12) << "Ускорение\n";
    std::cout << std::string(47, '-') << "\n";
    
    for (int testN : {5, 10, 15, 20}) {
        double timeRec = measureTime(factorialRecursive, testN);
        double timeIter = measureTime(factorialIterative, testN);
        
        std::cout << std::setw(5) << testN
                  << std::setw(15) << timeRec
                  << std::setw(15) << timeIter
                  << std::setw(12) << (timeRec / timeIter) << "x\n";
    }
    
    return 0;
}