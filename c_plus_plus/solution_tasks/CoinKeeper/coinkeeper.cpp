#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <fstream>
#include <sstream>
#include <ctime>
#include <iomanip>
#include <algorithm>

// Структура для хранения транзакции
struct Transaction {
    std::string date;
    std::string category;
    int amount;
    std::string description;
};

// Структура для хранения финансовой цели
struct Goal {
    std::string description;
    int targetAmount;
    int currentAmount;
};

// Структура для хранения бюджета
struct Budget {
    std::string category;
    int limit;
};

// Структура для хранения напоминания
struct Reminder {
    std::string date;
    std::string description;
};

// Класс для управления финансами
class FinanceManager {
private:
    std::vector<Transaction> transactions; // История транзакций
    std::map<std::string, int> categories; // Категории доходов/расходов
    std::vector<Goal> goals;               // Финансовые цели
    std::vector<Budget> budgets;           // Лимиты бюджета
    std::vector<Reminder> reminders;       // Напоминания
    int balance;                           // Текущий баланс

public:
    FinanceManager() : balance(0) {}

    // Добавление транзакции
    void addTransaction(const std::string& date, const std::string& category, int amount, const std::string& description) {
        transactions.push_back({date, category, amount, description});
        balance += amount;
        categories[category] += amount; // Обновляем сумму по категории
    }

    // Установка финансовой цели
    void setGoal(const std::string& description, int targetAmount) {
        goals.push_back({description, targetAmount, 0});
    }

    // Проверка целей
    void checkGoals() {
        for (auto& goal : goals) {
            if (balance >= goal.targetAmount && goal.currentAmount < goal.targetAmount) {
                goal.currentAmount = goal.targetAmount;
                std::cout << "Цель достигнута: " << goal.description << "!\n";
            }
        }
    }

    // Установка лимита бюджета
    void setBudget(const std::string& category, int limit) {
        budgets.push_back({category, limit});
    }

    // Проверка бюджета
    void checkBudget() {
        for (const auto& budget : budgets) {
            int spent = categories[budget.category];
            if (spent > budget.limit) {
                std::cout << "Внимание! Лимит по категории '" << budget.category << "' превышен: " << spent << "/" << budget.limit << "\n";
            }
        }
    }

    // Добавление напоминания
    void addReminder(const std::string& date, const std::string& description) {
        reminders.push_back({date, description});
    }

    // Проверка напоминаний
    void checkReminders(const std::string& currentDate) {
        for (const auto& reminder : reminders) {
            if (reminder.date == currentDate) {
                std::cout << "Напоминание: " << reminder.description << " (Дата: " << reminder.date << ")\n";
            }
        }
    }

    // Вывод статистики
    void printStatistics() {
        std::cout << "\n--- Статистика ---\n";
        std::cout << "Текущий баланс: " << balance << " рублей\n";
        std::cout << "Расходы по категориям:\n";
        for (const auto& [category, amount] : categories) {
            if (amount < 0) {
                std::cout << category << ": " << -amount << " рублей\n";
            }
        }
        std::cout << "Доходы по категориям:\n";
        for (const auto& [category, amount] : categories) {
            if (amount > 0) {
                std::cout << category << ": " << amount << " рублей\n";
            }
        }
    }

    // Сохранение данных в файл
    void saveToFile(const std::string& filename) {
        std::ofstream file(filename);
        for (const auto& transaction : transactions) {
            file << transaction.date << "," << transaction.category << "," << transaction.amount << "," << transaction.description << "\n";
        }
        std::cout << "Данные сохранены в файл: " << filename << "\n";
    }

    // Загрузка данных из файла
    void loadFromFile(const std::string& filename) {
        std::ifstream file(filename);
        std::string line;
        while (std::getline(file, line)) {
            std::string date, category, amountStr, description;
            std::istringstream ss(line);
            std::getline(ss, date, ',');
            std::getline(ss, category, ',');
            std::getline(ss, amountStr, ',');
            std::getline(ss, description, ',');
            addTransaction(date, category, std::stoi(amountStr), description);
        }
        std::cout << "Данные загружены из файла: " << filename << "\n";
    }

    // Получение текущей даты
    static std::string getCurrentDate() {
        std::time_t t = std::time(nullptr);
        std::tm tm = *std::localtime(&t);
        std::ostringstream oss;
        oss << std::put_time(&tm, "%d.%m.%Y");
        return oss.str();
    }

    // Вывод меню
    void printMenu() {
        std::cout << "\n--- Меню ---\n";
        std::cout << "1. Добавить транзакцию\n";
        std::cout << "2. Установить финансовую цель\n";
        std::cout << "3. Установить лимит бюджета\n";
        std::cout << "4. Добавить напоминание\n";
        std::cout << "5. Показать статистику\n";
        std::cout << "6. Проверить напоминания\n";
        std::cout << "7. Сохранить данные\n";
        std::cout << "8. Загрузить данные\n";
        std::cout << "9. Выйти\n";
    }
};

// Основная функция
int main() {
    FinanceManager manager;
    std::string currentDate = FinanceManager::getCurrentDate();
    int choice;

    // Загрузка данных из файла (если есть)
    manager.loadFromFile("transactions.csv");

    while (true) {
        manager.printMenu();
        std::cout << "Выберите действие: ";
        std::cin >> choice;
        std::cin.ignore(); // Игнорируем оставшийся символ новой строки

        switch (choice) {
            case 1: {
                std::string date, category, description;
                int amount;

                std::cout << "Введите дату (дд.мм.гггг): ";
                std::getline(std::cin, date);
                std::cout << "Введите категорию: ";
                std::getline(std::cin, category);
                std::cout << "Введите сумму: ";
                std::cin >> amount;
                std::cin.ignore();
                std::cout << "Введите описание: ";
                std::getline(std::cin, description);

                manager.addTransaction(date, category, amount, description);
                break;
            }
            case 2: {
                std::string description;
                int targetAmount;

                std::cout << "Введите описание цели: ";
                std::getline(std::cin, description);
                std::cout << "Введите целевую сумму: ";
                std::cin >> targetAmount;
                std::cin.ignore();

                manager.setGoal(description, targetAmount);
                break;
            }
            case 3: {
                std::string category;
                int limit;

                std::cout << "Введите категорию: ";
                std::getline(std::cin, category);
                std::cout << "Введите лимит: ";
                std::cin >> limit;
                std::cin.ignore();

                manager.setBudget(category, limit);
                break;
            }
            case 4: {
                std::string date, description;

                std::cout << "Введите дату напоминания (дд.мм.гггг): ";
                std::getline(std::cin, date);
                std::cout << "Введите описание напоминания: ";
                std::getline(std::cin, description);

                manager.addReminder(date, description);
                break;
            }
            case 5:
                manager.printStatistics();
                break;
            case 6:
                manager.checkReminders(currentDate);
                break;
            case 7:
                manager.saveToFile("transactions.csv");
                break;
            case 8:
                manager.loadFromFile("transactions.csv");
                break;
            case 9:
                std::cout << "Выход из программы.\n";
                return 0;
            default:
                std::cout << "Неверный выбор. Попробуйте снова.\n";
        }
    }

    return 0;
}
