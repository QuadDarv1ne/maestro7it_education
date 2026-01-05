package analyzer.utils;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

/**
 * Простой логгер для приложения TextAnalyzerPro
 */
public class Logger {
    private static final String LOG_FILE = AppConfig.LOG_FILE;
    private static final boolean LOGGING_ENABLED = AppConfig.LOGGING_ENABLED;
    private static final DateTimeFormatter TIMESTAMP_FORMAT = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
    
    public enum Level {
        INFO, WARN, ERROR, DEBUG
    }
    
    /**
     * Логирует информационное сообщение
     */
    public static void info(String message) {
        log(Level.INFO, message);
    }
    
    /**
     * Логирует предупреждение
     */
    public static void warn(String message) {
        log(Level.WARN, message);
    }
    
    /**
     * Логирует ошибку
     */
    public static void error(String message) {
        log(Level.ERROR, message);
    }
    
    /**
     * Логирует отладочное сообщение
     */
    public static void debug(String message) {
        log(Level.DEBUG, message);
    }
    
    /**
     * Логирует сообщение с указанным уровнем
     */
    public static void log(Level level, String message) {
        if (!LOGGING_ENABLED) {
            return;
        }
        
        String timestamp = LocalDateTime.now().format(TIMESTAMP_FORMAT);
        String logEntry = String.format("[%s] [%s] %s%n", timestamp, level.name(), message);
        
        // Вывод в консоль для уровней WARN и ERROR
        if (level == Level.WARN || level == Level.ERROR) {
            System.err.print(logEntry);
        } else {
            System.out.print(logEntry);
        }
        
        // Запись в файл
        try (BufferedWriter writer = new BufferedWriter(
                new OutputStreamWriter(new FileOutputStream(LOG_FILE, true), StandardCharsets.UTF_8))) {
            writer.write(logEntry);
        } catch (IOException e) {
            System.err.println("Ошибка записи в лог-файл: " + e.getMessage());
        }
    }
    
    /**
     * Логирует начало выполнения задачи
     */
    public static void logTaskStart(String taskName, String inputFile) {
        info(String.format("Начало выполнения задачи '%s' для файла: %s", taskName, inputFile));
    }
    
    /**
     * Логирует завершение выполнения задачи
     */
    public static void logTaskEnd(String taskName, String outputFile, long durationMs) {
        info(String.format("Задача '%s' завершена. Результат сохранен в: %s. Время выполнения: %d мс",
                          taskName, outputFile, durationMs));
    }
    
    /**
     * Логирует ошибку выполнения задачи
     */
    public static void logTaskError(String taskName, String errorMessage) {
        error(String.format("Ошибка выполнения задачи '%s': %s", taskName, errorMessage));
    }
}