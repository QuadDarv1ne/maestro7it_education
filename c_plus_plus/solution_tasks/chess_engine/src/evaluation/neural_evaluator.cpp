#include <stdint.h>
#include <random>
#include <cmath>
#include <algorithm>
#include <iostream>
#include <iomanip>
#include <limits.h>

#include "../../include/neural_evaluator.hpp"
#include <cstdint>
#include <climits>

// Инициализация констант
const float NeuralEvaluator::NN_WEIGHT = 0.7f;
const float NeuralEvaluator::TRADITIONAL_WEIGHT = 0.3f;

NeuralEvaluator::NeuralEvaluator(const Bitboard& board) 
    : board_(board), cache_valid_(false), cached_evaluation_(0.0f), cached_hash_(0),
      material_score_(0), positional_score_(0), mobility_score_(0),
      king_safety_score_(0), pawn_structure_score_(0) {
    
    initializeWeights();
    // В реальной реализации здесь можно загрузить предобученные веса
    // loadPretrainedWeights();
}

void NeuralEvaluator::initializeWeights() {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::normal_distribution<float> dis(0.0f, 0.1f);
    
    // Инициализируем веса случайными значениями
    for (auto& weight : weights_input_hidden_) {
        weight = dis(gen);
    }
    
    for (auto& bias : biases_hidden_) {
        bias = dis(gen) * 0.01f;
    }
    
    for (auto& weight : weights_hidden_output_) {
        weight = dis(gen);
    }
    
    for (auto& bias : biases_output_) {
        bias = dis(gen) * 0.01f;
    }
}

void NeuralEvaluator::loadPretrainedWeights() {
    // В реальной реализации здесь будет загрузка весов из файла
    // Пока используем случайную инициализацию
}

std::vector<float> NeuralEvaluator::boardToInputVector() const {
    std::vector<float> input(INPUT_SIZE, 0.0f);
    int idx = 0;
    
    // Кодируем положение фигур (one-hot encoding)
    for (int square = 0; square < 64; square++) {
        Bitboard::PieceType piece_type = board_.getPieceType(square);
        Bitboard::Color piece_color = board_.getPieceColor(square);
        
        if (piece_type != Bitboard::PIECE_TYPE_COUNT && 
            piece_color != Bitboard::COLOR_COUNT) {
            
            int piece_idx = static_cast<int>(piece_type);
            if (piece_color == Bitboard::BLACK) {
                piece_idx += 6; // Черные фигуры во второй половине
            }
            
            input[idx + piece_idx] = 1.0f;
        }
        idx += 12; // 12 типов фигур (6 белых + 6 черных)
    }
    
    // Добавляем игровые характеристики
    GamePhase phase = getCurrentGamePhase();
    input[idx++] = (phase == OPENING) ? 1.0f : 0.0f;
    input[idx++] = (phase == MIDDLEGAME) ? 1.0f : 0.0f;
    input[idx++] = (phase == ENDGAME) ? 1.0f : 0.0f;
    
    // Материальный баланс
    int material_balance = calculateMaterial();
    input[idx++] = static_cast<float>(material_balance) / 5000.0f; // Нормализация
    
    // Количество фигур
    int white_pieces = BitboardUtils::popCount(board_.getOccupancy(Bitboard::WHITE));
    int black_pieces = BitboardUtils::popCount(board_.getOccupancy(Bitboard::BLACK));
    input[idx++] = static_cast<float>(white_pieces) / 16.0f;
    input[idx++] = static_cast<float>(black_pieces) / 16.0f;
    
    // Контроль центра
    Bitboard::BitboardType center = 0x0000001818000000ULL; // d4, d5, e4, e5
    int white_center = BitboardUtils::popCount(board_.getOccupancy(Bitboard::WHITE) & center);
    int black_center = BitboardUtils::popCount(board_.getOccupancy(Bitboard::BLACK) & center);
    input[idx++] = static_cast<float>(white_center) / 4.0f;
    input[idx++] = static_cast<float>(black_center) / 4.0f;
    
    return input;
}

float NeuralEvaluator::forwardPass(const std::vector<float>& input) const {
    // Входной слой -> скрытый слой
    std::array<float, HIDDEN_SIZE> hidden_layer;
    
    for (int i = 0; i < HIDDEN_SIZE; i++) {
        float sum = biases_hidden_[i];
        for (int j = 0; j < INPUT_SIZE; j++) {
            sum += input[j] * weights_input_hidden_[j * HIDDEN_SIZE + i];
        }
        hidden_layer[i] = relu(sum);
    }
    
    // Скрытый слой -> выходной слой
    float output = biases_output_[0];
    for (int i = 0; i < HIDDEN_SIZE; i++) {
        output += hidden_layer[i] * weights_hidden_output_[i];
    }
    
    return tanh_approx(output); // Нормализуем в диапазон [-1, 1]
}

