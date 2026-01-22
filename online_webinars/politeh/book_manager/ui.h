#ifndef UI_H
#define UI_H

#include "library.h"
#include <string>

class UI {
private:
    Library& library;
    
    void clearInputBuffer();
    int getIntInput(const char* prompt);
    std::string getStringInput(const char* prompt);
    
    void addBookMenu();
    void removeBookMenu();
    void updateBookMenu();
    void sortMenu();
    void searchMenu();
    void fileMenu();
    void specialFunctionsMenu();
    void undoMenu();
    void loggingMenu();
    
public:
    UI(Library& lib);
    void run();
};

#endif