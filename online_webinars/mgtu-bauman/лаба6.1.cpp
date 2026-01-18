// лаба6.1.cpp : Этот файл содержит функцию "main". Здесь начинается и заканчивается выполнение программы.
//
//#include<stdafx.h>
#include"math.h"
#include <iostream>
#include"string"
using namespace std;
char toUpper(char a) {
    int num = int(a);
    if (num >= int('a') && num <= int('z')) {
        return char(int(a) - 32);
    }
    else {
        return a;
    }
} 
int main()
{
    bool c = true;
    int a, b;
    string door;
    door = "Henlo wreld";
    for (int i = 0; i < door.length(); i++) {
        if (door[i] == ' ' || door[i] == '!' || door[i] == '?' || door[i] == '.') {
            door.erase(i, 1);
            i--;
        }
    }
    cout << door << endl;
    string doors[5] = {
        "one",
        "Uuu",
        "Door",
        "Two  notebook",
        "Kot Shotland"
    };
    int arrLen = sizeof(doors) / sizeof(doors[0]);
    for (int i = 0; i < arrLen; i++) {
        for (int j = 0; j < doors[i].length(); j++) {
            doors[i][j] = toUpper(doors[i][j]);
            cout << doors[i][j];
        }
        cout << endl;
    }
    
    while (true) {
        for (int i = 0; i < door.length() / 2; i++) {
            if (door[i] == door[door.length() - 1 - i]) {
                cout << "polidrom";
            }
            else {
                cout << "podnyat flag" << endl;
                c = !true;
                break;
            }
        }
    }

    return 0;
}

// Запуск программы: CTRL+F5 или меню "Отладка" > "Запуск без отладки"
// Отладка программы: F5 или меню "Отладка" > "Запустить отладку"

// Советы по началу работы 
//   1. В окне обозревателя решений можно добавлять файлы и управлять ими.
//   2. В окне Team Explorer можно подключиться к системе управления версиями.
//   3. В окне "Выходные данные" можно просматривать выходные данные сборки и другие сообщения.
//   4. В окне "Список ошибок" можно просматривать ошибки.
//   5. Последовательно выберите пункты меню "Проект" > "Добавить новый элемент", чтобы создать файлы кода, или "Проект" > "Добавить существующий элемент", чтобы добавить в проект существующие файлы кода.
//   6. Чтобы снова открыть этот проект позже, выберите пункты меню "Файл" > "Открыть" > "Проект" и выберите SLN-файл.
