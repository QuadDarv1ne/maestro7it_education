package analyzer.statistics;

import analyzer.utils.IntList;
import java.util.*;

/**
 * Класс для сбора и анализа статистики чисел в тексте
 */
public class NumberStatistics {
    private final List<Integer> numbers;
    private final IntList positions;
    private int totalNumbers;
    
    public NumberStatistics() {
        this.numbers = new ArrayList<>();
        this.positions = new IntList();
        this.totalNumbers = 0;
    }
    
    /**
     * Добавляет число в статистику
     */
    public void addNumber(int number) {
        numbers.add(number);
        positions.add(++totalNumbers);
    }
    
    /**
     * Добавляет несколько чисел
     */
    public void addNumbers(List<Integer> numbersList) {
        for (Integer number : numbersList) {
            addNumber(number);
        }
    }
    
    /**
     * Возвращает общее количество чисел
     */
    public int getTotalNumbers() {
        return totalNumbers;
    }
    
    /**
     * Возвращает список всех чисел
     */
    public List<Integer> getNumbers() {
        return new ArrayList<>(numbers);
    }
    
    /**
     * Возвращает позиции чисел
     */
    public IntList getPositions() {
        return positions;
    }
    
    /**
     * Возвращает минимальное число
     */
    public int getMin() {
        if (numbers.isEmpty()) {
            throw new IllegalStateException("Нет чисел в статистике");
        }
        
        return Collections.min(numbers);
    }
    
    /**
     * Возвращает максимальное число
     */
    public int getMax() {
        if (numbers.isEmpty()) {
            throw new IllegalStateException("Нет чисел в статистике");
        }
        
        return Collections.max(numbers);
    }
    
    /**
     * Возвращает сумму всех чисел
     */
    public long getSum() {
        long sum = 0;
        for (int number : numbers) {
            sum += number;
        }
        return sum;
    }
    
    /**
     * Возвращает среднее арифметическое
     */
    public double getAverage() {
        if (numbers.isEmpty()) {
            throw new IllegalStateException("Нет чисел в статистике");
        }
        
        return (double) getSum() / numbers.size();
    }
    
    /**
     * Возвращает медиану
     */
    public double getMedian() {
        if (numbers.isEmpty()) {
            throw new IllegalStateException("Нет чисел в статистике");
        }
        
        List<Integer> sorted = new ArrayList<>(numbers);
        Collections.sort(sorted);
        
        int size = sorted.size();
        if (size % 2 == 0) {
            return (sorted.get(size / 2 - 1) + sorted.get(size / 2)) / 2.0;
        } else {
            return sorted.get(size / 2);
        }
    }
    
    /**
     * Возвращает моды (наиболее часто встречающиеся числа)
     */
    public List<Integer> getModes() {
        if (numbers.isEmpty()) {
            return Collections.emptyList();
        }
        
        Map<Integer, Integer> frequencyMap = new HashMap<>();
        for (int number : numbers) {
            frequencyMap.put(number, frequencyMap.getOrDefault(number, 0) + 1);
        }
        
        int maxFrequency = Collections.max(frequencyMap.values());
        List<Integer> modes = new ArrayList<>();
        
        for (Map.Entry<Integer, Integer> entry : frequencyMap.entrySet()) {
            if (entry.getValue() == maxFrequency) {
                modes.add(entry.getKey());
            }
        }
        
        return modes;
    }
    
    /**
     * Возвращает стандартное отклонение
     */
    public double getStandardDeviation() {
        if (numbers.isEmpty()) {
            throw new IllegalStateException("Нет чисел в статистике");
        }
        
        double mean = getAverage();
        double sumSquaredDiff = 0;
        
        for (int number : numbers) {
            double diff = number - mean;
            sumSquaredDiff += diff * diff;
        }
        
        return Math.sqrt(sumSquaredDiff / numbers.size());
    }
    
    /**
     * Возвращает частотное распределение чисел
     */
    public Map<Integer, Integer> getFrequencyDistribution() {
        Map<Integer, Integer> distribution = new TreeMap<>();
        
        for (int number : numbers) {
            distribution.put(number, distribution.getOrDefault(number, 0) + 1);
        }
        
        return distribution;
    }
    
    /**
     * Очищает статистику
     */
    public void clear() {
        numbers.clear();
        positions.clear();
        totalNumbers = 0;
    }
    
    /**
     * Объединяет статистику с другой статистикой
     */
    public void merge(NumberStatistics other) {
        for (int i = 0; i < other.numbers.size(); i++) {
            addNumber(other.numbers.get(i));
        }
    }
    
    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append("Статистика чисел:\n");
        sb.append("Всего чисел: ").append(totalNumbers).append("\n");
        
        if (!numbers.isEmpty()) {
            sb.append("Минимум: ").append(getMin()).append("\n");
            sb.append("Максимум: ").append(getMax()).append("\n");
            sb.append("Сумма: ").append(getSum()).append("\n");
            sb.append("Среднее: ").append(String.format("%.2f", getAverage())).append("\n");
            sb.append("Медиана: ").append(String.format("%.2f", getMedian())).append("\n");
            sb.append("Стандартное отклонение: ").append(String.format("%.2f", getStandardDeviation())).append("\n");
            
            List<Integer> modes = getModes();
            if (!modes.isEmpty()) {
                sb.append("Мода(ы): ").append(modes).append("\n");
            }
        }
        
        return sb.toString();
    }
    
    /**
     * Экспортирует статистику в форматированную строку
     */
    public String exportStatistics() {
        StringBuilder sb = new StringBuilder();
        
        for (int i = 0; i < numbers.size(); i++) {
            sb.append(numbers.get(i)).append(" ").append(i + 1).append("\n");
        }
        
        return sb.toString();
    }
}