"""
Unit tests for neural network layers.
"""

import unittest
import numpy as np
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from citrus.core.layers import Activation, LSTMCell, EmbeddingLayer, DenseLayer


class TestActivation(unittest.TestCase):
    """Test activation functions."""
    
    def test_sigmoid(self):
        """Test sigmoid activation."""
        x = np.array([0.0])
        result = Activation.sigmoid(x)
        self.assertAlmostEqual(result[0], 0.5, places=5)
    
    def test_tanh(self):
        """Test tanh activation."""
        x = np.array([0.0])
        result = Activation.tanh(x)
        self.assertEqual(result[0], 0.0)
    
    def test_softmax(self):
        """Test softmax activation."""
        x = np.array([[1.0, 2.0, 3.0]])
        result = Activation.softmax(x)
        
        # Softmax should sum to 1
        self.assertAlmostEqual(np.sum(result), 1.0, places=5)


class TestLSTMCell(unittest.TestCase):
    """Test LSTM cell."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.lstm = LSTMCell(input_size=10, hidden_size=20)
    
    def test_initialization(self):
        """Test LSTM cell initialization."""
        self.assertEqual(self.lstm.input_size, 10)
        self.assertEqual(self.lstm.hidden_size, 20)
        
        # Check weight shapes
        self.assertEqual(self.lstm.W_i.shape, (20, 10))
        self.assertEqual(self.lstm.U_i.shape, (20, 20))
    
    def test_forward(self):
        """Test forward pass."""
        x = np.random.randn(10, 1)
        h_prev = np.zeros((20, 1))
        c_prev = np.zeros((20, 1))
        
        h_next, c_next = self.lstm.forward(x, h_prev, c_prev)
        
        # Check output shapes
        self.assertEqual(h_next.shape, (20, 1))
        self.assertEqual(c_next.shape, (20, 1))


class TestEmbeddingLayer(unittest.TestCase):
    """Test embedding layer."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.embedding = EmbeddingLayer(vocab_size=100, embedding_dim=50)
    
    def test_initialization(self):
        """Test initialization."""
        self.assertEqual(self.embedding.vocab_size, 100)
        self.assertEqual(self.embedding.embedding_dim, 50)
        self.assertEqual(self.embedding.embeddings.shape, (100, 50))
    
    def test_forward(self):
        """Test forward pass."""
        embedding_vector = self.embedding.forward(5)
        
        # Check output shape
        self.assertEqual(embedding_vector.shape, (50, 1))


class TestDenseLayer(unittest.TestCase):
    """Test dense layer."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.dense = DenseLayer(input_size=10, output_size=5)
    
    def test_initialization(self):
        """Test initialization."""
        self.assertEqual(self.dense.input_size, 10)
        self.assertEqual(self.dense.output_size, 5)
        self.assertEqual(self.dense.W.shape, (5, 10))
    
    def test_forward(self):
        """Test forward pass."""
        x = np.random.randn(10, 1)
        output = self.dense.forward(x)
        
        # Check output shape
        self.assertEqual(output.shape, (5, 1))


if __name__ == '__main__':
    unittest.main()
