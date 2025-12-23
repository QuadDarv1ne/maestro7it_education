#include <iostream> // ввод/вывод
#include <iomanip>  // формат вывода
#include <cstdlib>  // rand() и srand()
#include <ctime>    // генерация рандомных чисел
#include <locale>

using namespace std;

#ifdef _WIN32
    #include <windows.h>
    #include <fcntl.h>
#endif

// Настройка консоли Windows для работы с UTF-8
void initWindowsConsole() {
    // Устанавливаем кодовую страницу консоли в UTF-8
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);
    
    // Настраиваем буферы для предотвращения искажения кириллицы
    setvbuf(stdout, nullptr, _IOFBF, 1000);
}

// создание матрицы r×c
double** createMatrix(int r, int c) { // динамическая память (двумерный массив через массив указателей)
    double** m = new double*[r]; // создаем массив указателей (строк)
    for (int i = 0; i < r; i++)
        m[i] = new double[c]; // для каждой строки создаем массив строк
    return m; // возвращаем указатель на матрицу
}

// очищение памяти
void deleteMatrix(double** m, int r) {
    for (int i = 0; i < r; i++)
        delete[] m[i]; // сначала удаляем каждую строку
    delete[] m; // потом массив указателей
}

// ручной ввод
void inputMatrix(double** m, int r, int c) {
    cout << "Введите " << r * c << " чисел:\n";
    for (int i = 0; i < r; i++)
        for (int j = 0; j < c; j++)
            cin >> m[i][j];
}

// случайное заполнение
void randomFill(double** m, int r, int c, double a, double b) {
    for (int i = 0; i < r; i++)
        for (int j = 0; j < c; j++) {
            double x = (double)rand() / RAND_MAX; // получаем число от 0 до 1
            m[i][j] = a + x * (b - a); // преобразование в [a, b]
        }
}

// печать матрицы
void printMatrix(double** m, int r, int c) {
    cout << fixed << setprecision(2);
    for (int i = 0; i < r; i++) {
        for (int j = 0; j < c; j++)
            cout << setw(10) << m[i][j];
        cout << endl;
    }
}

// операция 1 — сортировка нечётных столбцов (0, 2, 4 и т.д.)
void sortOddColumns(double** m, int r, int c) {
    if (c == 0) return;

    int count = (c + 1) / 2; // сколько столбцов с четными индексами
    int* cols = new int[count]; // массив для хранения индексов этих столбцов

    for (int i = 0; i < count; i++)
        cols[i] = i * 2; // индексы нечетных столбцов

    // пузырьковая сортировка по убыванию элементов первой строки
    for (int i = 0; i < count - 1; i++)
        for (int j = 0; j < count - 1 - i; j++)
            if (m[0][cols[j]] < m[0][cols[j + 1]]) // сравниваем по первой строке
                swap(cols[j], cols[j + 1]); // меняем индексы местами

    // копия
    double** tmp = createMatrix(r, c); // временная копия матрицы
    for (int i = 0; i < r; i++)
        for (int j = 0; j < c; j++)
            tmp[i][j] = m[i][j];

    // перестановка соответствующих столбцов в исходной
    int k = 0;
    for (int j = 0; j < c; j += 2) {
        int src = cols[k++];
        for (int i = 0; i < r; i++)
            m[i][j] = tmp[i][src];
    }

    deleteMatrix(tmp, r); // удаляем временную матрицу
    delete[] cols; // удаляем временный массив индексов
}

// операция 2 — три max под диагональю, работает только если rows (столбцы) == cols (строки)
bool threeMaxBelowDiagonal(double** m, int r, int c, double result[3], int& count) {
    if (r != c) { // проверка квадратная ли матрица
        cout << "Поиск элементов под диагональю доступен только для квадратных матриц!\n";
        count = 0;
        return false;
    }
    // сбор элементов под диагональю (i > j)
    int n = r;
    count = 0;

    int maxSize = n * (n - 1) / 2; // максимальное кол-во элементов под диагональю
    double* temp = new double[maxSize];

    for (int i = 1; i < n; i++) // идем по строкам со второй
        for (int j = 0; j < i; j++) // идем по столбцам до диагонали
            temp[count++] = m[i][j]; // собираем числа под диагональю в 1 ряд

    // пузырьковая сортировка по убыванию
    for (int i = 0; i < count - 1; i++)
        for (int j = 0; j < count - 1 - i; j++)
            if (temp[j] < temp[j + 1])
                swap(temp[j], temp[j + 1]);

    for (int i = 0; i < 3; i++)
        result[i] = (i < count ? temp[i] : 0); // возвращает первые три таких элемента, остальные 0

    delete[] temp;
    return true;
}

