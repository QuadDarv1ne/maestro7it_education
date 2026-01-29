#include "console_ui.hpp"
#include <iostream>
#include <cstdlib>
#include <ctime>
#include <locale>
#include <codecvt>
#include <string>
#include "../include/utf8_support.hpp"

#ifdef _WIN32
#include <windows.h>
#endif

// Function to set console encoding
void setupConsoleEncoding() {
#ifdef _WIN32
    // Set console to UTF-8
    SetConsoleOutputCP(65001);
    SetConsoleCP(65001);
#endif
}

int main() {
    try {
        // Setup console encoding
        setupConsoleEncoding();
        
        // Initialize UTF-8 support
        UTF8Support::initialize();
        
        // Seed random number generator
        std::srand(static_cast<unsigned int>(std::time(nullptr)));
        
        std::cout << "========================================\n";
        std::cout << "           CHESS ENGINE v1.0            \n";
        std::cout << "========================================\n";
        std::cout << "Welcome to the Chess Engine!\n";
        std::cout << "A clean, modular chess engine written in C++\n\n";
        
        // Create and run the console UI
        ConsoleUI ui;
        ui.run();
        
        std::cout << "\nThank you for playing! Goodbye.\n";
        return 0;
    }
    catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
    catch (...) {
        std::cerr << "Unknown error occurred!" << std::endl;
        return 1;
    }
}