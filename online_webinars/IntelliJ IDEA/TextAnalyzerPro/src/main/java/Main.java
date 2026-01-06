import analyzer.AppConfig;
import tasks.ReverseTask;
import tasks.WordStatPlusTask;
import tasks.TextStatTask;
//import tasks.TopWordsTask;
import tasks.WordLengthTask;
import java.util.Scanner;

/**
 * Главный класс приложения TextAnalyzerPro
 */
public class Main {

    public static void main(String[] args) {
        System.out.println("TextAnalyzerPro v" + AppConfig.VERSION);
        System.out.println();

        if (args.length == 0) {
            runInteractiveMode();
            return;
        }

        String command = args[0].toLowerCase();

        try {
            switch (command) {
                case "reverse":
                    if (args.length == 3) {
                        if (!new java.io.File(args[1]).exists()) {
                            System.err.println("Ошибка: Входной файл не найден: " + args[1]);
                            return;
                        }
                        if (new java.io.File(args[1]).length() > AppConfig.MAX_FILE_SIZE) {
                            System.err.println("Ошибка: Файл слишком большой (макс. " + AppConfig.MAX_FILE_SIZE / (1024 * 1024) + "MB)");
                            return;
                        }
                        ReverseTask.main(new String[]{args[1], args[2]});
                    } else {
                        printUsage();
                    }
                    break;

                case "wordstat":
                case "wordstatplus":
                    if (args.length == 3) {
                        if (!new java.io.File(args[1]).exists()) {
                            System.err.println("Ошибка: Входной файл не найден: " + args[1]);
                            return;
                        }
                        if (new java.io.File(args[1]).length() > AppConfig.MAX_FILE_SIZE) {
                            System.err.println("Ошибка: Файл слишком большой (макс. " + AppConfig.MAX_FILE_SIZE / (1024 * 1024) + "MB)");
                            return;
                        }
                        WordStatPlusTask.main(new String[]{args[1], args[2]});
                    } else {
                        printUsage();
                    }
                    break;

                case "textstat":
                    if (args.length == 3) {
                        if (!new java.io.File(args[1]).exists()) {
                            System.err.println("Ошибка: Входной файл не найден: " + args[1]);
                            return;
                        }
                        if (new java.io.File(args[1]).length() > AppConfig.MAX_FILE_SIZE) {
                            System.err.println("Ошибка: Файл слишком большой (макс. " + AppConfig.MAX_FILE_SIZE / (1024 * 1024) + "MB)");
                            return;
                        }
                        TextStatTask.main(new String[]{args[1], args[2]});
                    } else {
                        printUsage();
                    }
                    break;

                case "topwords":
                    if (args.length == 4) {
                        if (!new java.io.File(args[1]).exists()) {
                            System.err.println("Ошибка: Входной файл не найден: " + args[1]);
                            return;
                        }
                        if (new java.io.File(args[1]).length() > AppConfig.MAX_FILE_SIZE) {
                            System.err.println("Ошибка: Файл слишком большой (макс. " + AppConfig.MAX_FILE_SIZE / (1024 * 1024) + "MB)");
                            return;
                        }
                        // TopWordsTask.main(new String[]{args[1], args[2], args[3]});
                    } else {
                        printUsage();
                    }
                    break;

                case "wordlength":
                    if (args.length == 3) {
                        if (!new java.io.File(args[1]).exists()) {
                            System.err.println("Ошибка: Входной файл не найден: " + args[1]);
                            return;
                        }
                        if (new java.io.File(args[1]).length() > AppConfig.MAX_FILE_SIZE) {
                            System.err.println("Ошибка: Файл слишком большой (макс. " + AppConfig.MAX_FILE_SIZE / (1024 * 1024) + "MB)");
                            return;
                        }
                        WordLengthTask.main(new String[]{args[1], args[2]});
                    } else {
                        printUsage();
                    }
                    break;

                case "config":
                    AppConfig.printConfig();
                    break;

                case "help":
                    printHelp();
                    break;

                default:
                    System.err.println("Неизвестная команда: " + command);
                    printUsage();
                    break;
            }
        } catch (Exception e) {
            System.err.println("Ошибка: " + e.getMessage());
            e.printStackTrace();
        }
    }

