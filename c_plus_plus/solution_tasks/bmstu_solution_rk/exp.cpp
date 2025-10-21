#include <iostream>
#include <vector>
#include <string>
#include <cmath>

// Функция ручного преобразования строки в число
double parseNumber(const char* str) {
    double result = 0.0;
    double fraction = 0.0;
    double divisor = 1.0;
    bool negative = false;
    bool afterDot = false;

    // Пропуск пробелов
    while (*str == ' ') str++;

    // Проверка знака
    if (*str == '-') {
        negative = true;
        str++;
    } else if (*str == '+') {
        str++;
    }

    // Основной цикл чтения числа
    while (*str != '\0' && *str != ';' && *str != '\n') {
        if (*str == '.') {
            afterDot = true;
        } else if (*str >= '0' && *str <= '9') {
            int digit = *str - '0';
            if (!afterDot) {
                result = result * 10 + digit;
            } else {
                divisor *= 10.0;
                fraction += digit / divisor;
            }
        } else {
            break;
        }
        str++;
    }

    result += fraction;
    if (negative) result = -result;
    return result;
}

// Функция извлечения значения по метке 
double extractValue(const std::string& line, const char* label) {
    const char* p = line.c_str();
    const char* found = nullptr;

    // Поиск метки вручную
    while (*p != '\0') {
        const char* start = p;
        const char* lab = label;
        while (*start && *lab && *start == *lab) {
            start++;
            lab++;
        }
        if (*lab == '\0') { // метка найдена
            found = start;
            break;
        }
        p++;
    }

    if (found) {
        return parseNumber(found);
    } else {
        return NAN; // если метка не найдена
    }
}

int main() {
    std::vector<std::string> dataLogs = {
        "T=00:00:01;TEMP=134.6;PRESS=4.25;FLOW=1.23",
        "T=00:00:02;TEMP=135.1;PRESS=4.20;FLOW=1.22",
        "T=00:00:03;TEMP=136.8;PRESS=4.10;FLOW=1.18",
        "T=00:00:04;TEMP=139.2;PRESS=3.95;FLOW=1.10"
    };

    std::vector<double> temp, press, flow;
    std::vector<std::string> timeStamps;

    // Парсинг строк
    for (const auto& line : dataLogs) {
        // Извлечение данных
        double t = extractValue(line, "TEMP=");
        double p = extractValue(line, "PRESS=");
        double f = extractValue(line, "FLOW=");

        // Извлечение времени вручную
        const char* ts = line.c_str();
        const char* pos = nullptr;
        if ((pos = strstr(ts, "T=")) != nullptr) {
            pos += 2;
            std::string tstamp;
            while (*pos && *pos != ';') {
                tstamp.push_back(*pos);
                pos++;
            }
            timeStamps.push_back(tstamp);
        }

        temp.push_back(t);
        press.push_back(p);
        flow.push_back(f);
    }

    // Анализ данных
    double avgTemp = 0, avgFlow = 0, minPress = press[0];
    for (size_t i = 0; i < temp.size(); ++i) {
        avgTemp += temp[i];
        avgFlow += flow[i];
        if (press[i] < minPress) minPress = press[i];
    }
    avgTemp /= temp.size();
    avgFlow /= flow.size();

    std::cout << "Average temperature: " << avgTemp << " °C\n";
    std::cout << "Minimum pressure: " << minPress << " atm\n";
    std::cout << "Average flow: " << avgFlow << " m³/s\n";

    // Проверка аварийных условий и расчёт производных
    std::vector<double> dTemp, dPress;
    for (size_t i = 1; i < temp.size(); ++i) {
        double dT = temp[i] - temp[i - 1];
        double dP = press[i] - press[i - 1];
        dTemp.push_back(dT);
        dPress.push_back(dP);

        if (dT > 2.0) {
            std::cout << "Warning: rapid temperature rise between "
                      << timeStamps[i - 1] << " and " << timeStamps[i] << "\n";
        }
        if (dP < -0.3) {
            std::cout << "Warning: pressure drop between "
                      << timeStamps[i - 1] << " and " << timeStamps[i] << "\n";
        }
    }

    // Поиск максимальных изменений
    double maxDT = 0, maxDP = 0;
    size_t idxT = 0, idxP = 0;

    for (size_t i = 0; i < dTemp.size(); ++i) {
        if (fabs(dTemp[i]) > fabs(maxDT)) {
            maxDT = dTemp[i];
            idxT = i;
        }
        if (fabs(dPress[i]) > fabs(maxDP)) {
            maxDP = dPress[i];
            idxP = i;
        }
    }

    std::cout << "Max dT/dt at T=" << timeStamps[idxT + 1]
              << ": " << (maxDT > 0 ? "+" : "") << maxDT << " °C/s\n";
    std::cout << "Max dP/dt at T=" << timeStamps[idxP + 1]
              << ": " << (maxDP > 0 ? "+" : "") << maxDP << " atm/s\n";

    return 0;
}
