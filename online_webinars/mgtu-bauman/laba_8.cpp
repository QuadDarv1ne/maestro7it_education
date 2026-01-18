/**
 * @file laba_8.cpp
 * @brief Лабораторная работа 8 - Работа с файлами и строками
 * @details Программа выполняет следующие операции:
 *          - Создает файл с днями недели в смешанном регистре
 *          - Форматирует названия дней (первая буква заглавная, остальные строчные)
 *          - Разделяет дни на выходные и будние
 *          - Записывает отсортированный результат в выходной файл
 * @author Студент
 * @date 2026
 */

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
using namespace std;

/**
 * @brief Главная функция программы
 * @return 0 при успешном завершении
 * @details Алгоритм работы:
 *          1. Создает файл record.txt с днями недели в неправильном регистре
 *          2. Читает файл и форматирует каждое слово (Capitalize)
 *          3. Разделяет дни на выходные (Saturday, Sunday) и будние
 *          4. Записывает отформатированные дни в output.txt
 *          5. Выводит результат на консоль
 */
int main()
{
    cout << "Laboratornaya 8" << endl;
    
    // Создание входного файла
    ofstream record("record.txt");
    record << "moNDay THuesDAY weDNeSdAy tHuRsdAY FRAIday satURday sundaY";
    record.close();
    
    // Открытие файлов для чтения и записи
    ifstream inputFile("record.txt");
    ofstream theend("output.txt");
    
    string high = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    string low = "abcdefghijklmnopqrstuvwxyz";
    vector<string> weekend;
    vector<string> budni;
    
    string word;
    
    // Чтение и обработка слов
    while (inputFile >> word) {
        // Форматирование: первая буква - заглавная, остальные - строчные
        for (int i = 0; i < word.size(); i++) {
            for (int j = 0; j < high.size(); j++) {
                if (i == 0 && word[i] == low[j]) {
                    word[i] = high[j];
                    break;
                }
                else if (i > 0 && word[i] == high[j]) {
                    word[i] = low[j];
                    break;
                }
            }
        }
        
        // Разделение на выходные и будни
        if (word == "Saturday" || word == "Sunday") {
            weekend.push_back(word);
        }
        else {
            budni.push_back(word);
        }
    }
    
    inputFile.close();
    
    // Вывод выходных дней
    for (int i = 0; i < weekend.size(); i++) {
        theend << weekend[i];
        if (i < weekend.size() - 1) {
            theend << ", ";
        }
    }
    
    // Добавление разделителя между выходными и буднями
    if (!weekend.empty() && !budni.empty()) {
        theend << ", ";
    }
    
    // Вывод будних дней
    for (int i = 0; i < budni.size(); i++) {
        theend << budni[i];
        if (i < budni.size() - 1) {
            theend << ", ";
        }
    }
    
    theend.close();
    
    // Чтение и вывод результата на консоль
    ifstream outputReader("output.txt");
    string line;
    cout << "\nResult in output.txt:" << endl;
    while (getline(outputReader, line)) {
        cout << line << endl;
    }
    outputReader.close();
    
    // Вывод выходных дней на консоль
    if (weekend.size() >= 2) {
        cout << "\nWeekend days: " << weekend[0] << ", " << weekend[1] << endl;
    }
    
    return 0;
}