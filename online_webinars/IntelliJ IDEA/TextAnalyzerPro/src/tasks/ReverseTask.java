package tasks;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * Решение задачи "Реверс"
 * Читает матрицу чисел и выводит её в обратном порядке
 */
public class ReverseTask {

    /**
     * Обрабатывает входной файл и записывает результат в выходной
     */
    public static void processFile(String inputFile, String outputFile) throws IOException {
        List<List<Integer>> matrix = readMatrix(inputFile);
        writeReversedMatrix(outputFile, matrix);
    }

    /**
     * Читает матрицу чисел из файла
     */
    private static List<List<Integer>> readMatrix(String inputFile) throws IOException {
        List<List<Integer>> matrix = new ArrayList<>();

        try (BufferedReader reader = new BufferedReader(
                new InputStreamReader(new FileInputStream(inputFile), StandardCharsets.UTF_8))) {

            String line;
            while ((line = reader.readLine()) != null) {
                List<Integer> row = parseNumbersFromLine(line);
                if (!row.isEmpty()) {
                    matrix.add(row);
                }
            }
        }

        return matrix;
    }

    /**
     * Парсит числа из строки
     */
    private static List<Integer> parseNumbersFromLine(String line) {
        List<Integer> numbers = new ArrayList<>();
        String[] parts = line.trim().split("\\s+");

        for (String part : parts) {
            try {
                numbers.add(Integer.parseInt(part));
            } catch (NumberFormatException e) {
                // Игнорируем нечисловые части
            }
        }

        return numbers;
    }

    /**
     * Записывает матрицу в обратном порядке
     */
    private static void writeReversedMatrix(String outputFile, List<List<Integer>> matrix)
            throws IOException {

        try (BufferedWriter writer = new BufferedWriter(
                new OutputStreamWriter(new FileOutputStream(outputFile), StandardCharsets.UTF_8))) {

            // Обратный порядок строк
            for (int i = matrix.size() - 1; i >= 0; i--) {
                List<Integer> row = matrix.get(i);
                List<Integer> reversedRow = new ArrayList<>(row);
                Collections.reverse(reversedRow);

                // Записываем числа в строке в обратном порядке
                for (int j = 0; j < reversedRow.size(); j++) {
                    writer.write(reversedRow.get(j).toString());
                    if (j < reversedRow.size() - 1) {
                        writer.write(" ");
                    }
                }

                if (i > 0) {
                    writer.newLine();
                }
            }
        }
    }

    /**
     * Основной метод для запуска из командной строки
     */
    public static void main(String[] args) {
        if (args.length != 2) {
            System.err.println("Использование: java ReverseTask <входной-файл> <выходной-файл>");
            System.err.println("Пример: java ReverseTask input.txt output.txt");
            return;
        }

        try {
            long startTime = System.currentTimeMillis();

            processFile(args[0], args[1]);

            long endTime = System.currentTimeMillis();
            System.out.printf("Результат записан в файл: %s%n", args[1]);
            System.out.printf("Время выполнения: %d мс%n", endTime - startTime);

        } catch (FileNotFoundException e) {
            System.err.println("Ошибка: Файл не найден - " + e.getMessage());
        } catch (IOException e) {
            System.err.println("Ошибка ввода-вывода: " + e.getMessage());
        } catch (Exception e) {
            System.err.println("Неожиданная ошибка: " + e.getMessage());
            e.printStackTrace();
        }
    }
}