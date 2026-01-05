/**
 * Конфигурация приложения
 */
public class AppConfig {
    // Версия приложения
    public static final String VERSION = "1.0.0";
    
    // Кодировка по умолчанию
    public static final String DEFAULT_ENCODING = "UTF-8";
    
    // Размер буфера по умолчанию для сканера
    public static final int DEFAULT_BUFFER_SIZE = 8192;
    
    // Максимальная длина токена
    public static final int MAX_TOKEN_LENGTH = 65536;
    
    // Пути по умолчанию
    public static final String DEFAULT_INPUT_DIR = "input";
    public static final String DEFAULT_OUTPUT_DIR = "output";
    public static final String DEFAULT_TEST_DIR = "test";
    
    // Настройки логирования
    public static final boolean LOGGING_ENABLED = true;
    public static final String LOG_FILE = "text_analyzer.log";
    
    // Настройки производительности
    public static final boolean USE_PARALLEL_PROCESSING = false;
    public static final int MAX_THREADS = Runtime.getRuntime().availableProcessors();
    
    /**
     * Выводит информацию о конфигурации
     */
    public static void printConfig() {
        System.out.println("TextAnalyzerPro Configuration:");
        System.out.println("Version: " + VERSION);
        System.out.println("Default Encoding: " + DEFAULT_ENCODING);
        System.out.println("Default Buffer Size: " + DEFAULT_BUFFER_SIZE);
        System.out.println("Max Token Length: " + MAX_TOKEN_LENGTH);
        System.out.println("Logging Enabled: " + LOGGING_ENABLED);
        System.out.println("Parallel Processing: " + USE_PARALLEL_PROCESSING);
        System.out.println("Available Processors: " + MAX_THREADS);
    }
}