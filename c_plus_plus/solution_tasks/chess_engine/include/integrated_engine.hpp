#ifndef CHESS_ENGINE_INTEGRATED_HPP
#define CHESS_ENGINE_INTEGRATED_HPP

#include "bitboard.hpp"
#include "incremental_evaluator.hpp"
#include "parallel_search.hpp"
#include "uci_engine.hpp"
#include "opening_book.hpp"
#include "neural_evaluator.hpp"
#include "move_ordering.hpp"
#include <memory>

/**
 * @brief Интегрированный профессиональный шахматный движок
 * 
 * Объединяет все оптимизации и алгоритмы в единую систему
 */
class IntegratedChessEngine {
private:
    std::unique_ptr<BitboardEngine> bitboard_engine_;
    std::unique_ptr<IncrementalEvaluator> incremental_evaluator_;
    std::unique_ptr<ParallelChessEngine> parallel_engine_;
    std::unique_ptr<OpeningBook> opening_book_;
    std::unique_ptr<NeuralEvaluator> neural_evaluator_;
    std::unique_ptr<MoveOrdering> move_ordering_;
    
    bool use_neural_evaluation_;
    bool use_opening_book_;
    int search_depth_;
    
public:
    IntegratedChessEngine() 
        : use_neural_evaluation_(true)
        , use_opening_book_(true)
        , search_depth_(8) {
        
        initializeComponents();
    }
    
    void initializeComponents() {
        bitboard_engine_ = std::make_unique<BitboardEngine>();
        incremental_evaluator_ = std::make_unique<IncrementalEvaluator>();
        parallel_engine_ = std::make_unique<ParallelChessEngine>();
        opening_book_ = std::make_unique<OpeningBook>();
        neural_evaluator_ = std::make_unique<NeuralEvaluator>();
        move_ordering_ = std::make_unique<MoveOrdering>();
    }
    
    std::string findBestMove(const std::string& fen_position) {
        // 1. Проверка книги дебютов
        if (use_opening_book_) {
            std::string book_move = opening_book_->getRandomMove(fen_position);
            if (!book_move.empty()) {
                return book_move;
            }
        }
        
        // 2. Подготовка позиции для bitboard
        bitboard_engine_->setFromFEN(fen_position);
        
        // 3. Поиск лучшего хода
        std::string best_move = parallel_engine_->findBestMove(
            bitboard_engine_.get(), 
            search_depth_,
            [this](const BitboardEngine* engine) {
                return evaluatePosition(engine);
            },
            [this](const std::vector<std::string>& moves, int depth) {
                return move_ordering_->orderMoves(moves, depth);
            }
        );
        
        // 4. Обновление статистики
        if (!best_move.empty()) {
            move_ordering_->addGoodMove(best_move, search_depth_);
        }
        
        return best_move;
    }
    
    int evaluatePosition(const BitboardEngine* engine) const {
        if (use_neural_evaluation_) {
            // Использование нейронной оценки
            std::array<int, 64> board_state = engine->toFeatureArray();
            return neural_evaluator_->evaluate(board_state);
        } else {
            // Традиционная оценка
            return incremental_evaluator_->evaluate(engine);
        }
    }
    
    void trainNeuralNetwork(const std::vector<std::pair<std::array<int, 64>, int>>& training_data) {
        neural_evaluator_->train(training_data, 50);
    }
    
    void setNeuralEvaluation(bool enable) {
        use_neural_evaluation_ = enable;
    }
    
    void setOpeningBook(bool enable) {
        use_opening_book_ = enable;
    }
    
    void setSearchDepth(int depth) {
        search_depth_ = depth;
        parallel_engine_->setMaxDepth(depth);
    }
    
    void addOpeningPosition(const std::string& fen, const std::vector<std::string>& moves) {
        opening_book_->addPosition(fen, moves);
    }
    
    std::vector<std::string> getBookMoves(const std::string& fen) const {
        return opening_book_->getAllMoves(fen);
    }
    
    size_t getBookSize() const {
        return opening_book_->size();
    }
    
    size_t getHistorySize() const {
        return move_ordering_->getHistorySize();
    }
    
    void clearHistory() {
        move_ordering_->clearHistory();
    }
};

#endif // CHESS_ENGINE_INTEGRATED_HPP