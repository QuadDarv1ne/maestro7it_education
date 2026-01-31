#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Enhanced Neural Network Chess Evaluator
Deep learning-based position evaluation with multiple layers
"""

import numpy as np
from typing import List, Tuple, Dict, Optional
import math
import pickle
import os

class NeuralNetworkEvaluator:
    """Deep neural network for chess position evaluation"""
    
    def __init__(self, hidden_layers: List[int] = [512, 256, 128]):
        """
        Initialize neural network evaluator
        
        Args:
            hidden_layers: List of hidden layer sizes
        """
        self.input_size = 772  # 64 squares × 12 piece types + 4 castling rights + 1 en passant + 1 side to move
        self.hidden_layers = hidden_layers
        self.output_size = 1   # Single evaluation score
        
        # Initialize weights and biases
        self.weights = []
        self.biases = []
        
        # Input to first hidden layer
        self.weights.append(np.random.randn(self.input_size, hidden_layers[0]) * 0.1)
        self.biases.append(np.zeros((1, hidden_layers[0])))
        
        # Hidden layers
        for i in range(len(hidden_layers) - 1):
            self.weights.append(np.random.randn(hidden_layers[i], hidden_layers[i + 1]) * 0.1)
            self.biases.append(np.zeros((1, hidden_layers[i + 1])))
        
        # Last hidden to output
        self.weights.append(np.random.randn(hidden_layers[-1], self.output_size) * 0.1)
        self.biases.append(np.zeros((1, self.output_size)))
        
        # Activation functions
        self.activation = self._relu
        self.activation_derivative = self._relu_derivative
        
        # Training parameters
        self.learning_rate = 0.001
        self.momentum = 0.9
        self.velocity = [np.zeros_like(w) for w in self.weights]
        
        # Cache for faster inference
        self.eval_cache = {}
        self.cache_hits = 0
        self.cache_misses = 0
        
        print(f"🧠 Neural Network Evaluator initialized")
        print(f"   Architecture: {self.input_size} → {' → '.join(map(str, hidden_layers))} → {self.output_size}")
        print(f"   Parameters: {self._count_parameters():,}")
    
    def _count_parameters(self) -> int:
        """Count total trainable parameters"""
        total = 0
        for w, b in zip(self.weights, self.biases):
            total += w.size + b.size
        return total
    
    def _relu(self, x: np.ndarray) -> np.ndarray:
        """ReLU activation function"""
        return np.maximum(0, x)
    
    def _relu_derivative(self, x: np.ndarray) -> np.ndarray:
        """Derivative of ReLU"""
        return (x > 0).astype(float)
    
    def _tanh(self, x: np.ndarray) -> np.ndarray:
        """Tanh activation function"""
        return np.tanh(x)
    
    def _tanh_derivative(self, x: np.ndarray) -> np.ndarray:
        """Derivative of tanh"""
        return 1 - np.tanh(x) ** 2
    
    def _sigmoid(self, x: np.ndarray) -> np.ndarray:
        """Sigmoid activation function"""
        # Clip to prevent overflow
        x = np.clip(x, -500, 500)
        return 1 / (1 + np.exp(-x))
    
    def _sigmoid_derivative(self, x: np.ndarray) -> np.ndarray:
        """Derivative of sigmoid"""
        s = self._sigmoid(x)
        return s * (1 - s)
    
    def board_to_input_vector(self, board: List[List[str]], turn: bool = True) -> np.ndarray:
        """
        Convert board position to input vector for neural network
        
        Args:
            board: 8x8 board representation
            turn: True for white, False for black
            
        Returns:
            Input vector of size 772
        """
        # Piece encoding (12 piece types)
        piece_to_index = {
            'P': 0, 'N': 1, 'B': 2, 'R': 3, 'Q': 4, 'K': 5,
            'p': 6, 'n': 7, 'b': 8, 'r': 9, 'q': 10, 'k': 11
        }
        
        # Initialize input vector
        input_vector = np.zeros(self.input_size)
        
        # Encode piece positions (64 squares × 12 piece types = 768)
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece != '.':
                    piece_idx = piece_to_index[piece]
                    square_idx = row * 8 + col
                    input_vector[square_idx * 12 + piece_idx] = 1
        
        # Encode game state (last 4 elements)
        # Castling rights, en passant, side to move would go here
        # For simplicity, we'll use the last element for side to move
        input_vector[-1] = 1 if turn else -1
        
        return input_vector.reshape(1, -1)
    
    def forward_pass(self, input_vector: np.ndarray) -> Tuple[np.ndarray, List[np.ndarray]]:
        """
        Forward pass through the network
        
        Args:
            input_vector: Input vector of shape (1, input_size)
            
        Returns:
            Output value and list of layer activations
        """
        activations = [input_vector]
        current = input_vector
        
        # Hidden layers
        for i in range(len(self.weights) - 1):
            z = np.dot(current, self.weights[i]) + self.biases[i]
            a = self.activation(z)
            activations.append(a)
            current = a
        
        # Output layer (linear activation for evaluation)
        z = np.dot(current, self.weights[-1]) + self.biases[-1]
        output = z  # Linear activation for regression
        activations.append(output)
        
        return output, activations
    
    def evaluate_position(self, board: List[List[str]], turn: bool = True) -> float:
        """
        Evaluate chess position using neural network
        
        Args:
            board: 8x8 board representation
            turn: True for white, False for black
            
        Returns:
            Position evaluation score (positive = white advantage)
        """
        # Check cache first
        board_tuple = tuple(tuple(row) for row in board)
        cache_key = (board_tuple, turn)
        
        if cache_key in self.eval_cache:
            self.cache_hits += 1
            return self.eval_cache[cache_key]
        
        self.cache_misses += 1
        
        # Convert board to input vector
        input_vector = self.board_to_input_vector(board, turn)
        
        # Forward pass
        output, _ = self.forward_pass(input_vector)
        
        # Convert to centipawns (typical chess evaluation scale)
        score = float(output[0, 0]) * 100
        
        # Cache result
        self.eval_cache[cache_key] = score
        
        return score
    
    def train_step(self, input_vectors: np.ndarray, target_scores: np.ndarray) -> float:
        """
        Single training step using backpropagation
        
        Args:
            input_vectors: Batch of input vectors (batch_size, input_size)
            target_scores: Target scores (batch_size, 1)
            
        Returns:
            Mean squared error loss
        """
        # Forward pass
        activations = [input_vectors]
        current = input_vectors
        
        for i in range(len(self.weights) - 1):
            z = np.dot(current, self.weights[i]) + self.biases[i]
            a = self.activation(z)
            activations.append(a)
            current = a
        
        # Output layer
        z = np.dot(current, self.weights[-1]) + self.biases[-1]
        output = z
        activations.append(output)
        
        # Calculate loss
        loss = np.mean((output - target_scores) ** 2)
        
        # Backward pass
        # Output layer gradient
        delta = 2 * (output - target_scores) / len(target_scores)
        
        # Backpropagate through layers
        for i in reversed(range(len(self.weights))):
            # Weight gradients
            dW = np.dot(activations[i].T, delta)
            db = np.sum(delta, axis=0, keepdims=True)
            
            # Update weights with momentum
            self.velocity[i] = self.momentum * self.velocity[i] - self.learning_rate * dW
            self.weights[i] += self.velocity[i]
            self.biases[i] -= self.learning_rate * db
            
            # Previous layer delta (except for input layer)
            if i > 0:
                delta = np.dot(delta, self.weights[i].T) * self.activation_derivative(
                    np.dot(activations[i-1], self.weights[i-1]) + self.biases[i-1]
                )
        
        return float(loss)
    
    def get_cache_hit_rate(self) -> float:
        """Get evaluation cache hit rate"""
        total = self.cache_hits + self.cache_misses
        return (self.cache_hits / total * 100) if total > 0 else 0.0
    
    def save_model(self, filepath: str):
        """Save model weights to file"""
        model_data = {
            'weights': self.weights,
            'biases': self.biases,
            'hidden_layers': self.hidden_layers,
            'learning_rate': self.learning_rate,
            'momentum': self.momentum
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
        
        print(f"💾 Model saved to {filepath}")
    
    def load_model(self, filepath: str):
        """Load model weights from file"""
        if not os.path.exists(filepath):
            print(f"⚠️ Model file {filepath} not found")
            return False
        
        try:
            with open(filepath, 'rb') as f:
                model_data = pickle.load(f)
            
            self.weights = model_data['weights']
            self.biases = model_data['biases']
            self.hidden_layers = model_data['hidden_layers']
            self.learning_rate = model_data['learning_rate']
            self.momentum = model_data['momentum']
            
            print(f"📂 Model loaded from {filepath}")
            return True
        except Exception as e:
            print(f"❌ Failed to load model: {e}")
            return False
    
    def clear_cache(self):
        """Clear evaluation cache"""
        self.eval_cache.clear()
        self.cache_hits = 0
        self.cache_misses = 0

class HybridEvaluator:
    """Combines traditional evaluation with neural network"""
    
    def __init__(self, nn_model_path: Optional[str] = None):
        self.nn_evaluator = NeuralNetworkEvaluator([512, 256, 128])
        
        # Load pre-trained model if available
        if nn_model_path and os.path.exists(nn_model_path):
            self.nn_evaluator.load_model(nn_model_path)
        
        # Traditional evaluation weights
        self.traditional_weight = 0.3  # 30% traditional
        self.neural_weight = 0.7      # 70% neural
        
        print(f"🔄 Hybrid evaluator initialized")
        print(f"   Mix ratio: {self.traditional_weight*100:.0f}% traditional + {self.neural_weight*100:.0f}% neural")
    
    def evaluate_position(self, board: List[List[str]], turn: bool = True) -> float:
        """
        Hybrid evaluation combining traditional and neural approaches
        """
        # Neural network evaluation
        nn_score = self.nn_evaluator.evaluate_position(board, turn)
        
        # Traditional evaluation (simplified)
        traditional_score = self._traditional_evaluation(board, turn)
        
        # Combine evaluations
        final_score = (
            self.traditional_weight * traditional_score + 
            self.neural_weight * nn_score
        )
        
        return final_score
    
    def _traditional_evaluation(self, board: List[List[str]], turn: bool) -> float:
        """Traditional material and positional evaluation"""
        piece_values = {
            'P': 100, 'N': 320, 'B': 330, 'R': 500, 'Q': 900, 'K': 20000,
            'p': -100, 'n': -320, 'b': -330, 'r': -500, 'q': -900, 'k': -20000
        }
        
        # Material evaluation
        material_score = 0
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece in piece_values:
                    material_score += piece_values[piece]
        
        # Simple positional bonuses
        positional_score = 0
        center_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]
        
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece != '.':
                    # Center control bonus
                    if (row, col) in center_squares:
                        bonus = 5 if piece.isupper() else -5
                        positional_score += bonus
                    
                    # Development bonus for minor pieces
                    if piece.lower() in ['n', 'b']:
                        if (2 <= row <= 5) and (2 <= col <= 5):
                            bonus = 3 if piece.isupper() else -3
                            positional_score += bonus
        
        total_score = material_score + positional_score
        
        # Adjust for side to move
        if not turn:  # Black to move
            total_score = -total_score
            
        return total_score / 100.0  # Convert to pawn units

# Test function
def test_neural_evaluator():
    """Test the neural network evaluator"""
    print("🧠 NEURAL NETWORK EVALUATOR TEST")
    print("=" * 50)
    
    # Create hybrid evaluator
    evaluator = HybridEvaluator()
    
    # Test positions
    test_positions = [
        # Starting position
        ([
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ], True, "Starting position"),
        
        # Queen sacrifice position
        ([
            ['r', '.', '.', '.', 'k', '.', '.', 'r'],
            ['p', 'p', 'p', '.', '.', 'p', 'p', 'p'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', 'p', 'p', '.', '.', '.'],
            ['.', '.', '.', 'P', 'P', '.', '.', '.'],
            ['.', '.', '.', '.', '.', 'N', '.', '.'],
            ['P', 'P', 'P', '.', '.', 'P', 'P', 'P'],
            ['R', '.', 'B', 'Q', 'K', 'B', '.', 'R']
        ], True, "Mid-game position"),
        
        # Endgame position
        ([
            ['.', '.', '.', '.', 'k', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', 'K', '.', '.', '.']
        ], True, "Endgame position")
    ]
    
    print("Testing position evaluations...")
    
    for board, turn, description in test_positions:
        print(f"\n{description}:")
        
        # Traditional evaluation
        trad_score = evaluator._traditional_evaluation(board, turn)
        print(f"  Traditional: {trad_score:.2f}")
        
        # Neural network evaluation
        nn_score = evaluator.nn_evaluator.evaluate_position(board, turn)
        print(f"  Neural Net: {nn_score:.2f}")
        
        # Hybrid evaluation
        hybrid_score = evaluator.evaluate_position(board, turn)
        print(f"  Hybrid: {hybrid_score:.2f}")
        
        # Cache statistics
        cache_rate = evaluator.nn_evaluator.get_cache_hit_rate()
        print(f"  NN Cache hit rate: {cache_rate:.1f}%")
    
    # Test cache effectiveness
    print(f"\n🔁 Testing cache performance...")
    board, turn, _ = test_positions[0]
    
    # First evaluation (uncached)
    score1 = evaluator.evaluate_position(board, turn)
    hits1 = evaluator.nn_evaluator.cache_hits
    
    # Second evaluation (cached)
    score2 = evaluator.evaluate_position(board, turn)
    hits2 = evaluator.nn_evaluator.cache_hits
    
    print(f"  First call: {score1:.2f} (cache hits: {hits1})")
    print(f"  Second call: {score2:.2f} (cache hits: {hits2})")
    print(f"  Cache working: {'✅' if hits2 > hits1 else '❌'}")
    
    print(f"\n✅ Neural network evaluator test completed!")

if __name__ == "__main__":
    test_neural_evaluator()