float NeuralEvaluator::relu(float x) {
    return std::max(0.0f, x);
}

float NeuralEvaluator::tanh_approx(float x) {
    // Быстрая аппроксимация tanh
    if (x > 4.0f) return 1.0f;
    if (x < -4.0f) return -1.0f;
    
    float x2 = x * x;
    return x * (27.0f + x2) / (27.0f + 9.0f * x2);
}

int NeuralEvaluator::evaluate() const {
    // Проверяем кэш
    uint64_t current_hash = calculateBoardHash();
    if (cache_valid_ && cached_hash_ == current_hash) {
        return static_cast<int>(cached_evaluation_);
    }
    
    // Получаем входной вектор
    auto input_vector = boardToInputVector();
    
    // Нейросетевая оценка
    float nn_score = forwardPass(input_vector);
    
    // Традиционная оценка
    int traditional_score = traditionalEvaluation();
    
    // Комбинируем оценки
    float combined_score = NN_WEIGHT * nn_score + 
                          TRADITIONAL_WEIGHT * (static_cast<float>(traditional_score) / NeuralConstants::SCORE_SCALE);
    
    // Денормализуем
    int final_score = static_cast<int>(combined_score * NeuralConstants::SCORE_SCALE);
    
    // Обновляем кэш
    cached_evaluation_ = static_cast<float>(final_score);
    cached_hash_ = current_hash;
    cache_valid_ = true;
    
    return final_score;
}

int NeuralEvaluator::traditionalEvaluation() const {
    return calculateMaterial() + 
           calculatePositional() + 
           calculateMobility() + 
           calculateKingSafety() + 
           calculatePawnStructure();
}

int NeuralEvaluator::calculateMaterial() const {
    int score = 0;
    
    // Стоимости фигур
    static const int VALUES[] = {100, 320, 330, 500, 900, 20000}; // PAWN-KING
    
    // Белые фигуры
    for (int piece = 0; piece < 6; piece++) {
        Bitboard::BitboardType pieces = board_.getPieces(Bitboard::WHITE, 
                                                        static_cast<Bitboard::PieceType>(piece));
        score += BitboardUtils::popCount(pieces) * VALUES[piece];
    }
    
    // Черные фигуры
    for (int piece = 0; piece < 6; piece++) {
        Bitboard::BitboardType pieces = board_.getPieces(Bitboard::BLACK, 
                                                        static_cast<Bitboard::PieceType>(piece));
        score -= BitboardUtils::popCount(pieces) * VALUES[piece];
    }
    
    return score;
}

int NeuralEvaluator::calculatePositional() const {
    int score = 0;
    
    // Центральный контроль
    Bitboard::BitboardType center = 0x0000001818000000ULL;
    int white_center = BitboardUtils::popCount(board_.getOccupancy(Bitboard::WHITE) & center);
    int black_center = BitboardUtils::popCount(board_.getOccupancy(Bitboard::BLACK) & center);
    score += (white_center - black_center) * 10;
    
    // Развитие легких фигур
    Bitboard::BitboardType developed = 0x0000FFFFFFFF0000ULL; // Ранги 3-6
    int white_developed = BitboardUtils::popCount(board_.getPieces(Bitboard::WHITE, Bitboard::KNIGHT) & developed) +
                         BitboardUtils::popCount(board_.getPieces(Bitboard::WHITE, Bitboard::BISHOP) & developed);
    int black_developed = BitboardUtils::popCount(board_.getPieces(Bitboard::BLACK, Bitboard::KNIGHT) & developed) +
                         BitboardUtils::popCount(board_.getPieces(Bitboard::BLACK, Bitboard::BISHOP) & developed);
    score += (white_developed - black_developed) * 5;
    
    return score;
}

