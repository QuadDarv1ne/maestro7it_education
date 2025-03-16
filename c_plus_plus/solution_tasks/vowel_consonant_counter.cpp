#include <iostream>
#include <string>
#include <clocale>       // Для работы с setlocale
#include <limits>        // Для numeric_limits
#include <algorithm>     // Для std::transform   
#include <unordered_set> 
#include <cwctype>       // Для iswalpha

#ifdef _WIN32
#include <windows.h>     // Для SetConsoleOutputCP (только Windows)
#endif

using namespace std;

/**
 * Константа с гласными для русского и английского языков.
 */
const unordered_set<wchar_t> VOWELS = {L'a', L'e', L'i', L'o', L'u', L'A', L'E', L'I', L'O', L'U',
                                       L'а', L'е', L'ё', L'и', L'о', L'у', L'ы', L'э', L'ю', L'я',
                                       L'А', L'Е', L'Ё', L'И', L'О', L'У', L'Ы', L'Э', L'Ю', L'Я'};

/**
 * Функция для подсчета количества гласных и согласных букв в строке.
 *
 * @param str Входная строка для анализа.
 * @param vowels Счетчик для гласных букв.
 * @param consonants Счетчик для согласных букв.
 */
void countLetters(const wstring &str, int &vowels, int &consonants) {
    vowels = 0;
    consonants = 0;

    for (wchar_t ch : str) {
        if (VOWELS.find(ch) != VOWELS.end()) {
            vowels++;
        } else if (iswalpha(ch)) {
            consonants++;
        }
    }
}

/**
 * Функция для очистки буфера ввода.
 */
void clearInputBuffer() {
    wcin.clear();
    wcin.ignore(numeric_limits<streamsize>::max(), '\n');
}

/**
 * Функция для вывода приглашения пользователю.
 */
void displayPrompt() {
    wcout << L"╔══════════════════════════════╗\n"
          << L"║   Введите текст для анализа: ║\n"
          << L"╚══════════════════════════════╝\n> ";
}

/**
 * Функция для вывода результатов анализа.
 *
 * @param vowels Количество гласных.
 * @param consonants Количество согласных.
 */
void displayResults(int vowels, int consonants) {
    wcout << L"\n════════ Результаты ═════════\n"
          << L"• Гласные: " << vowels << L"\n"
          << L"• Согласные: " << consonants << L"\n"
          << L"═════════════════════════════\n\n";
}

/**
 * Основная функция программы.
 */
int main() {
    // Настройка локали для UTF-8
    setlocale(LC_ALL, "ru_RU.UTF-8");

#ifdef _WIN32
    // Настройка консоли Windows для UTF-8
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);
#endif

    wstring choice = L"y";

    while (towlower(choice[0]) == L'y') {
        wstring input;
        displayPrompt();
        getline(wcin, input);

        int vowels = 0, consonants = 0;
        countLetters(input, vowels, consonants);
        displayResults(vowels, consonants);

        wcout << L"Продолжить? (y/n): ";
        getline(wcin, choice);
        clearInputBuffer();  // Очистка буфера ввода
        wcout << endl;
    }

    wcout << L"Программа завершена. Нажмите Enter...";
    clearInputBuffer();
    return 0;
}

/**
 * Функция для тестирования countLetters.
 */
void testCountLetters() {
    int vowels, consonants;

    countLetters(L"Hello World!", vowels, consonants);
    wcout << L"Test 1 - Vowels: " << vowels << L", Consonants: " << consonants << endl;

    countLetters(L"Привет мир!", vowels, consonants);
    wcout << L"Test 2 - Vowels: " << vowels << L", Consonants: " << consonants << endl;

    countLetters(L"123! @#", vowels, consonants);
    wcout << L"Test 3 - Vowels: " << vowels << L", Consonants: " << consonants << endl;

    // Дополнительные тесты
    countLetters(L"", vowels, consonants);
    wcout << L"Test 4 - Vowels: " << vowels << L", Consonants: " << consonants << endl;

    countLetters(L"AEIOUaeiouАЕЁИОУЫЭЮЯаеёиоуыэюя", vowels, consonants);
    wcout << L"Test 5 - Vowels: " << vowels << L", Consonants: " << consonants << endl;
}

/*
* Преподаватель: Дуплей Максим Игоревич
* Дата: 16.03.2025
*/
