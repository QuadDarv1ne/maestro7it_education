#include <iostream>

int main() {
    int number = 0;
    
    if (number > 0) {
        std::cout << "Число положительное." << std::endl;
    } else if (number < 0) {
        std::cout << "Число отрицательное." << std::endl;
    } else {
        std::cout << "Число равно нулю." << std::endl;
    }
    
    return 0;
}