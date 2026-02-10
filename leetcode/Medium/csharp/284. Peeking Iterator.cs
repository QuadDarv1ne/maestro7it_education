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

// C# IEnumerator interface:
//     object Current { get; }
//     bool MoveNext();
//     void Reset();

/// <summary>
/// Класс PeekingIterator, который расширяет стандартный итератор методом Peek().
/// 
/// Позволяет просматривать следующий элемент итерации без продвижения итератора.
/// 
/// Поля:
///   iterator: Исходный итератор IEnumerator<int>
///   hasNext: Флаг наличия следующего элемента
///   nextValue: Сохраненный следующий элемент
/// 
/// Методы:
///   PeekingIterator(iterator): Конструктор, инициализирует итератор
///   Peek(): Возвращает следующий элемент без продвижения итератора
///   Next(): Возвращает следующий элемент и продвигает итератор
///   HasNext(): Проверяет наличие следующего элемента
/// 
/// Исключения:
///   InvalidOperationException: Вызывается при попытке Peek() или Next(), когда элементов нет
/// 
/// Пример использования:
///   List<int> nums = new List<int> { 1, 2, 3 };
///   PeekingIterator iter = new PeekingIterator(nums.GetEnumerator());
///   iter.Peek();    // 1
///   iter.Next();    // 1
///   iter.HasNext(); // true
/// </summary>
class PeekingIterator {
    private IEnumerator<int> iterator;
    private bool hasNext;
    private int nextValue;
    
    // iterators refers to the first element of the array.
    public PeekingIterator(IEnumerator<int> iterator) {
        // initialize any member here.
        this.iterator = iterator;
        hasNext = iterator.MoveNext();
        if (hasNext) {
            nextValue = iterator.Current;
        }
    }
    
    // Returns the next element in the iteration without advancing the iterator.
    public int Peek() {
        if (!hasNext) throw new InvalidOperationException("No more elements");
        return nextValue;
    }
    
    // Returns the next element in the iteration and advances the iterator.
    public int Next() {
        if (!hasNext) throw new InvalidOperationException("No more elements");
        
        int current = nextValue;
        hasNext = iterator.MoveNext();
        if (hasNext) {
            nextValue = iterator.Current;
        }
        return current;
    }
    
    // Returns false if the iterator is refering to the end of the array of true otherwise.
    public bool HasNext() {
        return hasNext;
    }
}