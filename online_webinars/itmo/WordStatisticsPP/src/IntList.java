/**
 * Класс для хранения списка целых чисел
 * 
 * <p>Реализуем динамический массив целых чисел с автоматическим выделением ёмкости памяти при необходимости.
 * <p>Используется для хранения позиций слов в тексте.
 */

import java.util.Arrays;

public class IntList {
    private static final int DEFAULT_CAPACITY = 10;
    private static final int MAX_CAPACITY = Integer.MAX_VALUE - 8;

    private int[] data;
    private int size;

    /**
     * Создаёт новый пустой список чисел с ёмкостью по умолчанию.
     */
    public IntList() {
        this(DEFAULT_CAPACITY);
    }

    /**
     * Создает новый пустой список целых чисел с указанной начальной емкостью.
     * 
     * @param initialCapacity начальная емкость списка
     * @throws IllegalArgumentException если initialCapacity отрицательно
     */
    public IntList(int initialCapacity) {
        if (initialCapacity < 0) {
            throw new IllegalArgumentException("Начальная емкость не может быть отрицательной: " + initialCapacity);
        }
        
        if (initialCapacity == 0) {
            this.data = new int[0];
        } else {
            this.data = new int[Math.min(initialCapacity, MAX_CAPACITY)];
        }
        this.size = 0;
    }
    
    /**
     * Добавляет значение в конец списка.
     * 
     * <p>Если внутренний массив заполнен, его емкость увеличивается
     * до data.length * 2, но не более MAX_CAPACITY.
     * 
     * @param value добавляемое целочисленное значение
     * @throws IllegalStateException если список достиг максимальной емкости
     */
    public void add(int value) {
        ensureCapacity(size + 1);
        data[size] = value;
        size++;
    }
    
    /**
     * Возвращает значение по указанному индексу.
     * 
     * @param index индекс элемента (0-based)
     * @return значение элемента по указанному индексу
     * @throws IndexOutOfBoundsException если индекс выходит за пределы списка
     */
    public int get(int index) {
        rangeCheck(index);
        return data[index];
    }

    /**
     * Возвращает количество элементов в списке.
     * 
     * @return текущий размер списка
     */
    public int size() {
        return size;
    }

    /**
     * Проверяет, пустой ли список
     */
    public boolean isEmpty() {
        return size == 0;
    }

    /**
     * Возвращает внутренний массив с элементами списка.
     */
    public int[] toArray() {
        return Arrays.copyOf(data, size);
    }

    /**
     * Гарантирует, что список имеет достаточную емкость для хранения указанного количества элементов.
     * 
     * @param minCapacity минимальная требуемая емкость
     * @throws IllegalStateException если требуемая емкость превышает MAX_CAPACITY
     */
    private void ensureCapacity(int minCapacity) {
        if (minCapacity - data.length > 0) {
            // Вычисляем новую емкость
            int oldCapacity = data.length;
            int newCapacity = oldCapacity + (oldCapacity >> 1); // Увеличиваем на 50%
            
            if (newCapacity - minCapacity < 0) {
                newCapacity = minCapacity;
            }
            
            if (newCapacity - MAX_CAPACITY > 0) {
                if (minCapacity < 0) { // Переполнение
                    throw new OutOfMemoryError("Требуемая емкость превышает максимальную");
                }
                newCapacity = (minCapacity > MAX_CAPACITY) ? 
                        Integer.MAX_VALUE : MAX_CAPACITY;
            }
            
            // Копируем данные в новый массив
            data = Arrays.copyOf(data, newCapacity);
        }
    }

    private void rangeCheck(int index) {
        if (index < 0 || index >= size) {
            throw new IndexOutOfBoundsException(
                String.format("Индекс: %d, Размер: %d", index, size)
            );
        }
    }

    /**
     * Возвращает строковое представление списка.
     * 
     * <p>Формат: "[1, 2, 3]" для списка из трех элементов.
     * 
     * @return строковое представление списка
     */
    @Override
    public String toString() {
        if (size == 0) {
            return "[]";
        }
        
        StringBuilder sb = new StringBuilder();
        sb.append('[');
        
        for (int i = 0; i < size; i++) {
            sb.append(data[i]);
            if (i < size - 1) {
                sb.append(", ");
            }
        }
        
        sb.append(']');
        return sb.toString();
    }
    
    /**
     * Сравнивает этот список с другим объектом.
     * 
     * @param obj объект для сравнения
     * @return true если obj является IntList с такими же элементами в том же порядке
     */
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        
        IntList other = (IntList) obj;
        if (size != other.size) return false;
        
        for (int i = 0; i < size; i++) {
            if (data[i] != other.data[i]) {
                return false;
            }
        }
        
        return true;
    }
    
    /**
     * Возвращает хэш-код списка.
     * 
     * @return хэш-код, вычисленный на основе элементов списка
     */
    @Override
    public int hashCode() {
        int result = 1;
        for (int i = 0; i < size; i++) {
            result = 31 * result + data[i];
        }
        return result;
    }
}