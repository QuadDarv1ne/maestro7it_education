#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <locale>
#include <Windows.h>
#include <sstream>

using namespace std;

// Функция для конвертации string (Windows-1251) в wstring
wstring stringToWstring(const string& str) {
    if (str.empty()) return wstring();
    int size_needed = MultiByteToWideChar(1251, 0, str.c_str(), (int)str.size(), NULL, 0);
    wstring wstr(size_needed, 0);
    MultiByteToWideChar(1251, 0, str.c_str(), (int)str.size(), &wstr[0], size_needed);
    return wstr;
}

// Функция для конвертации wstring в string (Windows-1251)
string wstringToString(const wstring& wstr) {
    if (wstr.empty()) return string();
    int size_needed = WideCharToMultiByte(1251, 0, wstr.c_str(), (int)wstr.size(), NULL, 0, NULL, NULL);
    string str(size_needed, 0);
    WideCharToMultiByte(1251, 0, wstr.c_str(), (int)wstr.size(), &str[0], size_needed, NULL, NULL);
    return str;
}

// Функция для приведения символа к нижнему регистру
wchar_t toLowerRus(wchar_t ch) {
    // Английские буквы
    if (ch >= L'A' && ch <= L'Z') {
        return wchar_t(ch + 32);
    }
    // Русские буквы (А-Я)
    else if (ch >= L'А' && ch <= L'Я') {
        return wchar_t(ch + 32);
    }
    // Буква Ё
    else if (ch == L'Ё') {
        return L'ё';
    }
    return ch;
}

// Функция для приведения символа к верхнему регистру
wchar_t toUpperRus(wchar_t ch) {
    // Английские буквы
    if (ch >= L'a' && ch <= L'z') {
        return wchar_t(ch - 32);
    }
    // Русские буквы (а-я)
    else if (ch >= L'а' && ch <= L'я') {
        return wchar_t(ch - 32);
    }
    // Буква ё
    else if (ch == L'ё') {
        return L'Ё';
    }
    return ch;
}

// Функция для выравнивания капитализации (первая буква заглавная, остальные строчные)
wstring normalizeCapitalization(wstring word) {
    if (word.empty()) return word;
    
    wstring result;
    result += toUpperRus(word[0]); // Первая буква заглавная
    
    for (int i = 1; i < word.length(); i++) {
        result += toLowerRus(word[i]); // Остальные строчные
    }
    
    return result;
}

// Проверка, является ли символ гласной буквой
bool isVowel(wchar_t ch) {
    wchar_t lower = toLowerRus(ch);
    
    // Русские гласные
    wstring russianVowels = L"аеёиоуыэюя";
    // Английские гласные
    wstring englishVowels = L"aeiou";
    
    for (wchar_t vowel : russianVowels) {
        if (lower == vowel) return true;
    }
    
    for (wchar_t vowel : englishVowels) {
        if (lower == vowel) return true;
    }
    
    return false;
}

int main()
{
    // Настройка кодировки для Windows
    SetConsoleCP(1251);
    SetConsoleOutputCP(1251);
    setlocale(LC_ALL, "Russian");

    // Показываем текущую директорию
    char currentPath[MAX_PATH];
    GetCurrentDirectoryA(MAX_PATH, currentPath);
    cout << "Текущая рабочая директория: " << currentPath << endl << endl;

    // Имена файлов
    string inputFileName = "input.txt";
    string outputFileName = "output.txt";

    // Открытие входного файла для чтения (обычный ifstream)
    ifstream inputFile(inputFileName);
    
    if (!inputFile.is_open()) {
        wcout << L"Ошибка: не удалось открыть файл input.txt" << endl;
        wcout << L"Создаю файл с примером данных..." << endl;
        
        // Создание примера входного файла с явной кодировкой
        ofstream createFile(inputFileName);
        if (createFile.is_open()) {
            // Записываем в ANSI (Windows-1251)
            createFile << "яНВарь ФевРАль МАРТ АпРЕЛЬ маЙ ИЮнь июЛЬ авГУСТ СЕнТЯбРь ОКТЯБРЬ ноябрь дЕкАбРь";
            createFile.close();
            wcout << L"Файл input.txt создан в папке: " << currentPath << endl;
            wcout << L"Запустите программу снова." << endl;
        } else {
            wcout << L"Не удалось создать файл!" << endl;
        }
        
        system("pause");
        return 1;
    }

    // Чтение всей строки из файла (как обычная string)
    string line;
    getline(inputFile, line);
    inputFile.close();

    // Конвертируем в wstring для работы с кириллицей
    wstring wline = stringToWstring(line);

    wcout << L"Прочитано из файла:" << endl;
    wcout << wline << endl << endl;

    // Разбиение строки на слова
    vector<wstring> words;
    wstring word;
    wstringstream ss(wline);
    
    while (ss >> word) {
        words.push_back(word);
    }

    wcout << L"Всего слов найдено: " << words.size() << endl << endl;

    // Разделение слов на гласные и согласные
    vector<wstring> vowelWords;
    vector<wstring> consonantWords;

    for (const wstring& w : words) {
        if (!w.empty()) {
            wstring normalized = normalizeCapitalization(w);
            
            if (isVowel(normalized[0])) {
                vowelWords.push_back(normalized);
            } else {
                consonantWords.push_back(normalized);
            }
        }
    }

    // Запись в выходной файл
    ofstream outputFile(outputFileName);
    
    if (!outputFile.is_open()) {
        wcout << L"Ошибка: не удалось создать файл " << outputFileName.c_str() << endl;
        return 1;
    }

    // Запись слов, начинающихся с гласных
    outputFile << "Слова, начинающиеся с гласных:" << endl;
    for (int i = 0; i < vowelWords.size(); i++) {
        outputFile << wstringToString(vowelWords[i]);
        if (i < vowelWords.size() - 1) {
            outputFile << ", ";
        }
    }
    outputFile << endl;

    // Запись слов, начинающихся с согласных
    outputFile << "Слова, начинающиеся с согласных:" << endl;
    for (int i = 0; i < consonantWords.size(); i++) {
        outputFile << wstringToString(consonantWords[i]);
        if (i < consonantWords.size() - 1) {
            outputFile << ", ";
        }
    }
    outputFile << endl;

    outputFile.close();

    // Вывод результата в консоль
    wcout << L"Слова, начинающиеся с гласных:" << endl;
    for (int i = 0; i < vowelWords.size(); i++) {
        wcout << vowelWords[i];
        if (i < vowelWords.size() - 1) {
            wcout << L", ";
        }
    }
    wcout << endl << endl;

    wcout << L"Слова, начинающиеся с согласных:" << endl;
    for (int i = 0; i < consonantWords.size(); i++) {
        wcout << consonantWords[i];
        if (i < consonantWords.size() - 1) {
            wcout << L", ";
        }
    }
    wcout << endl << endl;

    wcout << L"Результат записан в файл output.txt" << endl;
    wcout << L"Путь к файлу: " << currentPath << "\\" << outputFileName.c_str() << endl << endl;

    // Проверяем, что записалось в файл
    wcout << L"Содержимое output.txt:" << endl;
    wcout << L"----------------------------------------" << endl;
    ifstream checkFile(outputFileName);
    string fileLine;
    while (getline(checkFile, fileLine)) {
        wcout << stringToWstring(fileLine) << endl;
    }
    checkFile.close();
    wcout << L"----------------------------------------" << endl << endl;

    system("pause");
    return 0;
}