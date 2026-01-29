#ifndef NEURAL_EVALUATOR_HPP
#define NEURAL_EVALUATOR_HPP

#include <vector>
#include <array>
#include <cmath>
#include <random>

/**
 * @brief Нейронная сеть для оценки шахматных позиций
 * 
 * Реализует простую_feedforward нейронную сеть для оценки позиции
 * на основе материала, структуры, безопасности короля и других факторов.
 */
class NeuralEvaluator {
private:
    // Архитектура сети
    static const int INPUT_SIZE = 768;    // 64 клетки × 12 типов фигур
    static const int HIDDEN_SIZE = 256;   // Скрытые нейроны
    static const int OUTPUT_SIZE = 1;     // Оценка позиции
    
    // Веса сети
    std::vector<std::vector<double>> weights_input_hidden;
    std::vector<std::vector<double>> weights_hidden_output;
    std::vector<double> bias_hidden;
    std::vector<double> bias_output;
    
    // Активационные функции
    double sigmoid(double x) const {
        return 1.0 / (1.0 + std::exp(-x));
    }
    
    double relu(double x) const {
        return std::max(0.0, x);
    }
    
    // Инициализация весов
    void initializeWeights() {
        std::random_device rd;
        std::mt19937 gen(rd());
        std::normal_distribution<double> dis(0.0, 0.1);
        
        // Веса вход-скрытый слой
        weights_input_hidden.resize(HIDDEN_SIZE, std::vector<double>(INPUT_SIZE));
        for (int i = 0; i < HIDDEN_SIZE; i++) {
            for (int j = 0; j < INPUT_SIZE; j++) {
                weights_input_hidden[i][j] = dis(gen);
            }
        }
        
        // Веса скрытый-выход слой
        weights_hidden_output.resize(OUTPUT_SIZE, std::vector<double>(HIDDEN_SIZE));
        for (int i = 0; i < OUTPUT_SIZE; i++) {
            for (int j = 0; j < HIDDEN_SIZE; j++) {
                weights_hidden_output[i][j] = dis(gen);
            }
        }
        
        // Смещения
        bias_hidden.resize(HIDDEN_SIZE, 0.0);
        bias_output.resize(OUTPUT_SIZE, 0.0);
    }
    
public:
    NeuralEvaluator() {
        initializeWeights();
    }
    
    /**
     * @brief Преобразует доску в вектор признаков
     * @param board_state Текущее состояние доски
     * @return Вектор признаков размером 768
     */
    std::vector<double> boardToFeatures(const std::array<int, 64>& board_state) const {
        std::vector<double> features(INPUT_SIZE, 0.0);
        
        for (int square = 0; square < 64; square++) {
            int piece = board_state[square];
            if (piece != 0) {
                // piece: 1-6 белые, 7-12 черные
                int piece_index = piece - 1;
                int feature_index = square * 12 + piece_index;
                if (feature_index < INPUT_SIZE) {
                    features[feature_index] = 1.0;
                }
            }
        }
        
        return features;
    }
    
    /**
     * @brief Прямое распространение через сеть
     * @param inputs Входные признаки
     * @return Оценка позиции (-10000 до +10000)
     */
    int evaluatePosition(const std::vector<double>& inputs) const {
        // Скрытый слой
        std::vector<double> hidden(HIDDEN_SIZE, 0.0);
        for (int i = 0; i < HIDDEN_SIZE; i++) {
            for (int j = 0; j < INPUT_SIZE; j++) {
                hidden[i] += inputs[j] * weights_input_hidden[i][j];
            }
            hidden[i] += bias_hidden[i];
            hidden[i] = relu(hidden[i]); // ReLU активация
        }
        
        // Выходной слой
        double output = 0.0;
        for (int i = 0; i < HIDDEN_SIZE; i++) {
            output += hidden[i] * weights_hidden_output[0][i];
        }
        output += bias_output[0];
        output = sigmoid(output); // Sigmoid активация
        
        // Преобразуем в шахматную оценку (-10000 до +10000)
        return static_cast<int>((output * 2.0 - 1.0) * 10000);
    }
    
    /**
     * @brief Основной метод оценки позиции
     * @param board_state Состояние доски
     * @return Оценка позиции
     */
    int evaluate(const std::array<int, 64>& board_state) const {
        auto features = boardToFeatures(board_state);
        return evaluatePosition(features);
    }
    
    /**
     * @brief Обучение сети (упрощенная версия)
     * @param training_data Обучающие примеры
     * @param epochs Количество эпох обучения
     */
    void train(const std::vector<std::pair<std::array<int, 64>, int>>& training_data, 
               int epochs = 100) {
        // Упрощенная реализация стохастического градиентного спуска
        const double learning_rate = 0.01;
        
        for (int epoch = 0; epoch < epochs; epoch++) {
            for (const auto& sample : training_data) {
                const auto& board = sample.first;
                int target = sample.second;
                
                // Прямое распространение
                auto features = boardToFeatures(board);
                auto hidden = std::vector<double>(HIDDEN_SIZE, 0.0);
                
                for (int i = 0; i < HIDDEN_SIZE; i++) {
                    for (int j = 0; j < INPUT_SIZE; j++) {
                        hidden[i] += features[j] * weights_input_hidden[i][j];
                    }
                    hidden[i] += bias_hidden[i];
                    hidden[i] = relu(hidden[i]);
                }
                
                double output = 0.0;
                for (int i = 0; i < HIDDEN_SIZE; i++) {
                    output += hidden[i] * weights_hidden_output[0][i];
                }
                output += bias_output[0];
                double predicted = sigmoid(output);
                
                // Обратное распространение (упрощенное)
                double error = (target / 10000.0 + 1.0) / 2.0 - predicted;
                
                // Обновление весов (градиентный спуск)
                double delta_output = error * predicted * (1.0 - predicted);
                bias_output[0] += learning_rate * delta_output;
                
                for (int i = 0; i < HIDDEN_SIZE; i++) {
                    weights_hidden_output[0][i] += learning_rate * delta_output * hidden[i];
                }
            }
        }
    }
};

#endif // NEURAL_EVALUATOR_HPP