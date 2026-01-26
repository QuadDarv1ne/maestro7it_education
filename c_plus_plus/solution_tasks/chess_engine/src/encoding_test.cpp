#include <iostream>
#include <string>
#include <locale>
#include <codecvt>

#ifdef _WIN32
#include <windows.h>
#endif

void setupEncoding() {
#ifdef _WIN32
    // Set console to UTF-8
    SetConsoleOutputCP(65001); // UTF-8 code page
    SetConsoleCP(65001);
#endif
}

int main() {
    setupEncoding();
    
    std::cout << "Testing encoding support:" << std::endl;
    std::cout << "Latin characters: ABC abc 123" << std::endl;
    std::cout << "UTF-8 characters: café naïve résumé" << std::endl;
    std::cout << "Cyrillic characters: Привет мир" << std::endl;
    std::cout << "Mixed: Hello мир 你好" << std::endl;
    
    // Test chess symbols
    std::cout << "Chess symbols: ♔ ♕ ♖ ♗ ♘ ♙ ♚ ♛ ♜ ♝ ♞ ♟" << std::endl;
    
    return 0;
}