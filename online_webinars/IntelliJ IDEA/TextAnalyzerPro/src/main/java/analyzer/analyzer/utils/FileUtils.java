package analyzer.utils;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

/**
 * Утилиты для работы с файлами
 */
public class FileUtils {

    private FileUtils() {
        // Утилитарный класс
    }

    /**
     * Читает весь файл в строку с указанной кодировкой
     */
    public static String readFile(String filePath, String charsetName) throws IOException {
        byte[] bytes = Files.readAllBytes(Paths.get(filePath));
        return new String(bytes, charsetName);
    }

    /**
     * Читает весь файл в строку с кодировкой UTF-8
     */
    public static String readFileUTF8(String filePath) throws IOException {
        return readFile(filePath, StandardCharsets.UTF_8.name());
    }

    /**
     * Читает файл построчно в список строк
     */
    public static List<String> readLines(String filePath, String charsetName) throws IOException {
        List<String> lines = new ArrayList<>();

        try (BufferedReader reader = new BufferedReader(
                new InputStreamReader(new FileInputStream(filePath), charsetName))) {

            String line;
            while ((line = reader.readLine()) != null) {
                lines.add(line);
            }
        }

        return lines;
    }

    /**
     * Читает файл построчно в список строк с кодировкой UTF-8
     */
    public static List<String> readLinesUTF8(String filePath) throws IOException {
        return readLines(filePath, StandardCharsets.UTF_8.name());
    }

    /**
     * Записывает строку в файл с указанной кодировкой
     */
    public static void writeFile(String filePath, String content, String charsetName) throws IOException {
        try (BufferedWriter writer = new BufferedWriter(
                new OutputStreamWriter(new FileOutputStream(filePath), charsetName))) {
            writer.write(content);
        }
    }

    /**
     * Записывает строку в файл с кодировкой UTF-8
     */
    public static void writeFileUTF8(String filePath, String content) throws IOException {
        writeFile(filePath, content, StandardCharsets.UTF_8.name());
    }

    /**
     * Записывает список строк в файл
     */
    public static void writeLines(String filePath, List<String> lines, String charsetName) throws IOException {
        try (BufferedWriter writer = new BufferedWriter(
                new OutputStreamWriter(new FileOutputStream(filePath), charsetName))) {

            for (int i = 0; i < lines.size(); i++) {
                writer.write(lines.get(i));
                if (i < lines.size() - 1) {
                    writer.newLine();
                }
            }
        }
    }

    /**
     * Записывает список строк в файл с кодировкой UTF-8
     */
    public static void writeLinesUTF8(String filePath, List<String> lines) throws IOException {
        writeLines(filePath, lines, StandardCharsets.UTF_8.name());
    }

    /**
     * Копирует файл
     */
    public static void copyFile(String sourcePath, String destPath) throws IOException {
        Files.copy(Paths.get(sourcePath), Paths.get(destPath));
    }

    /**
     * Удаляет файл
     */
    public static boolean deleteFile(String filePath) {
        try {
            return Files.deleteIfExists(Paths.get(filePath));
        } catch (IOException e) {
            return false;
        }
    }

    /**
     * Создает директорию, если она не существует
     */
    public static void createDirectory(String dirPath) throws IOException {
        Path path = Paths.get(dirPath);
        if (!Files.exists(path)) {
            Files.createDirectories(path);
        }
    }

    /**
     * Проверяет существование файла
     */
    public static boolean fileExists(String filePath) {
        return Files.exists(Paths.get(filePath));
    }

    /**
     * Получает размер файла в байтах
     */
    public static long getFileSize(String filePath) throws IOException {
        return Files.size(Paths.get(filePath));
    }

    /**
     * Получает расширение файла
     */
    public static String getFileExtension(String filePath) {
        if (filePath == null) {
            return "";
        }

        int lastDotIndex = filePath.lastIndexOf('.');
        if (lastDotIndex == -1 || lastDotIndex == filePath.length() - 1) {
            return "";
        }

        return filePath.substring(lastDotIndex + 1);
    }

    /**
     * Получает имя файла без расширения
     */
    public static String getFileNameWithoutExtension(String filePath) {
        if (filePath == null) {
            return "";
        }

        String fileName = Paths.get(filePath).getFileName().toString();
        int lastDotIndex = fileName.lastIndexOf('.');

        if (lastDotIndex == -1) {
            return fileName;
        }

        return fileName.substring(0, lastDotIndex);
    }

    /**
     * Получает имя файла с расширением
     */
    public static String getFileName(String filePath) {
        if (filePath == null) {
            return "";
        }

        Path path = Paths.get(filePath);
        return path.getFileName().toString();
    }

    /**
     * Получает родительскую директорию файла
     */
    public static String getParentDirectory(String filePath) {
        if (filePath == null) {
            return "";
        }

        Path parent = Paths.get(filePath).getParent();
        return parent != null ? parent.toString() : "";
    }

    /**
     * Читает файл и возвращает его содержимое в виде массива байтов
     */
    public static byte[] readFileBytes(String filePath) throws IOException {
        return Files.readAllBytes(Paths.get(filePath));
    }

    /**
     * Записывает массив байтов в файл
     */
    public static void writeFileBytes(String filePath, byte[] data) throws IOException {
        Files.write(Paths.get(filePath), data);
    }

    /**
     * Проверяет, является ли файл текстовым по расширению
     */
    public static boolean isTextFile(String filePath) {
        String extension = getFileExtension(filePath).toLowerCase();

        switch (extension) {
            case "txt":
            case "html":
            case "htm":
            case "xml":
            case "json":
            case "csv":
            case "java":
            case "c":
            case "cpp":
            case "h":
            case "hpp":
            case "py":
            case "js":
            case "css":
            case "php":
            case "sql":
            case "md":
            case "yml":
            case "yaml":
            case "properties":
                return true;
            default:
                return false;
        }
    }

    /**
     * Подсчитывает количество строк в файле
     */
    public static int countLines(String filePath, String charsetName) throws IOException {
        int lineCount = 0;

        try (BufferedReader reader = new BufferedReader(
                new InputStreamReader(new FileInputStream(filePath), charsetName))) {

            while (reader.readLine() != null) {
                lineCount++;
            }
        }

        return lineCount;
    }

    /**
     * Подсчитывает количество строк в файле с кодировкой UTF-8
     */
    public static int countLinesUTF8(String filePath) throws IOException {
        return countLines(filePath, StandardCharsets.UTF_8.name());
    }
}