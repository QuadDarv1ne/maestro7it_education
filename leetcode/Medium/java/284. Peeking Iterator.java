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

// Java Iterator interface reference:
// https://docs.oracle.com/javase/8/docs/api/java/util/Iterator.html

/**
 * Класс PeekingIterator, который расширяет стандартный итератор методом peek().
 * 
 * Позволяет просматривать следующий элемент итерации без продвижения итератора.
 * 
 * Поля:
 *   iterator: Исходный итератор Iterator<Integer>
 *   nextElement: Сохраненный следующий элемент
 *   hasNextElement: Флаг наличия следующего элемента
 * 
 * Методы:
 *   PeekingIterator(iterator): Конструктор, инициализирует итератор
 *   peek(): Возвращает следующий элемент без продвижения итератора
 *   next(): Возвращает следующий элемент и продвигает итератор
 *   hasNext(): Проверяет наличие следующего элемента
 * 
 * Интерфейсы:
 *   Реализует Iterator<Integer>, переопределяя методы next() и hasNext()
 * 
 * Исключения:
 *   NoSuchElementException: Вызывается при попытке peek() или next(), когда элементов нет
 * 
 * Пример использования:
 *   List<Integer> nums = Arrays.asList(1, 2, 3);
 *   PeekingIterator iter = new PeekingIterator(nums.iterator());
 *   iter.peek();    // 1
 *   iter.next();    // 1
 *   iter.hasNext(); // true
 */
class PeekingIterator implements Iterator<Integer> {
    private Iterator<Integer> iterator;
    private Integer nextElement;
    private boolean hasNextElement;
    
    public PeekingIterator(Iterator<Integer> iterator) {
        // initialize any member here.
        this.iterator = iterator;
        hasNextElement = iterator.hasNext();
        if (hasNextElement) {
            nextElement = iterator.next();
        }
    }
    
    // Returns the next element in the iteration without advancing the iterator.
    public Integer peek() {
        if (!hasNextElement) {
            throw new NoSuchElementException();
        }
        return nextElement;
    }
    
    // hasNext() and next() should behave the same as in the Iterator interface.
    // Override them if needed.
    @Override
    public Integer next() {
        if (!hasNextElement) {
            throw new NoSuchElementException();
        }
        
        Integer current = nextElement;
        hasNextElement = iterator.hasNext();
        if (hasNextElement) {
            nextElement = iterator.next();
        } else {
            nextElement = null;
        }
        return current;
    }
    
    @Override
    public boolean hasNext() {
        return hasNextElement;
    }
}