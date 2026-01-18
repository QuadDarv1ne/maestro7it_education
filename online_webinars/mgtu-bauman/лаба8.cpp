// лаба8.cpp : Этот файл содержит функцию "main". Здесь начинается и заканчивается выполнение программы.
//
//#include "stdafx.h"
#include "iostream"
#include "fstream"
#include"string"
#include"vector"
using namespace std;
int main()
{
	cout << "Laboratornaya 8" << endl;
	ofstream record("record.txt");
	record << "moNDay THuesDAY weDNeSdAy tHuRsdAY FRAIday satURday sundaY";
	record.close();
	
	string word;
    ifstream cin("record.txt");
	ofstream theend("output.txt");
	string high = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
	string low = "abcdefghijklmnopqrstuvwxyz";
	vector<string> weekend;
	vector<string> budni;
	while (cin >> word) {
		for (int i = 0; i < word.size(); i++) {
			for (int j = 0; j < high.size(); j++) {
				if (i == 0 && word[i] == low[j]) {
					word[i] = high[j];
					theend << word[i];
				}
				else if (i > 0 && word[i] == high[j]) {
					word[i] = low[j];
					theend << word[i];
				}
			}
		}
		if (word == "Saturday" || word == "Sunday") {
			weekend.push_back(word);
		}
		else {
			budni.push_back(word);
		}
	}
	for (int i = 0; i < weekend.size(); i++) {
		theend << weekend[i] << ", ";
	}
	for (int i = 0; i < budni.size()-1; i++) {
			theend << budni[i] << ", ";
	}
	theend.close();
	cin.close();
	ifstream ("output.txt");
	cout << weekend[0] << ", " << weekend[1];
	theend.close();
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
