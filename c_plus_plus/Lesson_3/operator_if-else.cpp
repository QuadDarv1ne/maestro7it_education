#include <iostream>

int main() {
    int number = -5;
    
    if (number >= 0) {
        std::cout << "Число неотрицательное." << std::endl;
    } else {
        std::cout << "Число отрицательное." << std::endl;
    }
    
    return 0;
}