    private static void runInteractiveMode() {
        Scanner consoleScanner = new Scanner(System.in, "UTF-8");

        System.out.println("╔════════════════════════════════════╗");
        System.out.println("║      TextAnalyzerPro v1.0          ║");
        System.out.println("╚════════════════════════════════════╝");
        System.out.println();
        System.out.println("Доступные задачи:");
        System.out.println("1. Реверс (обратный порядок чисел)");
        System.out.println("2. Статистика слов++ (частоты и позиции)");
        System.out.println("3. Комплексная статистика текста");
        System.out.println("4. Топ слов (наиболее частые слова)");
        System.out.println("5. Анализ длины слов");
        System.out.println("6. Выход");
        System.out.println();

        while (true) {
            System.out.print("Выберите задачу (1-6): ");
            String choice = consoleScanner.nextLine().trim();

            switch (choice) {
                case "1":
                    runReverseTask(consoleScanner);
                    break;

                case "2":
                    runWordStatTask(consoleScanner);
                    break;

                case "3":
                    runTextStatTask(consoleScanner);
                    break;

                case "4":
                    // runTopWordsTask(consoleScanner);
                    break;

                case "5":
                    runWordLengthTask(consoleScanner);
                    break;

                case "6":
                    System.out.println("Выход из программы...");
                    consoleScanner.close();
                    return;

                default:
                    System.out.println("Неверный выбор. Попробуйте снова.");
                    break;
            }

            System.out.println();
        }
    }

    private static void runReverseTask(Scanner consoleScanner) {
        System.out.println("\n=== Задача 'Реверс' ===");
        System.out.print("Входной файл: ");
        String inputFile = consoleScanner.nextLine().trim();

        java.io.File file = new java.io.File(inputFile);
        if (!file.exists()) {
            System.err.println("✗ Ошибка: Входной файл не найден: " + inputFile);
            return;
        }
        if (file.length() > AppConfig.MAX_FILE_SIZE) {
            System.err.println("✗ Ошибка: Файл слишком большой (макс. " + AppConfig.MAX_FILE_SIZE / (1024 * 1024) + "MB)");
            return;
        }

        System.out.print("Выходной файл: ");
        String outputFile = consoleScanner.nextLine().trim();

        try {
            ReverseTask.processFile(inputFile, outputFile);
            System.out.println("✓ Задача успешно выполнена!");
            System.out.println("Результат сохранен в: " + outputFile);
        } catch (Exception e) {
            System.err.println("✗ Ошибка: " + e.getMessage());
        }
    }

    private static void runWordStatTask(Scanner consoleScanner) {
        System.out.println("\n=== Задача 'Статистика слов++' ===");
        System.out.print("Входной файл: ");
        String inputFile = consoleScanner.nextLine().trim();

        java.io.File file = new java.io.File(inputFile);
        if (!file.exists()) {
            System.err.println("✗ Ошибка: Входной файл не найден: " + inputFile);
            return;
        }
        if (file.length() > AppConfig.MAX_FILE_SIZE) {
            System.err.println("✗ Ошибка: Файл слишком большой (макс. " + AppConfig.MAX_FILE_SIZE / (1024 * 1024) + "MB)");
            return;
        }

        System.out.print("Выходной файл: ");
        String outputFile = consoleScanner.nextLine().trim();

        try {
            WordStatPlusTask.processFile(inputFile, outputFile);
            System.out.println("✓ Задача успешно выполнена!");
            System.out.println("Статистика сохранена в: " + outputFile);
        } catch (Exception e) {
            System.err.println("✗ Ошибка: " + e.getMessage());
        }
    }

    private static void runTextStatTask(Scanner consoleScanner) {
        System.out.println("\n=== Задача 'Комплексная статистика текста' ===");
        System.out.print("Входной файл: ");
        String inputFile = consoleScanner.nextLine().trim();

        java.io.File file = new java.io.File(inputFile);
        if (!file.exists()) {
            System.err.println("✗ Ошибка: Входной файл не найден: " + inputFile);
            return;
        }
        if (file.length() > AppConfig.MAX_FILE_SIZE) {
            System.err.println("✗ Ошибка: Файл слишком большой (макс. " + AppConfig.MAX_FILE_SIZE / (1024 * 1024) + "MB)");
            return;
        }

        System.out.print("Выходной файл: ");
        String outputFile = consoleScanner.nextLine().trim();

        try {
            TextStatTask.processFile(inputFile, outputFile);
            System.out.println("✓ Задача успешно выполнена!");
            System.out.println("Отчёт сохранён в: " + outputFile);
        } catch (Exception e) {
            System.err.println("✗ Ошибка: " + e.getMessage());
        }
    }

