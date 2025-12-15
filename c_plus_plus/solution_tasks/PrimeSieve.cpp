/**
 * Преподаватель: Дуплей Максим Игоревич
 * Студент: Каплин Кирилл Витальевич
 */

#include <iostream>
#include <vector>
#include <cmath>

/**
 * @brief Находит все простые числа до n используя алгоритм "Решето Эратосфена"
 * 
 * Алгоритм работает путём последовательного исключения составных чисел.
 * Для каждого простого числа p вычёркиваются все его кратные, начиная с p².
 * 
 * @param n Верхняя граница диапазона поиска (включительно)
 * @return std::vector<int> Вектор всех простых чисел от 2 до n
 * 
 * @note Временная сложность: O(n log log n)
 * @note Пространственная сложность: O(n)
 * 
 * @example
 * auto primes = sieveOfEratosthenes(10);
 * // Вернёт: {2, 3, 5, 7}
 */
std::vector<int> sieveOfEratosthenes(int n) {
    if (n < 2) return {};
    
    // Массив для отметки составных чисел
    std::vector<bool> isPrime(n + 1, true);
    isPrime[0] = isPrime[1] = false;
    
    // Достаточно проверить до √n
    int sqrtN = sqrt(n);
    for (int i = 2; i <= sqrtN; ++i) {
        if (isPrime[i]) {
            // Вычёркиваем кратные числа, начиная с i²
            for (int j = i * i; j <= n; j += i) {
                isPrime[j] = false;
            }
        }
    }
    
    // Собираем результат
    std::vector<int> primes;
    primes.reserve(n / log(n) * 1.3); // Приближённая оценка по теореме о простых числах
    
    for (int i = 2; i <= n; ++i) {
        if (isPrime[i]) {
            primes.push_back(i);
        }
    }
    
    return primes;
}

/**
 * @brief Точка входа в программу
 * 
 * Запрашивает у пользователя число N и выводит все простые числа до N.
 */
int main() {
    int n;
    std::cout << "Введите N: ";
    std::cin >> n;
    
    auto primes = sieveOfEratosthenes(n);
    
    std::cout << "Найдено " << primes.size() << " простых чисел:\n";
    for (int p : primes) {
        std::cout << p << " ";
    }
    std::cout << "\n";
    
    return 0;
}