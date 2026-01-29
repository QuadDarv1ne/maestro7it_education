#include "../include/uci_engine.hpp"
#include <algorithm>
#include <cctype>

// Определение констант
namespace UCIConstants {
    const std::string ENGINE_NAME = "Professional Chess Engine";
    const std::string ENGINE_AUTHOR = "Development Team";
    const int DEFAULT_SEARCH_DEPTH = 6;
    const int DEFAULT_SEARCH_TIME = 1000; // миллисекунды
    const std::vector<std::string> SUPPORTED_OPTIONS = {
        "Hash", "Threads", "Ponder", "MultiPV", "Skill Level"
    };
}

// Реализация утилит
namespace UCIUtils {
    std::vector<std::string> splitString(const std::string& str, char delimiter) {
        std::vector<std::string> tokens;
        std::stringstream ss(str);
        std::string token;
        
        while (std::getline(ss, token, delimiter)) {
            tokens.push_back(trimString(token));
        }
        
        return tokens;
    }
    
    std::string trimString(const std::string& str) {
        size_t start = str.find_first_not_of(" \t\r\n");
        if (start == std::string::npos) return "";
        
        size_t end = str.find_last_not_of(" \t\r\n");
        return str.substr(start, end - start + 1);
    }
    
    bool stringStartsWith(const std::string& str, const std::string& prefix) {
        return str.length() >= prefix.length() && 
               str.substr(0, prefix.length()) == prefix;
    }
    
    std::string toLowerCase(const std::string& str) {
        std::string result = str;
        std::transform(result.begin(), result.end(), result.begin(), 
                      [](unsigned char c){ return std::tolower(c); });
        return result;
    }
}

UCIEngine::UCIEngine(const std::string& name, const std::string& author)
    : engineName_(name), engineAuthor_(author), 
      shouldStop_(false), isSearching_(false),
      searchDepth_(UCIConstants::DEFAULT_SEARCH_DEPTH),
      searchTime_(UCIConstants::DEFAULT_SEARCH_TIME),
      searchNodes_(0), ponder_(false) {
    
    // Инициализация опций по умолчанию
    options_["Hash"] = "64";
    options_["Threads"] = "4";
    options_["Ponder"] = "false";
    options_["MultiPV"] = "1";
    options_["Skill Level"] = "20";
    
    // Установка начальной позиции
    currentPosition_ = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1";
}

void UCIEngine::runUCIProtocol() {
    std::cout << "id name " << engineName_ << std::endl;
    std::cout << "id author " << engineAuthor_ << std::endl;
    
    // Вывод поддерживаемых опций
    for (const auto& option : UCIConstants::SUPPORTED_OPTIONS) {
        if (option == "Hash") {
            std::cout << "option name Hash type spin default 64 min 1 max 1024" << std::endl;
        } else if (option == "Threads") {
            std::cout << "option name Threads type spin default 4 min 1 max 64" << std::endl;
        } else if (option == "Ponder") {
            std::cout << "option name Ponder type check default false" << std::endl;
        } else if (option == "MultiPV") {
            std::cout << "option name MultiPV type spin default 1 min 1 max 10" << std::endl;
        } else if (option == "Skill Level") {
            std::cout << "option name Skill Level type spin default 20 min 0 max 20" << std::endl;
        }
    }
    
    std::cout << "uciok" << std::endl;
    
    // Основной цикл обработки команд
    std::string command;
    while (std::getline(std::cin, command)) {
        command = UCIUtils::trimString(command);
        if (command.empty()) continue;
        
        processCommand(command);
        
        if (command == "quit") {
            break;
        }
    }
}

