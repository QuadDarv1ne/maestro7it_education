/**
 * Проект: Word Statistics Plus Plus - Расширенный анализатор статистики слов
 * 
 * Программа для подсчета статистики встречаемости слов в тексте с сохранением порядка их появления и позиций каждого вхождения.
 * 
 * Основные возможности:
 * - Подсчет частоты слов с учетом регистра (приведение к нижнему)
 * - Сохранение порядка первого появления слов
 * - Вывод позиций каждого слова в тексте
 * - Поддержка Unicode символов (кириллица, дефисы, апострофы)
 * - Линейная производительность O(n)
 * 
 * <p> Запуск: java WordStatPlusPlus <входной-файл> <выходной-файл>
 */

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.*;

public class WordStatPlusPlus {
    /**
     * Точка входа в программу.
     * 
     * <p>Обрабатывает аргументы командной строки и запускает обработку файлов.
     * 
     * @param args аргументы командной строки:
     *             args[0] - путь к входному файлу (UTF-8)
     *             args[1] - путь к выходному файлу (UTF-8)
     * 
     * @throws IllegalArgumentException если количество аргументов некорректно
     */

    public static void main(String[] args) {
        // Проверяем количество аргументов
        if (args.length != 2) {
            System.err.println("Ошибка: Неверное количество аргументов.");
            System.err.println("Использование: java WordStatPlusPlus <входной-файл> <выходной-файл>");
            System.err.println("Пример: java WordStatPlusPlus input.txt output.txt");
            System.exit(1);
        }

        // Создание двух переменных для работы с данными
        String inputFile = args[0]; // входные данные
        String outputFile = args[1]; // выходные данные (после обработки)

        try {
            long startTime = System.currentTimeMillis();
            
            // Обрабатываем файл
            processFile(inputFile, outputFile);
            
            long endTime = System.currentTimeMillis();
            System.out.printf("Обработка завершена за %d мс%n", endTime - startTime);
            
        } catch (FileNotFoundException e) {
            System.err.println("Ошибка: Файл не найден - " + e.getMessage());
            System.exit(2);
        } catch (IOException e) {
            System.err.println("Ошибка ввода-вывода: " + e.getMessage());
            System.exit(3);
        } catch (Exception e) {
            System.err.println("Неожиданная ошибка: " + e.getMessage());
            e.printStackTrace();
            System.exit(4);
        }
    }

     /**
     * Основной метод обработки файлов.
     * 
     * <p>Выполняет следующие шаги:
     * 1. Создает сканер для чтения слов из входного файла
     * 2. Собирает статистику по словам (частота и позиции)
     * 3. Сохраняет порядок первого появления слов
     * 4. Записывает результаты в выходной файл
     * 
     * <p>Сложность: O(n), где n - количество символов во входном файле
     * 
     * @param inputFile путь к входному файлу в кодировке UTF-8
     * @param outputFile путь к выходному файлу в кодировке UTF-8
     * @throws IOException если возникает ошибка чтения или записи
     */

    private static void processFile(String inputFile, String outputFile) throws IOException {
        // Статистика для отладки
        int totalWords = 0;
        int uniqueWords = 0;
        
        // Используем LinkedHashMap для сохранения порядка добавления данных
        Map<String, IntList> wordPositions = new LinkedHashMap<>();
        WordScanner scanner = null;
        
        try {
            // Открываем сканер для чтения слов
            scanner = new WordScanner(new FileInputStream(inputFile));
            int wordCounter = 0;
            String word;
            
            // Считываем слова одно за другим
            while ((word = scanner.nextWord()) != null) {
                wordCounter++;
                totalWords++;
                word = word.toLowerCase(); // Приводим к нижнему регистру
                
                // Добавляем позицию слова в статистику
                IntList positions = wordPositions.get(word);
                if (positions == null) {
                    // Первое вхождение слова
                    positions = new IntList();
                    wordPositions.put(word, positions);
                    uniqueWords++;
                }
                positions.add(wordCounter);
            }
            
            // Выводим статистику в консоль
            System.out.printf("Обработано слов: %d (уникальных: %d)%n", totalWords, uniqueWords);
            
            // Записываем результаты в файл
            writeOutput(outputFile, wordPositions);
            
        } finally {
            // Закрываем сканер, если он был открыт
            if (scanner != null) {
                scanner.close();
            }
        }
    }

    /**
     * Записываем статистику слов в выходной файл.
     * 
     * <p>Формат каждой строки выводы:
     * <слово> <количество_вхождений> <позиция1> <позиция2> ...
     * 
     * <p>Пример: "hello 3 1 4 7"
     * 
     * @param outputFile путь к входному файлу с данными
     * @param wordPositions отображение слов на их позиции в тексте
     * @throws IOException если возникает ошибка записи
     */

    private static void writeOutput(String outputFile, Map<String, IntList> wordPositions) 
            throws IOException {
        
        try (BufferedWriter writer = new BufferedWriter(
                new OutputStreamWriter(new FileOutputStream(outputFile), StandardCharsets.UTF_8))) {
            
            // Для каждого слова в порядке первого появления
            for (Map.Entry<String, IntList> entry : wordPositions.entrySet()) {
                String word = entry.getKey();
                IntList positions = entry.getValue();
                
                // Формируем строку: слово + количество + позиции
                StringBuilder line = new StringBuilder();
                line.append(word).append(" ").append(positions.size());
                
                for (int i = 0; i < positions.size(); i++) {
                    line.append(" ").append(positions.get(i));
                }
                
                // Записываем строку в файл
                writer.write(line.toString());
                writer.newLine();
            }
        }
        
        System.out.printf("Результаты записаны в файл: %s%n", outputFile);
    }
}
