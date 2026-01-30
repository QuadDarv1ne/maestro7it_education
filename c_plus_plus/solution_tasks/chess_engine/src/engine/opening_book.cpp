#include "../include/opening_book.hpp"
#include <iostream>

OpeningBook::OpeningBook() : rng_(std::random_device{}()) {
    addStandardOpenings();
}

void OpeningBook::loadFromFile(const std::string& filename) {
    // TODO: Реализовать загрузку из файла
    std::cout << "OpeningBook: Загрузка из файла пока не реализована (" << filename << ")\n";
}

void OpeningBook::addStandardOpenings() {
    // Добавляем базовые дебютные позиции
    // Начальная позиция
    std::string startingFEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1";
    
    // Добавляем популярные дебютные ходы
    book_[startingFEN] = {
        {"e2e4", 100},  // Королевская пешка
        {"d2d4", 100},  // Ферзевая пешка
        {"c2c4", 80},   // Английское начало
        {"g1f3", 90}    // Дебют Рети
    };
}

std::string OpeningBook::getMove(const std::string& fen) const {
    auto it = book_.find(fen);
    if (it == book_.end() || it->second.empty()) {
        return ""; // Позиция не найдена в книге
    }
    
    // Вычисляем общий вес
    int totalWeight = 0;
    for (const auto& moveEntry : it->second) {
        totalWeight += moveEntry.second;
    }
    
    // Выбираем ход на основе весов
    std::uniform_int_distribution<int> dist(0, totalWeight - 1);
    int selection = dist(rng_);
    
    int cumulative = 0;
    for (const auto& moveEntry : it->second) {
        cumulative += moveEntry.second;
        if (selection < cumulative) {
            return moveEntry.first;
        }
    }
    
    // Запасной вариант (не должны сюда попасть)
    return it->second[0].first;
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
