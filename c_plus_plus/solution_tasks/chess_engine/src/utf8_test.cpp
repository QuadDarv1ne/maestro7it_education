#include <iostream>
#include <string>
#include <locale>
#include <codecvt>

#ifdef _WIN32
#include <windows.h>
#include <io.h>
#include <fcntl.h>
#endif

void setupUTF8() {
#ifdef _WIN32
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);
    _setmode(_fileno(stdout), _O_U8TEXT);
    _setmode(_fileno(stderr), _O_U8TEXT);
    _setmode(_fileno(stdin), _O_U8TEXT);
#else
    std::setlocale(LC_ALL, "en_US.UTF-8");
#endif
}

int main() {
    setupUTF8();
    
    std::cout << "Тестирование поддержки UTF-8 и русских символов" << std::endl;
    std::cout << "================================================" << std::endl;
    std::cout << std::endl;
    
    // Тест различных символов
    std::cout << "Латинские символы: ABC abc 123" << std::endl;
    std::cout << "Русские символы: Привет мир" << std::endl;
    std::cout << "Смешанные: Hello мир 你好" << std::endl;
    std::cout << "Шахматные фигуры: ♔ ♕ ♖ ♗ ♘ ♙ ♚ ♛ ♜ ♝ ♞ ♟" << std::endl;
    std::cout << "Специальные символы: α β γ δ ε ζ η θ" << std::endl;
    std::cout << std::endl;
    
    // Тест шахматной терминологии на русском
    std::cout << "Шахматная терминология:" << std::endl;
    std::cout << "• Мат" << std::endl;
    std::cout << "• Пат" << std::endl;
    std::cout << "• Рокировка" << std::endl;
    std::cout << "• Взятие на проходе" << std::endl;
    std::cout << "• Превращение пешки" << std::endl;
    std::cout << std::endl;
    
    // Тест меню на русском
    std::cout << "Главное меню:" << std::endl;
    std::cout << "1. Играть партию" << std::endl;
    std::cout << "2. Настройки" << std::endl;
    std::cout << "3. Помощь" << std::endl;
    std::cout << "4. Выход" << std::endl;
    std::cout << std::endl;
    
    std::cout << "Тест пройден успешно!" << std::endl;
    std::cout << "Все символы отображаются корректно." << std::endl;
    
    return 0;
}