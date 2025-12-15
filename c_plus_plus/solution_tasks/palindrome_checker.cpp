/**
 * Преподаватель: Дуплей Максим Игоревич
 * Студент: Каплин Кирилл Витальевич
 */

#include <iostream>
#include <string>
#include <algorithm>
#include <cctype>

/**
 * @brief Проверяет, является ли символ буквой или цифрой
 * 
 * @param c Символ для проверки
 * @return true Если символ - буква или цифра
 * @return false В противном случае
 */
bool isAlphanumeric(char c) {
    return std::isalnum(static_cast<unsigned char>(c));
}

/**
 * @brief Преобразует символ в нижний регистр
 * 
 * @param c Символ для преобразования
 * @return char Символ в нижнем регистре
 */
char toLowerCase(char c) {
    return std::tolower(static_cast<unsigned char>(c));
}

/**
 * @brief Проверяет, является ли строка палиндромом
 * 
 * Функция игнорирует пробелы, знаки препинания и регистр букв.
 * Учитываются только буквы и цифры.
 * 
 * @param str Строка для проверки
 * @return true Если строка является палиндромом
 * @return false Если строка не является палиндромом
 * 
 * @note Временная сложность: O(n)
 * @note Пространственная сложность: O(1)
 * 
 * @example
 * isPalindrome("A man, a plan, a canal: Panama"); // true
 * isPalindrome("race a car"); // false
 */
bool isPalindrome(const std::string& str) {
    int left = 0;
    int right = str.length() - 1;
    
    while (left < right) {
        // Пропускаем не-алфавитно-цифровые символы слева
        while (left < right && !isAlphanumeric(str[left])) {
            ++left;
        }
        
        // Пропускаем не-алфавитно-цифровые символы справа
        while (left < right && !isAlphanumeric(str[right])) {
            --right;
        }
        
        // Сравниваем символы без учёта регистра
        if (toLowerCase(str[left]) != toLowerCase(str[right])) {
            return false;
        }
        
        ++left;
        --right;
    }
    
    return true;
}

/**
 * @brief Альтернативная реализация с предварительной очисткой строки
 * 
 * @param str Строка для проверки
 * @return true Если строка является палиндромом
 * @return false Если строка не является палиндромом
 * 
 * @note Временная сложность: O(n)
 * @note Пространственная сложность: O(n)
 */
bool isPalindromeClean(const std::string& str) {
    std::string cleaned;
    cleaned.reserve(str.length());
    
    // Оставляем только буквы и цифры в нижнем регистре
    for (char c : str) {
        if (isAlphanumeric(c)) {
            cleaned += toLowerCase(c);
        }
    }
    
    // Проверяем, равна ли строка своей обратной копии
    int left = 0;
    int right = cleaned.length() - 1;
    
    while (left < right) {
        if (cleaned[left] != cleaned[right]) {
            return false;
        }
        ++left;
        --right;
    }
    
    return true;
}

/**
 * @brief Точка входа в программу
 * 
 * Демонстрирует работу функции проверки палиндрома на различных примерах.
 */
int main() {
    std::string input;
    
    std::cout << "=== ПРОВЕРКА ПАЛИНДРОМОВ ===\n\n";
    std::cout << "Введите строку для проверки: ";
    std::getline(std::cin, input);
    
    bool result = isPalindrome(input);
    
    std::cout << "\nРезультат: \"" << input << "\" ";
    std::cout << (result ? "ЯВЛЯЕТСЯ" : "НЕ ЯВЛЯЕТСЯ") << " палиндромом\n";
    
    // Тестовые примеры
    std::cout << "\n=== ТЕСТОВЫЕ ПРИМЕРЫ ===\n";
    
    std::string testCases[] = {
        "A man, a plan, a canal: Panama",
        "race a car",
        "Was it a car or a cat I saw?",
        "Madam",
        "12321",
        "hello",
        "A Santa at NASA",
        "No 'x' in Nixon",
        ""
    };
    
    for (const auto& test : testCases) {
        bool isPalin = isPalindrome(test);
        std::cout << std::boolalpha;
        std::cout << "\"" << test << "\" -> " << isPalin << "\n";
    }
    
    return 0;
}