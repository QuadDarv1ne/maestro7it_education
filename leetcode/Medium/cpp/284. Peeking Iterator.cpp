/**
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Полезные ссылки:
 * 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
 * 2. Telegram №1 @quadd4rv1n7
 * 3. Telegram №2 @dupley_maxim_1999
 * 4. Rutube канал: https://rutube.ru/channel/4218729/
 * 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
 * 6. YouTube канал: https://www.youtube.com/@it-coders
 * 7. ВК группа: https://vk.com/science_geeks
 */

/*
 * Below is the interface for Iterator, which is already defined for you.
 * **DO NOT** modify the interface for Iterator.
 *
 *  class Iterator {
 *      struct Data;
 *      Data* data;
 *      Iterator(const vector<int>& nums);
 *      Iterator(const Iterator& iter);
 *
 *      // Returns the next element in the iteration.
 *      int next();
 *
 *      // Returns true if the iteration has more elements.
 *      bool hasNext() const;
 *  };
 */

/**
 * Класс PeekingIterator, который расширяет стандартный итератор методом peek().
 * 
 * Позволяет просматривать следующий элемент итерации без продвижения итератора.
 * 
 * Атрибуты:
 *   next_val: Сохраненный следующий элемент
 *   has_next_val: Флаг наличия следующего элемента
 * 
 * Методы:
 *   PeekingIterator(nums): Конструктор, инициализирует итератор
 *   peek(): Возвращает следующий элемент без продвижения итератора
 *   next(): Возвращает следующий элемент и продвигает итератор
 *   hasNext(): Проверяет наличие следующего элемента
 * 
 * Наследование:
 *   Наследует от класса Iterator, использует его методы next() и hasNext()
 * 
 * Пример использования:
 *   vector<int> nums = {1, 2, 3};
 *   PeekingIterator* iter = new PeekingIterator(nums);
 *   iter->peek();    // 1
 *   iter->next();    // 1
 *   iter->hasNext(); // true
 */
class PeekingIterator : public Iterator {
private:
    int next_val;
    bool has_next_val;
    
public:
    PeekingIterator(const vector<int>& nums) : Iterator(nums) {
        // Initialize any member here.
        // **DO NOT** save a copy of nums and manipulate it directly.
        // You should only use the Iterator interface methods.
        has_next_val = Iterator::hasNext();
        if (has_next_val) {
            next_val = Iterator::next();
        }
    }
    
    // Returns the next element in the iteration without advancing the iterator.
    int peek() {
        return next_val;
    }
    
    // hasNext() and next() should behave the same as in the Iterator interface.
    // Override them if needed.
    int next() {
        int current = next_val;
        has_next_val = Iterator::hasNext();
        if (has_next_val) {
            next_val = Iterator::next();
        }
        return current;
    }
    
    bool hasNext() const {
        return has_next_val;
    }
};