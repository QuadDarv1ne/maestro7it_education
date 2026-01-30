#include "../include/uci_engine.hpp"
#include <iostream>
#include <sstream>
#include <algorithm>
#include <chrono>

UCIEngine::UCIEngine() 
    : running_(false), searching_(false), search_depth_(10), 
      search_time_ms_(5000), infinite_search_(false) {
    
    // Инициализация стандартных опций
    options_[UCIConstants::OPTION_HASH] = "64";        // 64 MB хэш таблица
    options_[UCIConstants::OPTION_THREADS] = "4";      // 4 потока
    options_[UCIConstants::OPTION_MULTI_PV] = "1";     // 1 линия
    options_[UCIConstants::OPTION_OWN_BOOK] = "true";  // Использовать книгу дебютов
}

UCIEngine::~UCIEngine() {
    stop();
    if (search_thread_.joinable()) {
        search_thread_.join();
    }
}

void UCIEngine::start() {
    running_ = true;
    std::cout << UCIConstants::RESP_ID_NAME << std::endl;
    std::cout << UCIConstants::RESP_ID_AUTHOR << std::endl;
    printOptions();
    std::cout << UCIConstants::RESP_UCI_OK << std::endl;
}

void UCIEngine::stop() {
    running_ = false;
    searching_ = false;
    if (search_thread_.joinable()) {
        search_thread_.join();
    }
}

void UCIEngine::sendCommand(const std::string& command) {
    if (!running_) return;
    
    std::string trimmed_cmd = trim(command);
    std::vector<std::string> tokens = tokenize(trimmed_cmd);
    
    if (tokens.empty()) return;
    
    const std::string& cmd = tokens[0];
    
    if (cmd == UCIConstants::CMD_UCI) {
        start();
    } else if (cmd == UCIConstants::CMD_ISREADY) {
        std::cout << UCIConstants::RESP_READY_OK << std::endl;
    } else if (cmd == UCIConstants::CMD_UCINEWGAME) {
        handleUCINewGame();
    } else if (cmd == UCIConstants::CMD_POSITION) {
        handlePosition(tokens);
    } else if (cmd == UCIConstants::CMD_GO) {
        handleGo(tokens);
    } else if (cmd == UCIConstants::CMD_STOP) {
        handleStop();
    } else if (cmd == UCIConstants::CMD_QUIT) {
        handleQuit();
    } else if (cmd == UCIConstants::CMD_SET_OPTION) {
        // Обработка установки опций
        if (tokens.size() >= 5 && tokens[1] == "name" && tokens[3] == "value") {
            std::string option_name = tokens[2];
            std::string option_value;
            for (size_t i = 4; i < tokens.size(); i++) {
                if (!option_value.empty()) option_value += " ";
                option_value += tokens[i];
            }
            setOption(option_name, option_value);
        }
    }
}

void UCIEngine::handleUCINewGame() {
    // Сброс истории и подготовка к новой игре
    sendInfo("string Starting new game");
}

void UCIEngine::handlePosition(const std::vector<std::string>& tokens) {
    if (tokens.size() < 2) return;
    
    std::string position_type = tokens[1];
    
    if (position_type == "startpos") {
        // Начальная позиция
        sendInfo("string Setting up starting position");
    } else if (position_type == "fen" && tokens.size() >= 8) {
        // Позиция в формате FEN
        std::string fen;
        for (int i = 2; i < 8; i++) {
            fen += tokens[i] + " ";
        }
        sendInfo("string Setting up position from FEN: " + fen);
    }
    
    // Обработка ходов
    for (size_t i = 2; i < tokens.size(); i++) {
        if (tokens[i] == "moves" && i + 1 < tokens.size()) {
            for (size_t j = i + 1; j < tokens.size(); j++) {
                sendInfo("string Processing move: " + tokens[j]);
            }
            break;
        }
    }
}