void UCIEngine::processCommand(const std::string& command) {
    std::vector<std::string> tokens = UCIUtils::splitString(command, ' ');
    if (tokens.empty()) return;
    
    std::string mainCommand = UCIUtils::toLowerCase(tokens[0]);
    
    if (mainCommand == "uci") {
        handleUCI();
    } else if (mainCommand == "isready") {
        handleIsReady();
    } else if (mainCommand == "position") {
        handlePosition(command);
    } else if (mainCommand == "go") {
        handleGo(command);
    } else if (mainCommand == "stop") {
        handleStop();
    } else if (mainCommand == "ponderhit") {
        handlePonderHit();
    } else if (mainCommand == "setoption") {
        handleSetOption(command);
    } else if (mainCommand == "ucinewgame") {
        handleUCINewGame();
    } else if (mainCommand == "quit") {
        handleQuit();
    } else {
        std::cout << "info string Unknown command: " << command << std::endl;
    }
}

void UCIEngine::handleUCI() {
    std::cout << "id name " << engineName_ << std::endl;
    std::cout << "id author " << engineAuthor_ << std::endl;
    std::cout << "uciok" << std::endl;
}

void UCIEngine::handleIsReady() {
    // Проверка готовности движка
    // Здесь можно добавить инициализацию тяжелых компонентов
    std::cout << "readyok" << std::endl;
}

void UCIEngine::handlePosition(const std::string& command) {
    std::vector<std::string> tokens = UCIUtils::splitString(command, ' ');
    
    if (tokens.size() < 2) return;
    
    if (tokens[1] == "startpos") {
        currentPosition_ = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1";
        moveHistory_.clear();
        
        // Обработка ходов после startpos
        for (size_t i = 2; i < tokens.size(); i++) {
            if (tokens[i] == "moves" && i + 1 < tokens.size()) {
                for (size_t j = i + 1; j < tokens.size(); j++) {
                    if (isValidMove(tokens[j])) {
                        moveHistory_.push_back(tokens[j]);
                    }
                }
                break;
            }
        }
    } else if (tokens[1] == "fen" && tokens.size() >= 8) {
        // Сбор FEN строки
        std::string fen;
        for (int i = 2; i < 8 && i < static_cast<int>(tokens.size()); i++) {
            fen += tokens[i] + " ";
        }
        fen.pop_back(); // Удалить последний пробел
        currentPosition_ = fen;
        moveHistory_.clear();
        
        // Обработка ходов после fen
        for (size_t i = 8; i < tokens.size(); i++) {
            if (tokens[i] == "moves" && i + 1 < tokens.size()) {
                for (size_t j = i + 1; j < tokens.size(); j++) {
                    if (isValidMove(tokens[j])) {
                        moveHistory_.push_back(tokens[j]);
                    }
                }
                break;
            }
        }
    }
    
    sendInfo("string Position set: " + currentPosition_);
    if (!moveHistory_.empty()) {
        sendInfo("string Move history: " + std::to_string(moveHistory_.size()) + " moves");
    }
}

void UCIEngine::handleGo(const std::string& command) {
    std::vector<std::string> tokens = UCIUtils::splitString(command, ' ');
    
    // Сброс параметров поиска
    searchDepth_ = UCIConstants::DEFAULT_SEARCH_DEPTH;
    searchTime_ = UCIConstants::DEFAULT_SEARCH_TIME;
    searchNodes_ = 0;
    
    // Парсинг параметров поиска
    for (size_t i = 1; i < tokens.size(); i++) {
        if (tokens[i] == "depth" && i + 1 < tokens.size()) {
            searchDepth_ = std::stoi(tokens[i + 1]);
            i++;
        } else if (tokens[i] == "movetime" && i + 1 < tokens.size()) {
            searchTime_ = std::stoi(tokens[i + 1]);
            i++;
        } else if (tokens[i] == "nodes" && i + 1 < tokens.size()) {
            searchNodes_ = std::stoi(tokens[i + 1]);
            i++;
        } else if (tokens[i] == "infinite") {
            searchTime_ = 0; // Бесконечный поиск
        }
    }
    
    // Запуск поиска в отдельном потоке
    std::thread searchThread([this]() {
        startSearch();
    });
    searchThread.detach();
}

void UCIEngine::handleStop() {
    shouldStop_.store(true);
    sendInfo("string Search stopped");
}