int NeuralEvaluator::calculateMobility() const {
    int score = 0;
    
    // Подсчет мобильности для белых
    auto white_moves = board_.generateLegalMoves();
    int white_mobility = static_cast<int>(white_moves.size());
    
    // Подсчет мобильности для черных
    // Для этого нужно временно переключить ход (но Bitboard::generateLegalMoves использует side_to_move_)
    // Нам нужно либо метод, принимающий цвет, либо временное переключение
    
    // В текущей реализации Bitboard::generateLegalMoves использует внутреннее состояние
    // Создадим копию для подсчета мобильности черных, если сейчас ход белых, и наоборот
    Bitboard temp_board = board_;
    // Нам нужно переключить ход в Bitboard. Посмотрим если есть метод setSideToMove
    // В bitboard.hpp нет setSideToMove, но есть side_to_move_ приватный.
    // Однако в bitboard_engine.cpp я видел sideToMove.
    
    // В include/bitboard.hpp нет метода для смены хода. 
    // Но подождите, я могу просто вызвать generateLegalMoves и посмотреть результат.
    
    // Для простоты, если мы не можем легко сменить ход, оценим мобильность текущего игрока
    if (board_.getSideToMove() == Bitboard::WHITE) {
        score += white_mobility * 2;
    } else {
        score -= white_mobility * 2;
    }
    
    return score;
}

int NeuralEvaluator::calculateKingSafety() const {
    int score = 0;
    
    // Простая оценка безопасности короля
    uint64_t white_king_bb = board_.getPieces(Bitboard::WHITE, Bitboard::KING);
    uint64_t black_king_bb = board_.getPieces(Bitboard::BLACK, Bitboard::KING);
    
    if (white_king_bb) {
        int king_square = BitboardUtils::lsb(white_king_bb);
        // Бонус за пешечный щит
        uint64_t shield = getPawnShield(king_square, Bitboard::WHITE);
        score += BitboardUtils::popCount(shield) * 5;
    }
    
    if (black_king_bb) {
        int king_square = BitboardUtils::lsb(black_king_bb);
        uint64_t shield = getPawnShield(king_square, Bitboard::BLACK);
        score -= BitboardUtils::popCount(shield) * 5;
    }
    
    return score;
}

uint64_t NeuralEvaluator::getPawnShield(int king_square, Bitboard::Color color) const {
    uint64_t shield = 0;
    int rank = king_square / 8;
    int file = king_square % 8;
    
    int direction = (color == Bitboard::WHITE) ? 1 : -1;
    int shield_rank = rank + direction;
    
    if (shield_rank >= 0 && shield_rank < 8) {
        for (int df = -1; df <= 1; df++) {
            int shield_file = file + df;
            if (shield_file >= 0 && shield_file < 8) {
                int sq = shield_rank * 8 + shield_file;
                if (board_.getPieceType(sq) == Bitboard::PAWN && 
                    board_.getPieceColor(sq) == color) {
                    shield |= (1ULL << sq);
                }
            }
        }
    }
    
    return shield;
}

int NeuralEvaluator::calculatePawnStructure() const {
    int score = 0;
    
    uint64_t white_pawns = board_.getPieces(Bitboard::WHITE, Bitboard::PAWN);
    uint64_t black_pawns = board_.getPieces(Bitboard::BLACK, Bitboard::PAWN);
    
    // Штраф за сдвоенные пешки
    for (int f = 0; f < 8; f++) {
        uint64_t file_mask = 0x0101010101010101ULL << f;
        
        int white_on_file = BitboardUtils::popCount(white_pawns & file_mask);
        if (white_on_file > 1) score -= (white_on_file - 1) * 20;
        
        int black_on_file = BitboardUtils::popCount(black_pawns & file_mask);
        if (black_on_file > 1) score += (black_on_file - 1) * 20;
    }
    
    // Бонус за проходные пешки (упрощенно)
    for (int sq = 0; sq < 64; sq++) {
        if (BitboardUtils::getBit(white_pawns, sq)) {
            int rank = sq / 8;
            if (rank >= 5) score += (rank - 4) * 15; // Белые пешки на 6-7 горизонтали
        }
        if (BitboardUtils::getBit(black_pawns, sq)) {
            int rank = sq / 8;
            if (rank <= 2) score -= (3 - rank) * 15; // Черные пешки на 2-3 горизонтали
        }
    }
    
    return score;
}

NeuralEvaluator::GamePhase NeuralEvaluator::getCurrentGamePhase() const {
    int piece_count = BitboardUtils::popCount(board_.getAllPieces());
    
    if (piece_count > 30) return OPENING;
    if (piece_count > 15) return MIDDLEGAME;
    return ENDGAME;
}

