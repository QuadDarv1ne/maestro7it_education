#include <vector>
#include <iostream>
#include <typeinfo>

/**
 * @brief Демонстрация использования различных методов класса std::vector в C++.
 *
 * Этот код демонстрирует основные функции и операторы, доступные для работы с векторами в C++.
 * Каждый метод сопровождается кратким описанием его функциональности.
 */
int main() {
    // Объявление векторов
    std::vector<int> v1, v2, v3, v4;

    // Заполнение вектора v1 значениями
    v1.push_back(10);
    v1.push_back(20);
    v1.push_back(30);
    v1.push_back(40);
    v1.push_back(50);

    // Вывод содержимого вектора v1
    std::cout << "v1 = ";
    for (const auto& v : v1) {
        std::cout << v << " ";
    }
    std::cout << std::endl;

    /**
     * @brief assign: Удаляет вектор и копирует указанные элементы в пустой вектор.
     */
    v2.assign(v1.begin(), v1.end());
    std::cout << "v2 = ";
    for (const auto& v : v2) {
        std::cout << v << " ";
    }
    std::cout << std::endl;

    /**
     * @brief assign: Заполняет вектор определённым количеством одинаковых элементов.
     */
    v3.assign(7, 4);
    std::cout << "v3 = ";
    for (const auto& v : v3) {
        std::cout << v << " ";
    }
    std::cout << std::endl;

    /**
     * @brief assign: Заменяет содержимое вектора на элементы из инициализаторного списка.
     */
    v4.assign({ 5, 6, 7 });
    std::cout << "v4 = ";
    for (const auto& v : v4) {
        std::cout << v << " ";
    }
    std::cout << std::endl;

    /**
     * @brief data: Возвращает указатель на первый элемент в векторе.
     */
    std::cout << "Указатель на данные v4: " << v4.data() << std::endl;

    /**
     * @brief back: Возвращает ссылку на последний элемент вектора.
     */
    std::cout << "Последний элемент в списке v1: " << v1.back() << std::endl;
    std::cout << "Последний элемент в списке v2: " << v2.back() << std::endl;
    std::cout << "Последний элемент в списке v3: " << v3.back() << std::endl;
    std::cout << "Последний элемент в списке v4: " << v4.back() << std::endl;

    /**
     * @brief rbegin и rend: Возвращают итераторы для обратной итерации по вектору.
     */
    std::cout << "v1 в обратном порядке: ";
    for (auto it = v1.rbegin(); it != v1.rend(); ++it) {
        std::cout << *it << " ";
    }
    std::cout << std::endl;

    /**
     * @brief reserve: Резервирует минимальную длину хранилища для объекта вектора.
     */
    v1.reserve(20);
    std::cout << "Размер v1: " << v1.size() << ", ёмкость v1: " << v1.capacity() << std::endl;

    /**
     * @brief resize: Определяет новый размер вектора.
     */
    v1.resize(10, 0);
    std::cout << "v1 после resize: ";
    for (const auto& v : v1) {
        std::cout << v << " ";
    }
    std::cout << std::endl;

    /**
     * @brief get_allocator: Возвращает объект класса allocator, используемого вектором.
     */
    std::allocator<int> alloc = v1.get_allocator();
    std::cout << "Используется аллокатор: " << typeid(alloc).name() << std::endl;

    /**
     * @brief front: Возвращает ссылку на первый элемент вектора.
     */
    std::cout << "Первый элемент в списке v1: " << v1.front() << std::endl;

    /**
     * @brief at: Возвращает ссылку на элемент в заданном положении в векторе.
     */
    try {
        std::cout << "Элемент v1 на позиции 3: " << v1.at(3) << std::endl;
    } catch (const std::out_of_range& e) {
        std::cerr << "Ошибка: " << e.what() << std::endl;
    }

    /**
     * @brief cbegin и cend: Возвращают константные итераторы для вектора.
     */
    std::cout << "v1 с использованием cbegin и cend: ";
    for (auto it = v1.cbegin(); it != v1.cend(); ++it) {
        std::cout << *it << " ";
    }
    std::cout << std::endl;

    /**
     * @brief crbegin и crend: Возвращают константные итераторы для обратной итерации по вектору.
     */
    std::cout << "v1 в обратном порядке с использованием crbegin и crend: ";
    for (auto it = v1.crbegin(); it != v1.crend(); ++it) {
        std::cout << *it << " ";
    }
    std::cout << std::endl;

    /**
     * @brief clear: Очищает элементы вектора.
     */
    v2.clear();
    std::cout << "v2 после clear: размер = " << v2.size() << std::endl;

    /**
     * @brief emplace: Вставляет элемент, созданный на месте, в указанное положение в векторе.
     */
    v1.emplace(v1.begin() + 1, 99);
    std::cout << "v1 после emplace(99) на позицию 1: ";
    for (const auto& v : v1) {
        std::cout << v << " ";
    }
    std::cout << std::endl;

    /**
     * @brief emplace_back: Добавляет элемент, созданный на месте, в конец вектора.
     */
    v1.emplace_back(100);
    std::cout << "v1 после emplace_back(100): ";
    for (const auto& v : v1) {
        std::cout << v << " ";
    }
    std::cout << std::endl;

    /**
     * @brief empty: Проверяет, пуст ли контейнер вектора.
     */
    std::cout << "v2 пуст? " << (v2.empty() ? "Да" : "Нет") << std::endl;

    /**
     * @brief max_size: Возвращает максимальную длину вектора.
     */
    std::cout << "Максимальный размер v1: " << v1.max_size() << std::endl;

    /**
     * @brief shrink_to_fit: Удаляет лишнюю емкость.
     */
    v1.shrink_to_fit();
    std::cout << "Ёмкость v1 после shrink_to_fit: " << v1.capacity() << std::endl;

    /**
     * @brief size: Возвращает количество элементов в векторе.
     */
    std::cout << "Размер v1: " << v1.size() << std::endl;

    /**
     * @brief swap: Меняет местами элементы двух векторов.
     */
    v3.swap(v4);
    std::cout << "v3 после swap с v4: ";
    for (const auto& v : v3) {
        std::cout << v << " ";
    }
    std::cout << std::endl;

    std::cout << "v4 после swap с v3: ";
    for (const auto& v : v4) {
        std::cout << v << " ";
    }
    std::cout << std::endl;

    return 0;
}