// операция 3 — умножение матриц A(r×c) * B(c×k)
double** multiply(double** A, int rA, int cA, double** B, int rB, int cB) {
    if (cA != rB) { // проверка можно ли умножить (число столбцов А = число строк В
        cout << "Умножение невозможно, т.к. размеры не совпадают\n";
        return nullptr;
    }

    double** C = createMatrix(rA, cB); // результирующая матрица С

    for (int i = 0; i < rA; i++) // строки А
        for (int j = 0; j < cB; j++) { // столбцы В
            C[i][j] = 0;
            for (int k = 0; k < cA; k++) // суммирование произведений
                C[i][j] += A[i][k] * B[k][j];
        }

    return C;
}

// квадрат матрицы
double** squareMatrix(double** M, int r, int c) {
    if (r != c) {
        cout << "Квадрат невозможен, т.к. матрица не квадратная!\n";
        return nullptr;
    }
    return multiply(M, r, c, M, r, c);
}

int main() {
    // Инициализация консоли Windows для UTF-8
    initWindowsConsole();

    // setlocale(LC_ALL, "RU");
    setlocale(LC_ALL, "ru_RU.UTF-8");
    
    srand(time(0));

    int rA, cA, rB, cB;

    cout << "Введите размер матрицы A (строки столбцы): ";
    cin >> rA >> cA;

    cout << "Введите размер матрицы B (строки столбцы): ";
    cin >> rB >> cB;

    double** A = createMatrix(rA, cA); // создание матрицы А
    double** B = createMatrix(rB, cB); // создание матрицы В

    int mode;

    // Ввод A
    cout << "\nЗаполнение матрицы A: 1 — вручную, 2 — случайно\n> ";
    cin >> mode;
    if (mode == 1) inputMatrix(A, rA, cA);
    else {
        double a, b;
        cout << "Введите диапазон [a b]: ";
        cin >> a >> b;
        randomFill(A, rA, cA, a, b);
    }

    cout << "\nМатрица A:\n";
    printMatrix(A, rA, cA);

    // Ввод B
    cout << "\nЗаполнение матрицы B: 1 — вручную, 2 — случайно\n> ";
    cin >> mode;
    if (mode == 1) inputMatrix(B, rB, cB);
    else {
        double a, b;
        cout << "Введите диапазон [a b]: ";
        cin >> a >> b;
        randomFill(B, rB, cB, a, b);
    }

    cout << "\nМатрица B:\n";
    printMatrix(B, rB, cB);

    // 1 — сортировка столбцов
    sortOddColumns(A, rA, cA);
    sortOddColumns(B, rB, cB);

    cout << "\nA после сортировки:\n";
    printMatrix(A, rA, cA);

    cout << "\nB после сортировки:\n";
    printMatrix(B, rB, cB);

    // 2 — три максимальных элемента
    double maxA[3], maxB[3];
    int countA, countB;

    threeMaxBelowDiagonal(A, rA, cA, maxA, countA);
    threeMaxBelowDiagonal(B, rB, cB, maxB, countB);

    if (countA > 0) {
        cout << "\nМаксимальные под диагональю A: ";
        for (int i = 0; i < min(countA, 3); i++)
            cout << maxA[i] << " ";
        cout << endl;
    }

    if (countB > 0) {
        cout << "Максимальные под диагональю B: ";
        for (int i = 0; i < min(countB, 3); i++)
            cout << maxB[i] << " ";
        cout << endl;
    }

    // 3 — квадраты матриц
    double** A2 = squareMatrix(A, rA, cA);
    double** B2 = squareMatrix(B, rB, cB);

    if (A2) {
        cout << "\nA * A:\n";
        printMatrix(A2, rA, cA);
    }

    if (B2) {
        cout << "\nB * B:\n";
        printMatrix(B2, rB, cB);
    }

    // 4 — произведения A*B и B*A
    double** AB = multiply(A, rA, cA, B, rB, cB);
    double** BA = multiply(B, rB, cB, A, rA, cA);

    if (AB) {
        cout << "\nA * B:\n";
        printMatrix(AB, rA, cB);
    }

    if (BA) {
        cout << "\nB * A:\n";
        printMatrix(BA, rB, cA);
    }

    // освобождение памяти
    deleteMatrix(A, rA);
    deleteMatrix(B, rB);
    if (A2) deleteMatrix(A2, rA);
    if (B2) deleteMatrix(B2, rB);
    if (AB) deleteMatrix(AB, rA);
    if (BA) deleteMatrix(BA, rB);

    return 0;
}