void UCIEngine::handlePonderHit() {
    // Пока не реализован ponder режим
    sendInfo("string Ponder not implemented");
}

void UCIEngine::handleSetOption(const std::string& command) {
    std::vector<std::string> tokens = UCIUtils::splitString(command, ' ');
    
    std::string optionName, optionValue;
    bool valueFound = false;
    
    for (size_t i = 1; i < tokens.size(); i++) {
        if (tokens[i] == "name" && i + 1 < tokens.size()) {
            optionName = tokens[i + 1];
            i++;
        } else if (tokens[i] == "value" && i + 1 < tokens.size()) {
            optionValue = tokens[i + 1];
            valueFound = true;
            i++;
        }
    }
    
    if (!optionName.empty() && valueFound) {
        options_[optionName] = optionValue;
        sendInfo("string Option " + optionName + " set to " + optionValue);
    }
}

void UCIEngine::handleUCINewGame() {
    // Сброс истории и настроек для новой игры
    moveHistory_.clear();
    currentPosition_ = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1";
    shouldStop_.store(false);
    sendInfo("string New game started");
}

void UCIEngine::handleQuit() {
    shouldStop_.store(true);
    sendInfo("string Engine shutting down");
}

// Вспомогательные методы
std::vector<std::string> UCIEngine::parseCommand(const std::string& command) {
    return UCIUtils::splitString(command, ' ');
}

std::string UCIEngine::getCurrentMove() const {
    return moveHistory_.empty() ? "none" : moveHistory_.back();
}

void UCIEngine::sendInfo(const std::string& info) {
    std::cout << "info " << info << std::endl;
}

void UCIEngine::sendBestMove(const std::string& move) {
    std::cout << "bestmove " << move << std::endl;
}

// Методы поиска
void UCIEngine::startSearch() {
    isSearching_.store(true);
    shouldStop_.store(false);
    
    sendInfo("string Starting search with depth " + std::to_string(searchDepth_));
    
    // Здесь будет интеграция с основным шахматным движком
    std::string bestMove = findBestMove();
    
    if (!shouldStop_.load()) {
        sendBestMove(bestMove);
    }
    
    isSearching_.store(false);
}

void UCIEngine::stopSearch() {
    shouldStop_.store(true);
}

std::string UCIEngine::findBestMove() {
    // Эмуляция поиска лучшего хода
    // В реальной реализации здесь будет вызов шахматного движка
    
    // Простая эвристика для демонстрации
    std::vector<std::string> commonMoves = {
        "e2e4", "d2d4", "g1f3", "c2c4", "e2e3"
    };
    
    // Выбор хода на основе текущей позиции и истории
    int moveIndex = moveHistory_.size() % commonMoves.size();
    return commonMoves[moveIndex];
}

// Валидация
bool UCIEngine::isValidMove(const std::string& move) const {
    // Проверка формата хода UCI (например, "e2e4", "g8f6")
    if (move.length() != 4) return false;
    
    char file1 = move[0];
    char rank1 = move[1];
    char file2 = move[2];
    char rank2 = move[3];
    
    return (file1 >= 'a' && file1 <= 'h') &&
           (rank1 >= '1' && rank1 <= '8') &&
           (file2 >= 'a' && file2 <= 'h') &&
           (rank2 >= '1' && rank2 <= '8');
}

bool UCIEngine::isValidFEN(const std::string& fen) const {
    // Базовая проверка FEN строки
    // В реальной реализации нужна полная валидация
    return !fen.empty() && fen.find(" ") != std::string::npos;
}

std::string UCIEngine::moveToUCI(const std::string& internalMove) const {
    // Конвертация внутреннего формата в UCI
    return internalMove; // Пока предполагаем, что форматы совпадают
}

std::string UCIEngine::moveFromUCI(const std::string& uciMove) const {
    // Конвертация UCI в внутренний формат
    return uciMove; // Пока предполагаем, что форматы совпадают
}