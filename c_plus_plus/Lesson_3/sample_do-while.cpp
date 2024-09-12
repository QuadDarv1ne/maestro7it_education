#include <iostream>

int main() {
    int i = 0;
    do {
        std::cout << "Итерация: " << i << std::endl;
        ++i;
    } while (i < 5);
    
    return 0;
}