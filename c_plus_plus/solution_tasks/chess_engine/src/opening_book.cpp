#include "../include/opening_book.hpp"
#include <sstream>
#include <iostream>

OpeningBook::OpeningBook() : rng_(std::random_device{}()) {
    addStandardOpenings();
}

void OpeningBook::addStandardOpenings() {
    // Итальянская партия
    book_["rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"] = {
        {"e2e4", 100}, {"d2d4", 80}, {"g1f3", 60}, {"c2c4", 50}
    };
    
    book_["rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2"] = {
        {"g1f3", 100}, {"f1c4", 90}, {"d2d4", 70}
    };
    
    book_["r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3"] = {
        {"f1c4", 100}, {"d2d4", 80}, {"c2c3", 60}
    };
    
    // Испанская партия
    book_["r1bqkb1r/pppp1ppp/2n2n2/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 4 4"] = {
        {"f1b5", 100}, {"d2d4", 70}, {"c2c3", 50}
    };
    
    // Сицилианская защита
    book_["rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2"] = {
        {"g1f3", 100}, {"f1b5", 80}, {"d2d4", 70}
    };
    
    // Королевский гамбит
    book_["rnbqkbnr/pppp1ppp/8/4p3/4PP2/8/PPPP2PP/RNBQKBNR b KQkq - 0 2"] = {
        {"d7d5", 100}, {"e5f4", 80}, {"g8f6", 60}
    };
    
    // Дебют английского
    book_["rnbqkbnr/pppppppp/8/8/2P5/8/PP1PPPPP/RNBQKBNR b KQkq - 0 1"] = {
        {"g8f6", 100}, {"e7e6", 90}, {"c7c5", 80}
    };
    
    // Ферзевый гамбит
    book_["rnbqkbnr/ppp2ppp/4p3/3p4/2PP4/8/PP2PPPP/RNBQKBNR w KQkq - 0 3"] = {
        {"c4d5", 100}, {"g1f3", 80}, {"b1c3", 70}
    };
    
    // Нимцович-Ларсенова атака
    book_["rnbqkbnr/pppppppp/8/8/8/1P6/P1PPPPPP/RNBQKBNR b KQkq - 0 1"] = {
        {"d7d5", 100}, {"g8f6", 80}, {"e7e5", 70}
    };
    
    // Рети
    book_["rnbqkbnr/pppppppp/8/8/8/5N2/PPPPPPPP/RNBQKB1R b KQkq - 1 1"] = {
        {"d7d5", 100}, {"g8f6", 90}, {"c7c5", 80}
    };
}

std::string OpeningBook::getMove(const std::string& fen) const {
    auto it = book_.find(fen);
    if (it == book_.end()) {
        return "";
    }
    
    const auto& moves = it->second;
    if (moves.empty()) {
        return "";
    }
    
    // Выбор хода с учетом весов
    int total_weight = 0;
    for (const auto& pair : moves) {
        total_weight += pair.second;
    }
    
    std::uniform_int_distribution<int> dist(1, total_weight);
    int random_value = dist(rng_);
    
    int current_sum = 0;
    for (const auto& pair : moves) {
        current_sum += pair.second;
        if (random_value <= current_sum) {
            return pair.first;
        }
    }
    
    return moves.front().first; // fallback
}

bool OpeningBook::hasPosition(const std::string& fen) const {
    return book_.find(fen) != book_.end();
}

std::vector<std::pair<std::string, int>> OpeningBook::getMoves(const std::string& fen) const {
    auto it = book_.find(fen);
    if (it == book_.end()) {
        return {};
    }
    return it->second;
}

size_t OpeningBook::size() const {
    return book_.size();
}