    private static void runWordLengthTask(Scanner consoleScanner) {
        System.out.println("\n=== Задача 'Анализ длины слов' ===");
        System.out.print("Входной файл: ");
        String inputFile = consoleScanner.nextLine().trim();

        java.io.File file = new java.io.File(inputFile);
        if (!file.exists()) {
            System.err.println("✗ Ошибка: Входной файл не найден: " + inputFile);
            return;
        }
        if (file.length() > AppConfig.MAX_FILE_SIZE) {
            System.err.println("✗ Ошибка: Файл слишком большой (макс. " + AppConfig.MAX_FILE_SIZE / (1024 * 1024) + "MB)");
            return;
        }

        System.out.print("Выходной файл: ");
        String outputFile = consoleScanner.nextLine().trim();

        try {
            WordLengthTask.processFile(inputFile, outputFile);
            System.out.println("✓ Задача успешно выполнена!");
            System.out.println("Анализ длин слов сохранён в: " + outputFile);
        } catch (Exception e) {
            System.err.println("✗ Ошибка: " + e.getMessage());
        }
    }

    private static void printUsage() {
        System.err.println("Использование:");
        System.err.println("  java Main <команда> <входной-файл> <выходной-файл> [параметры]");
        System.err.println();
        System.err.println("Команды:");
        System.err.println("  reverse     - задача 'Реверс'");
        System.err.println("  wordstat    - задача 'Статистика слов++'");
        System.err.println("  textstat    - комплексная статистика текста");
        System.err.println("  topwords    - топ наиболее частых слов (требует <топ-N>)");
        System.err.println("  wordlength  - анализ длины слов");
        System.err.println("  config      - показать конфигурацию");
        System.err.println("  help        - показать эту справку");
        System.err.println();
        System.err.println("Примеры:");
        System.err.println("  java Main reverse input.txt output.txt");
        System.err.println("  java Main wordstat text.txt stats.txt");
        System.err.println("  java Main textstat text.txt report.txt");
        System.err.println("  java Main topwords text.txt top.txt 10");
        System.err.println("  java Main config");
    }

    private static void printHelp() {
        System.out.println("TextAnalyzerPro - Анализатор текста на Java");
        System.out.println();
        System.out.println("Задачи:");
        System.out.println("1. Реверс:");
        System.out.println("   Читает матрицу чисел из файла и выводит её");
        System.out.println("   в обратном порядке (строки и числа в строках)");
        System.out.println();
        System.out.println("2. Статистика слов++:");
        System.out.println("   Подсчитывает частоту каждого слова в тексте");
        System.out.println("   и выводит слова в порядке их первого появления");
        System.out.println("   с указанием количества и позиций каждого слова");
        System.out.println();
        System.out.println("3. Комплексная статистика текста:");
        System.out.println("   Выполняет полный анализ текста: подсчёт символов,");
        System.out.println("   слов, предложений, строк, распределение длин слов,");
        System.out.println("   самые частые и длинные слова и др.");
        System.out.println();
        System.out.println("4. Топ слов:");
        System.out.println("   Выводит топ N наиболее частых слов в тексте");
        System.out.println("   отсортированных по частоте (убывание) и алфавиту");
        System.out.println();
        System.out.println("5. Анализ длины слов:");
        System.out.println("   Выполняет статистический анализ длин слов в тексте");
        System.out.println("   показывает распределение по длинам и общую статистику");
        System.out.println();
        System.out.println("Формат вывода для Статистики слов++:");
        System.out.println("   слово количество позиция1 позиция2 ...");
        System.out.println();
        System.out.println("Формат вывода для Топ слов:");
        System.out.println("   слово частота");
        System.out.println();
        System.out.println("Формат вывода для Анализа длины слов:");
        System.out.println("   длина_слова количество_слов");
        System.out.println();
        System.out.println("Поддерживаемые кодировки: UTF-8");
        System.out.println("Поддержка Unicode: полная (кириллица, эмодзи и др.)");
    }
}