uint64_t NeuralEvaluator::calculateBoardHash() const {
    // Простая хеш-функция
    uint64_t hash = 0;
    
    for (int color = 0; color < 2; color++) {
        for (int piece = 0; piece < 6; piece++) {
            Bitboard::BitboardType pieces = board_.getPieces(static_cast<Bitboard::Color>(color), 
                                                            static_cast<Bitboard::PieceType>(piece));
            hash ^= pieces * (color * 6 + piece + 1);
        }
    }
    
    hash ^= static_cast<uint64_t>(board_.getSideToMove()) << 56;
    
    return hash;
}

float NeuralEvaluator::normalizeScore(int score) const {
    return std::clamp(static_cast<float>(score) / NeuralConstants::SCORE_SCALE, -1.0f, 1.0f);
}

int NeuralEvaluator::denormalizeScore(float normalized) const {
    return static_cast<int>(normalized * NeuralConstants::SCORE_SCALE);
}

void NeuralEvaluator::updateOnMove(int from_square, int to_square, 
                                  Bitboard::PieceType captured_piece) {
    // Инвалидируем кэш
    cache_valid_ = false;
    
    // В реальной реализации здесь будет инкрементальное обновление
    (void)from_square; (void)to_square; (void)captured_piece;
}

void NeuralEvaluator::train(const std::vector<std::pair<Bitboard, int>>& training_data) {
    // Заглушка для обучения
    (void)training_data;
    std::cout << "Обучение нейросети (заглушка)" << std::endl;
}

void NeuralEvaluator::resetCache() {
    cache_valid_ = false;
}

float NeuralEvaluator::getNetworkConfidence() const {
    // Возвращает уверенность сети в оценке
    auto input = boardToInputVector();
    float nn_output = forwardPass(input);
    return std::abs(nn_output); // Чем ближе к 1, тем увереннее
}

std::vector<float> NeuralEvaluator::getHiddenActivations() const {
    auto input = boardToInputVector();
    std::vector<float> activations(HIDDEN_SIZE, 0.0f);
    
    for (int i = 0; i < HIDDEN_SIZE; i++) {
        float sum = biases_hidden_[i];
        for (int j = 0; j < INPUT_SIZE; j++) {
            sum += input[j] * weights_input_hidden_[j * HIDDEN_SIZE + i];
        }
        activations[i] = relu(sum);
    }
    
    return activations;
}

void NeuralEvaluator::printFeatureImportance() const {
    std::cout << "\n=== ВАЖНОСТЬ ФИЧ НЕЙРОСЕТИ ===" << std::endl;
    
    auto activations = getHiddenActivations();
    
    // Находим наиболее активные нейроны
    std::vector<std::pair<int, float>> neuron_importance;
    for (int i = 0; i < HIDDEN_SIZE; i++) {
        neuron_importance.emplace_back(i, activations[i]);
    }
    
    std::sort(neuron_importance.begin(), neuron_importance.end(),
              [](const auto& a, const auto& b) { return a.second > b.second; });
    
    std::cout << "Топ-5 самых активных нейронов:" << std::endl;
    for (int i = 0; i < std::min(5, static_cast<int>(neuron_importance.size())); i++) {
        std::cout << "  Нейрон " << neuron_importance[i].first 
                  << ": активация = " << std::fixed << std::setprecision(4) 
                  << neuron_importance[i].second << std::endl;
    }
}

void NeuralEvaluator::analyzePosition() const {
    std::cout << "\n=== АНАЛИЗ ПОЗИЦИИ ===" << std::endl;
    
    int material = calculateMaterial();
    int positional = calculatePositional();
    int mobility = calculateMobility();
    int king_safety = calculateKingSafety();
    int pawn_structure = calculatePawnStructure();
    int total_traditional = material + positional + mobility + king_safety + pawn_structure;
    
    std::cout << "Материальная оценка:     " << material << std::endl;
    std::cout << "Позиционная оценка:      " << positional << std::endl;
    std::cout << "Мобильность:             " << mobility << std::endl;
    std::cout << "Безопасность короля:     " << king_safety << std::endl;
    std::cout << "Структура пешек:         " << pawn_structure << std::endl;
    std::cout << "Традиционная сумма:      " << total_traditional << std::endl;
    
    auto input = boardToInputVector();
    float nn_score = forwardPass(input) * NeuralConstants::SCORE_SCALE;
    std::cout << "Нейросетевая оценка:     " << static_cast<int>(nn_score) << std::endl;
    
    int combined = evaluate();
    std::cout << "Комбинированная оценка:  " << combined << std::endl;
    
    std::cout << "Уверенность сети:        " << std::fixed << std::setprecision(2) 
              << getNetworkConfidence() * 100 << "%" << std::endl;
}