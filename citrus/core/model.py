"""
LSTM-based language model for learning writing style.
"""

import numpy as np
from typing import List, Tuple, Optional
from .layers import LSTMCell, EmbeddingLayer, DenseLayer, Activation


class LanguageModel:
    """
    LSTM-based language model built from scratch.
    Learns to predict next character/word given a sequence.
    """
    
    def __init__(self, vocab_size: int, embedding_dim: int = 128, hidden_size: int = 256):
        """
        Initialize the language model.
        
        Args:
            vocab_size: Size of vocabulary
            embedding_dim: Dimension of embedding vectors
            hidden_size: Size of LSTM hidden state
        """
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.hidden_size = hidden_size
        
        # Initialize layers
        self.embedding = EmbeddingLayer(vocab_size, embedding_dim)
        self.lstm = LSTMCell(embedding_dim, hidden_size)
        self.output_layer = DenseLayer(hidden_size, vocab_size)
        
        # Training state
        self.h = np.zeros((hidden_size, 1))
        self.c = np.zeros((hidden_size, 1))
    
    def reset_state(self) -> None:
        """Reset hidden and cell states."""
        self.h = np.zeros((self.hidden_size, 1))
        self.c = np.zeros((self.hidden_size, 1))
    
    def forward(self, token_idx: int) -> np.ndarray:
        """
        Forward pass for a single token.
        
        Args:
            token_idx: Input token index
            
        Returns:
            Probability distribution over vocabulary
        """
        # Get embedding
        x = self.embedding.forward(token_idx)
        
        # LSTM forward
        self.h, self.c = self.lstm.forward(x, self.h, self.c)
        
        # Output layer
        logits = self.output_layer.forward(self.h)
        
        # Softmax to get probabilities
        probs = Activation.softmax(logits)
        
        return probs
    
    def predict_sequence(self, sequence: List[int]) -> np.ndarray:
        """
        Process a sequence and return final prediction.
        
        Args:
            sequence: List of token indices
            
        Returns:
            Probability distribution for next token
        """
        self.reset_state()
        
        probs = None
        for token_idx in sequence:
            probs = self.forward(token_idx)
        
        return probs
    
    def compute_loss(self, sequence: List[int], target: int) -> float:
        """
        Compute cross-entropy loss for a sequence.
        
        Args:
            sequence: Input sequence
            target: Target token index
            
        Returns:
            Loss value
        """
        probs = self.predict_sequence(sequence)
        
        # Cross-entropy loss
        loss = -np.log(probs[target, 0] + 1e-8)
        
        return loss
    
    def get_all_params(self) -> dict:
        """Get all model parameters."""
        return {
            'embedding': self.embedding.get_params(),
            'lstm': self.lstm.get_params(),
            'output': self.output_layer.get_params()
        }
    
    def set_params(self, params: dict) -> None:
        """
        Set model parameters.
        
        Args:
            params: Dictionary of parameters
        """
        if 'embedding' in params:
            self.embedding.embeddings = params['embedding']['embeddings']
        
        if 'lstm' in params:
            lstm_params = params['lstm']
            for key, value in lstm_params.items():
                setattr(self.lstm, key, value)
        
        if 'output' in params:
            self.output_layer.W = params['output']['W']
            self.output_layer.b = params['output']['b']
