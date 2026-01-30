#include "../../include/uci_engine.hpp"
#include <iostream>
#include <sstream>
#include <algorithm>

UCIEngine::UCIEngine() 
    : gameRules_(board_), minimax_(board_), running_(false), searching_(false),
      searchDepth_(6), searchTimeMs_(1000), infiniteSearch_(false) {
    
    options_["Hash"] = "64";
    options_["Threads"] = "1";
    board_.setupStartPosition();
}

UCIEngine::~UCIEngine() {
    handleStop();
    if (searchThread_.joinable()) {
        searchThread_.join();
    }
}

void UCIEngine::run() {
    running_ = true;
    std::string line;
    
    while (running_ && std::getline(std::cin, line)) {
        if (line.empty()) continue;
        processCommand(line);
    }
}

void UCIEngine::processCommand(const std::string& command) {
    std::vector<std::string> tokens = tokenize(command);
    if (tokens.empty()) return;
    
    std::string cmd = tokens[0];
    
    if (cmd == "uci") handleUCI();
    else if (cmd == "isready") handleIsReady();
    else if (cmd == "ucinewgame") handleUCINewGame();
    else if (cmd == "position") handlePosition(tokens);
    else if (cmd == "go") handleGo(tokens);
    else if (cmd == "stop") handleStop();
    else if (cmd == "quit") handleQuit();
    else if (cmd == "setoption") handleSetOption(tokens);
}

void UCIEngine::handleUCI() {
    std::cout << "id name Maestro Chess Engine" << std::endl;
    std::cout << "id author Chess Engine Team" << std::endl;
    std::cout << "option name Hash type spin default 64 min 1 max 1024" << std::endl;
    std::cout << "option name Threads type spin default 1 min 1 max 128" << std::endl;
    std::cout << "uciok" << std::endl;
}

void UCIEngine::handleIsReady() {
    std::cout << "readyok" << std::endl;
}

void UCIEngine::handleUCINewGame() {
    handleStop();
    board_.setupStartPosition();
}

void UCIEngine::handlePosition(const std::vector<std::string>& tokens) {
    if (tokens.size() < 2) return;
    
    size_t movesIdx = 0;
    
    if (tokens[1] == "startpos") {
        board_.setupStartPosition();
        movesIdx = 2;
    } else if (tokens[1] == "fen") {
        std::string fen;
        size_t i = 2;
        while (i < tokens.size() && tokens[i] != "moves") {
            fen += tokens[i] + " ";
            i++;
        }
        if (!fen.empty()) {
            fen.pop_back();
            board_.setupFromFEN(fen);
        }
        movesIdx = i;
    }
    
    if (movesIdx < tokens.size() && tokens[movesIdx] == "moves") {
        for (size_t i = movesIdx + 1; i < tokens.size(); i++) {
            gameRules_.makeMove(tokens[i]);
        }
    }
}

void UCIEngine::handleGo(const std::vector<std::string>& tokens) {
    handleStop();
    
    searchDepth_ = 6; // Default
    searchTimeMs_ = 0;
    infiniteSearch_ = false;
    
    for (size_t i = 1; i < tokens.size(); i++) {
        if (tokens[i] == "depth" && i + 1 < tokens.size()) {
            searchDepth_ = std::stoi(tokens[i + 1]);
        } else if (tokens[i] == "movetime" && i + 1 < tokens.size()) {
            searchTimeMs_ = std::stoi(tokens[i + 1]);
        } else if (tokens[i] == "wtime" && i + 1 < tokens.size() && board_.getCurrentPlayer() == Color::WHITE) {
            searchTimeMs_ = std::stoi(tokens[i + 1]) / 30; // Тратим 1/30 оставшегося времени
        } else if (tokens[i] == "btime" && i + 1 < tokens.size() && board_.getCurrentPlayer() == Color::BLACK) {
            searchTimeMs_ = std::stoi(tokens[i + 1]) / 30;
        } else if (tokens[i] == "infinite") {
            infiniteSearch_ = true;
        }
    }
    
    if (searchThread_.joinable()) {
        searchThread_.join();
    }
    
    searching_ = true;
    searchThread_ = std::thread(&UCIEngine::startSearch, this);
}

void UCIEngine::startSearch() {
    minimax_.setMaxDepth(searchDepth_);
    minimax_.resetInterrupt();
    if (searchTimeMs_ > 0) {
        minimax_.setTimeLimit(std::chrono::milliseconds(searchTimeMs_));
    } else {
        // Устанавливаем очень большое время для "бесконечного" поиска или поиска по глубине
        minimax_.setTimeLimit(std::chrono::hours(1));
    }
    
    Move bestMove = minimax_.findBestMove(board_.getCurrentPlayer());
    
    // Вывод информации о поиске (в реальном времени это должно быть в minimax_)
    // Но здесь мы можем вывести финальную информацию
    int score = minimax_.evaluatePosition();
    std::cout << "info depth " << searchDepth_ << " score cp " << score << " nodes " << 1000 << " pv " 
              << board_.squareToAlgebraic(bestMove.from) << board_.squareToAlgebraic(bestMove.to) << std::endl;
    
    if (searching_ && !minimax_.isTimeUp()) {
        std::string moveStr = board_.squareToAlgebraic(bestMove.from) + board_.squareToAlgebraic(bestMove.to);
        if (bestMove.promotion != PieceType::EMPTY) {
            char p = 'q';
            if (bestMove.promotion == PieceType::ROOK) p = 'r';
            else if (bestMove.promotion == PieceType::BISHOP) p = 'b';
            else if (bestMove.promotion == PieceType::KNIGHT) p = 'n';
            moveStr += p;
        }
        sendBestMove(moveStr);
    }
    
    searching_ = false;
}

void UCIEngine::handleStop() {
    searching_ = false;
    minimax_.interrupt();
}

void UCIEngine::handleQuit() {
    handleStop();
    running_ = false;
}

void UCIEngine::handleSetOption(const std::vector<std::string>& tokens) {
    // Упрощенная обработка setoption name X value Y
    if (tokens.size() < 5) return;
    std::string name = tokens[2];
    std::string value = tokens[4];
    options_[name] = value;
}

void UCIEngine::sendInfo(const std::string& info) {
    std::cout << "info " << info << std::endl;
}

void UCIEngine::sendBestMove(const std::string& move) {
    std::cout << "bestmove " << move << std::endl;
}

std::vector<std::string> UCIEngine::tokenize(const std::string& input) {
    std::vector<std::string> tokens;
    std::stringstream ss(input);
    std::string token;
    while (ss >> token) {
        tokens.push_back(token);
    }
    return tokens;
}

std::string UCIEngine::trim(const std::string& str) {
    size_t first = str.find_first_not_of(' ');
    if (std::string::npos == first) return str;
    size_t last = str.find_last_not_of(' ');
    return str.substr(first, (last - first + 1));
}
