/*
    📖 fstream — это библиотека для работы с файлами.
    
    ▶️ Она предоставляет три основных класса:
    1️⃣ std::ifstream: поток ввода из файла
    2️⃣ std::ofstream: поток вывода в файл
    3️⃣ std::fstream: поток ввода и вывода в файл
*/

#include <fstream>
#include <iostream>

using namespace std;

int main() {
    std::ofstream outFile("example.txt"); // Открытие файла для записи
    if (outFile.is_open()) {
        outFile << "Hello, file :D" << std::endl;
        outFile.close(); // Закрытие файла
    } else {
        std::cerr << "Не удалось открыть файл для записи." << std::endl;
    }

    std::ifstream inFile("example.txt"); // Открытие файла для чтения
    std::string line;
    if (inFile.is_open()) {
        while (std::getline(inFile, line)) {
            std::cout << line << std::endl;
        }
        inFile.close(); // Закрытие файла
    } else {
        std::cerr << "Не удалось открыть файл для чтения." << std::endl;
    }

    return 0;
}
