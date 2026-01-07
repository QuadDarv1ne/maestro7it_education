package analyzer.utils;

import java.util.Arrays;

/**
 * Эффективный список целых чисел с автоматическим расширением
 */
public class IntList {
    private static final int DEFAULT_CAPACITY = 10;
    private static final int MAX_CAPACITY = Integer.MAX_VALUE - 8;

    private int[] data;
    private int size;

    public IntList() {
        this(DEFAULT_CAPACITY);
    }

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

    public IntList(IntList other) {
        this.data = Arrays.copyOf(other.data, other.size);
        this.size = other.size;
    }

    public void add(int value) {
        ensureCapacity(size + 1);
        data[size++] = value;
    }

    public void addAll(IntList other) {
        ensureCapacity(size + other.size);
        System.arraycopy(other.data, 0, data, size, other.size);
        size += other.size;
    }

    public int get(int index) {
        rangeCheck(index);
        return data[index];
    }

    public void set(int index, int value) {
        rangeCheck(index);
        data[index] = value;
    }

    public int size() {
        return size;
    }

    public boolean isEmpty() {
        return size == 0;
    }

    public void clear() {
        size = 0;
    }

    public int[] toArray() {
        return Arrays.copyOf(data, size);
    }

    public void sort() {
        Arrays.sort(data, 0, size);
    }

    public int indexOf(int value) {
        for (int i = 0; i < size; i++) {
            if (data[i] == value) {
                return i;
            }
        }
        return -1;
    }

    public boolean contains(int value) {
        return indexOf(value) != -1;
    }

    public void remove(int index) {
        rangeCheck(index);
        int numMoved = size - index - 1;
        if (numMoved > 0) {
            System.arraycopy(data, index + 1, data, index, numMoved);
        }
        size--;
    }

    public void removeValue(int value) {
        int index = indexOf(value);
        if (index != -1) {
            remove(index);
        }
    }

    public void ensureCapacity(int minCapacity) {
        if (minCapacity - data.length > 0) {
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

            data = Arrays.copyOf(data, newCapacity);
        }
    }

    public void trimToSize() {
        if (size < data.length) {
            data = Arrays.copyOf(data, size);
        }
    }

    private void rangeCheck(int index) {
        if (index < 0 || index >= size) {
            throw new IndexOutOfBoundsException(
                    String.format("Индекс: %d, Размер: %d", index, size));
        }
    }

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

    @Override
    public int hashCode() {
        int result = 1;
        for (int i = 0; i < size; i++) {
            result = 31 * result + data[i];
        }
        return result;
    }

    /**
     * Возвращает сумму всех элементов
     */
    public long sum() {
        long total = 0;
        for (int i = 0; i < size; i++) {
            total += data[i];
        }
        return total;
    }
}