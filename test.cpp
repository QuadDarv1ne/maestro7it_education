#include <iostream>
#include <windows.h>  // Windows API для управления консолью

int main() {
    // Установка UTF-8 для ввода/вывода (работает в Windows 10+)
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);

    // Проверка (должно вывести кириллицу без искажений)
    std::cout << "Привет, мир αβс ©\n"; 

    // Дальше идёт ваша локализованная логика...
    // (работа с <locale>, gettext и т.д.)
}