void UCIEngine::handleGo(const std::vector<std::string>& tokens) {
    if (searching_) return;
    
    searching_ = true;
    infinite_search_ = false;
    search_depth_ = 10;
    search_time_ms_ = 5000;
    
    // Парсинг параметров поиска
    for (size_t i = 1; i < tokens.size(); i++) {
        if (tokens[i] == "depth" && i + 1 < tokens.size()) {
            search_depth_ = std::stoi(tokens[i + 1]);
            i++;
        } else if (tokens[i] == "movetime" && i + 1 < tokens.size()) {
            search_time_ms_ = std::stoi(tokens[i + 1]);
            i++;
        } else if (tokens[i] == "infinite") {
            infinite_search_ = true;
        }
    }
    
    // Запуск поиска в отдельном потоке
    search_thread_ = std::thread([this]() {
        auto start_time = std::chrono::steady_clock::now();
        
        // Имитация поиска лучшего хода
        std::this_thread::sleep_for(std::chrono::milliseconds(search_time_ms_));
        
        auto end_time = std::chrono::steady_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time);
        
        // Отправка информации о поиске
        sendInfo("depth " + std::to_string(search_depth_));
        sendInfo("time " + std::to_string(duration.count()));
        sendInfo("nodes 1000000"); // Имитация
        sendInfo("nps 200000");    // Имитация
        
        // Отправка лучшего хода
        sendBestMove("e2e4");
        
        searching_ = false;
    });
}

void UCIEngine::handleStop() {
    searching_ = false;
    if (search_thread_.joinable()) {
        search_thread_.join();
    }
}

void UCIEngine::handleQuit() {
    stop();
    std::exit(0);
}

void UCIEngine::sendInfo(const std::string& info) {
    std::cout << UCIConstants::RESP_INFO << info << std::endl;
}

void UCIEngine::sendBestMove(const std::string& move) {
    std::cout << UCIConstants::RESP_BESTMOVE << move << std::endl;
}

std::vector<std::string> UCIEngine::tokenize(const std::string& input) {
    std::vector<std::string> tokens;
    std::istringstream iss(input);
    std::string token;
    
    while (iss >> token) {
        tokens.push_back(token);
    }
    
    return tokens;
}

std::string UCIEngine::trim(const std::string& str) {
    size_t start = str.find_first_not_of(" \t\r\n");
    if (start == std::string::npos) return "";
    
    size_t end = str.find_last_not_of(" \t\r\n");
    return str.substr(start, end - start + 1);
}

void UCIEngine::setOption(const std::string& name, const std::string& value) {
    options_[name] = value;
    sendInfo("string Option " + name + " set to " + value);
}

std::string UCIEngine::getOption(const std::string& name) const {
    auto it = options_.find(name);
    return (it != options_.end()) ? it->second : "";
}

void UCIEngine::printOptions() {
    std::cout << "option name " << UCIConstants::OPTION_HASH 
              << " type spin default 64 min 1 max 1024" << std::endl;
    std::cout << "option name " << UCIConstants::OPTION_THREADS 
              << " type spin default 4 min 1 max 64" << std::endl;
    std::cout << "option name " << UCIConstants::OPTION_MULTI_PV 
              << " type spin default 1 min 1 max 10" << std::endl;
    std::cout << "option name " << UCIConstants::OPTION_OWN_BOOK 
              << " type check default true" << std::endl;
}

// Демонстрационная программа для тестирования UCI
class UCIDemo {
public:
    void runDemo() {
        std::cout << "=== UCI PROTOCOL DEMONSTRATION ===" << std::endl;
        
        UCIEngine engine;
        
        // Тестовые команды UCI
        std::vector<std::string> test_commands = {
            "uci",
            "isready", 
            "ucinewgame",
            "position startpos",
            "position startpos moves e2e4 e7e5",
            "position fen rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            "go depth 6",
            "go movetime 1000",
            "stop",
            "setoption name Hash value 128",
            "setoption name Threads value 8",
            "quit"
        };
        
        std::cout << "\nTesting UCI commands:\n" << std::endl;
        
        for (const auto& command : test_commands) {
            std::cout << ">>> " << command << std::endl;
            engine.sendCommand(command);
            std::cout << std::endl;
            
            // Небольшая задержка между командами
            std::this_thread::sleep_for(std::chrono::milliseconds(100));
        }
        
        std::cout << "=== UCI DEMONSTRATION COMPLETED ===" << std::endl;
    }
};

int main() {
    try {
        UCIDemo demo;
        demo.runDemo();
        return 0;
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
}