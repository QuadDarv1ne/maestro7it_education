#include <iostream>

int main() {
    int day = 3;
    
    switch (day) {
        case 1:
            std::cout << "Понедельник" << std::endl;
            break;
        case 2:
            std::cout << "Вторник" << std::endl;
            break;
        case 3:
            std::cout << "Среда" << std::endl;
            break;
        default:
            std::cout << "Другой день недели" << std::endl;
            break;
    }
    
    return 0;
}