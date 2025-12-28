#include "library.h"
#include "ui.h"
#include <locale.h>
#include <clocale>
#include <iostream>

#ifdef _WIN32
    #include <windows.h>
#endif

int main() {
    // Установка локали для поддержки кириллицы
    setlocale(LC_ALL, "ru_RU.UTF-8");
    
    #ifdef _WIN32
    // Для Windows: установка кодовой страницы UTF-8
    SetConsoleCP(65001);
    SetConsoleOutputCP(65001);
    
    // Дополнительная настройка для Visual Studio
    #ifdef _MSC_VER
    system("chcp 65001 > nul");
    std::locale::global(std::locale("ru_RU.UTF-8"));
    #endif
    #endif
    
    Library library;
    UI ui(library);
    
    ui.run();
    
    return 0;
}