"""
Core neural network components built from scratch using only NumPy.
No existing ML frameworks are used.
"""

import numpy as np
from typing import Tuple, Optional


class Activation:
    """Activation functions and their derivatives."""
    
    @staticmethod
    def tanh(x: np.ndarray) -> np.ndarray:
        """Hyperbolic tangent activation."""
        return np.tanh(x)
    
    @staticmethod
    def tanh_derivative(x: np.ndarray) -> np.ndarray:
        """Derivative of tanh."""
        return 1 - np.tanh(x) ** 2
    
    @staticmethod
    def sigmoid(x: np.ndarray) -> np.ndarray:
        """Sigmoid activation."""
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))
    
    @staticmethod
    def sigmoid_derivative(x: np.ndarray) -> np.ndarray:
        """Derivative of sigmoid."""
        s = Activation.sigmoid(x)
        return s * (1 - s)
    
    @staticmethod
    def softmax(x: np.ndarray) -> np.ndarray:
        """Softmax activation for output layer."""
        # Flatten if 2D with shape (n, 1)
        if x.ndim == 2 and x.shape[1] == 1:
            x = x.flatten()
        
        # Subtract max for numerical stability
        x_exp = np.exp(x - np.max(x))
        result = x_exp / np.sum(x_exp)
        
        # Restore original shape if needed
        if len(result.shape) == 1:
            result = result.reshape(-1, 1)
        
        return result


class LSTMCell:
    """
    Single LSTM cell implementation from scratch.
    
    LSTM has four gates: input, forget, output, and cell state.
    """
    
    def __init__(self, input_size: int, hidden_size: int):
        """
        Initialize LSTM cell.
        
        Args:
            input_size: Size of input vector
            hidden_size: Size of hidden state
        """
        self.input_size = input_size
        self.hidden_size = hidden_size
        
        # Initialize weights using Xavier initialization
        scale = np.sqrt(2.0 / (input_size + hidden_size))
        
        # Input gate weights
        self.W_i = np.random.randn(hidden_size, input_size) * scale
        self.U_i = np.random.randn(hidden_size, hidden_size) * scale
        self.b_i = np.zeros((hidden_size, 1))
        
        # Forget gate weights
        self.W_f = np.random.randn(hidden_size, input_size) * scale
        self.U_f = np.random.randn(hidden_size, hidden_size) * scale
        self.b_f = np.ones((hidden_size, 1))  # Bias to 1 for forget gate
        
        # Output gate weights
        self.W_o = np.random.randn(hidden_size, input_size) * scale
        self.U_o = np.random.randn(hidden_size, hidden_size) * scale
        self.b_o = np.zeros((hidden_size, 1))
        
        # Cell state weights
        self.W_c = np.random.randn(hidden_size, input_size) * scale
        self.U_c = np.random.randn(hidden_size, hidden_size) * scale
        self.b_c = np.zeros((hidden_size, 1))
        
        # Cache for backward pass
        self.cache = {}
    
    def forward(self, x: np.ndarray, h_prev: np.ndarray, c_prev: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Forward pass through LSTM cell.
        
        Args:
            x: Input vector (input_size, 1)
            h_prev: Previous hidden state (hidden_size, 1)
            c_prev: Previous cell state (hidden_size, 1)
            
        Returns:
            Tuple of (h_next, c_next)
        """
        # Input gate
        i_t = Activation.sigmoid(np.dot(self.W_i, x) + np.dot(self.U_i, h_prev) + self.b_i)
        
        # Forget gate
        f_t = Activation.sigmoid(np.dot(self.W_f, x) + np.dot(self.U_f, h_prev) + self.b_f)
        
        # Output gate
        o_t = Activation.sigmoid(np.dot(self.W_o, x) + np.dot(self.U_o, h_prev) + self.b_o)
        
        # Candidate cell state
        c_tilde = Activation.tanh(np.dot(self.W_c, x) + np.dot(self.U_c, h_prev) + self.b_c)
        
        # Cell state
        c_next = f_t * c_prev + i_t * c_tilde
        
        # Hidden state
        h_next = o_t * Activation.tanh(c_next)
        
        # Cache values for backward pass
        self.cache = {
            'x': x, 'h_prev': h_prev, 'c_prev': c_prev,
            'i_t': i_t, 'f_t': f_t, 'o_t': o_t,
            'c_tilde': c_tilde, 'c_next': c_next, 'h_next': h_next
        }
        
        return h_next, c_next
    
    def get_params(self) -> dict:
        """Get all parameters."""
        return {
            'W_i': self.W_i, 'U_i': self.U_i, 'b_i': self.b_i,
            'W_f': self.W_f, 'U_f': self.U_f, 'b_f': self.b_f,
            'W_o': self.W_o, 'U_o': self.U_o, 'b_o': self.b_o,
            'W_c': self.W_c, 'U_c': self.U_c, 'b_c': self.b_c
        }


class EmbeddingLayer:
    """Embedding layer to convert tokens to dense vectors."""
    
    def __init__(self, vocab_size: int, embedding_dim: int):
        """
        Initialize embedding layer.
        
        Args:
            vocab_size: Size of vocabulary
            embedding_dim: Dimension of embedding vectors
        """
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        
        # Initialize embeddings
        self.embeddings = np.random.randn(vocab_size, embedding_dim) * 0.01
    
    def forward(self, token_idx: int) -> np.ndarray:
        """
        Get embedding for a token.
        
        Args:
            token_idx: Token index
            
        Returns:
            Embedding vector (embedding_dim, 1)
        """
        return self.embeddings[token_idx].reshape(-1, 1)
    
    def get_params(self) -> dict:
        """Get parameters."""
        return {'embeddings': self.embeddings}


class DenseLayer:
    """Fully connected dense layer."""
    
    def __init__(self, input_size: int, output_size: int):
        """
        Initialize dense layer.
        
        Args:
            input_size: Size of input
            output_size: Size of output
        """
        self.input_size = input_size
        self.output_size = output_size
        
        # Initialize weights
        scale = np.sqrt(2.0 / input_size)
        self.W = np.random.randn(output_size, input_size) * scale
        self.b = np.zeros((output_size, 1))
    
    def forward(self, x: np.ndarray) -> np.ndarray:
        """
        Forward pass.
        
        Args:
            x: Input (input_size, 1)
            
        Returns:
            Output (output_size, 1)
        """
        return np.dot(self.W, x) + self.b
    
    def get_params(self) -> dict:
        """Get parameters."""
        return {'W': self.W, 'b': self.b}
