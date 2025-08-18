#include <iostream>
#include <string>
#include <vector>

using namespace std;

void greet(string name, string surname, string patronomic, 
           string profession, int start_year, vector<string> skills) {
    // Обработка некорректного года
    string experience_str;
    string motivation = "";
    bool show_motivation = true;

    if (start_year > 2025) {
        experience_str = "в будущем (" + to_string(start_year) + ")";
        show_motivation = false;
    }
    else if (start_year < 1900) {
        experience_str = "более 125 лет (проверьте данные)";
        show_motivation = false;
    }
    else {
        int experience = 2025 - start_year;
        
        // Определение правильного окончания для стажа
        if (experience % 100 >= 11 && experience % 100 <= 14) {
            experience_str = to_string(experience) + " лет";
        }
        else {
            switch (experience % 10) {
                case 1: experience_str = to_string(experience) + " год"; break;
                case 2: case 3: case 4: experience_str = to_string(experience) + " года"; break;
                default: experience_str = to_string(experience) + " лет"; break;
            }
        }
        
        // Выбор мотивационной фразы
        if (experience <= 1) {
            motivation = "Желаем продуктивной работы в нашей команде";
        }
        else if (experience >= 2 && experience <= 5) {
            motivation = "Ваш опыт — наша сила";
        }
        else {
            motivation = "Вы — легенда компании";
        }
    }

    // Определение обращения по полу
    string greeting = "Уважаемый(ая)";
    if (!patronomic.empty()) {
        if (patronomic.size() >= 2 && 
            patronomic.substr(patronomic.size() - 2) == "ич") {
            greeting = "Уважаемый";
        }
        else if (patronomic.size() >= 2 && 
                 patronomic.substr(patronomic.size() - 2) == "на") {
            greeting = "Уважаемая";
        }
    }

    // Форматирование списка навыков
    string skills_str;
    if (skills.empty()) {
        skills_str = "Навыки не указаны";
    }
    else if (skills.size() <= 5) {
        for (size_t i = 0; i < skills.size(); ++i) {
            skills_str += skills[i];
            if (i < skills.size() - 1) skills_str += ", ";
        }
    }
    else {
        for (int i = 0; i < 5; ++i) {
            skills_str += skills[i];
            if (i < 4) skills_str += ", ";
        }
        skills_str += ", и еще " + to_string(skills.size() - 5);
    }

    // Вывод информации
    cout << "\n" << greeting << " " << surname << " " << name << " " << patronomic << " ...\n";
    cout << "Профессия: " << profession << endl;
    cout << "Стаж работы: " << experience_str << endl;
    cout << "Навыки: " << skills_str << endl;
    if (show_motivation && !motivation.empty()) {
        cout << motivation << endl;
    }
}

int main() {
    // Вызов функции с дополнительными параметрами
    greet("Максим", "Дуплей", "Игоревич", 
          "DevOps-инженер и преподаватель", 
          2019, 
          {"C++", "Python", "Алгоритмы", "ООП", "Java", "JavaScript", "C#", "Assembler", "Database", "SQL", "Figma", "Video-maker"});
    
    // Дополнительные тестовые примеры
    greet("Анна", "Иванова", "Петровна",
          "Программист",
          2024,
          {"C++", "Python"});
    
    greet("Иван", "Петров", "",
          "Аналитик",
          2030,
          {"Excel"});
    
    greet("Сергей", "Сидоров", "Николаевич",
        "Дизайнер",
        1800,
        {"Photoshop", "Illustrator", "Figma"});

    return 0;
}