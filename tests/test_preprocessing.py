"""
Unit tests for text preprocessing components.
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from citrus.data.preprocessing import TextPreprocessor, SequenceGenerator


class TestTextPreprocessor(unittest.TestCase):
    """Test the TextPreprocessor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.preprocessor = TextPreprocessor(level='char')
    
    def test_clean_text(self):
        """Test text cleaning."""
        text = "Hello   world\n\n\nTest"
        cleaned = self.preprocessor.clean_text(text)
        # Whitespace should be normalized to single spaces
        self.assertEqual(cleaned, "Hello world\n\nTest")
    
    def test_char_tokenization(self):
        """Test character-level tokenization."""
        text = "Hello"
        tokens = self.preprocessor.tokenize(text)
        self.assertEqual(tokens, ['H', 'e', 'l', 'l', 'o'])
    
    def test_word_tokenization(self):
        """Test word-level tokenization."""
        preprocessor = TextPreprocessor(level='word')
        text = "Hello, world!"
        tokens = preprocessor.tokenize(text)
        self.assertIn('Hello', tokens)
        self.assertIn('world', tokens)
    
    def test_build_vocab(self):
        """Test vocabulary building."""
        texts = ["hello", "world"]
        self.preprocessor.build_vocab(texts)
        
        # Check special tokens
        self.assertIn('<PAD>', self.preprocessor.vocab)
        self.assertIn('<UNK>', self.preprocessor.vocab)
        
        # Check vocab size
        self.assertGreater(self.preprocessor.vocab_size, 0)
    
    def test_encode_decode(self):
        """Test encoding and decoding."""
        texts = ["hello"]
        self.preprocessor.build_vocab(texts)
        
        encoded = self.preprocessor.encode("hello")
        decoded = self.preprocessor.decode(encoded)
        
        self.assertEqual(decoded, "hello")


class TestSequenceGenerator(unittest.TestCase):
    """Test the SequenceGenerator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.generator = SequenceGenerator(seq_length=3)
    
    def test_create_sequences(self):
        """Test sequence creation."""
        encoded = [1, 2, 3, 4, 5, 6]
        sequences, targets = self.generator.create_sequences(encoded)
        
        # Should create len(encoded) - seq_length sequences
        self.assertEqual(len(sequences), 3)
        self.assertEqual(len(targets), 3)
        
        # Check first sequence
        self.assertEqual(sequences[0], [1, 2, 3])
        self.assertEqual(targets[0], 4)


if __name__ == '__main__':
    unittest.main()
