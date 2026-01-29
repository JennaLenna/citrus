"""
Text preprocessing utilities for the Citrus AI writing system.
Handles tokenization, encoding, and text cleaning.
"""

import re
from typing import List, Dict, Tuple


class TextPreprocessor:
    """Preprocesses text for training and generation."""
    
    def __init__(self, level: str = 'char'):
        """
        Initialize the preprocessor.
        
        Args:
            level: 'char' for character-level, 'word' for word-level
        """
        self.level = level
        self.vocab: Dict[str, int] = {}
        self.reverse_vocab: Dict[int, str] = {}
        self.vocab_size = 0
        
    def clean_text(self, text: str) -> str:
        """
        Clean input text while preserving style markers.
        
        Args:
            text: Raw input text
            
        Returns:
            Cleaned text
        """
        # Normalize whitespace but preserve paragraph breaks
        text = re.sub(r'\n\n+', '\n\n', text)
        text = re.sub(r'[ \t]+', ' ', text)
        return text.strip()
    
    def tokenize(self, text: str) -> List[str]:
        """
        Tokenize text into characters or words.
        
        Args:
            text: Input text
            
        Returns:
            List of tokens
        """
        if self.level == 'char':
            return list(text)
        else:  # word level
            # Simple word tokenization preserving punctuation
            tokens = []
            words = re.findall(r'\w+|[^\w\s]|\s+', text)
            return words
    
    def build_vocab(self, texts: List[str]) -> None:
        """
        Build vocabulary from a list of texts.
        
        Args:
            texts: List of text samples
        """
        unique_tokens = set()
        for text in texts:
            tokens = self.tokenize(text)
            unique_tokens.update(tokens)
        
        # Add special tokens
        self.vocab = {'<PAD>': 0, '<UNK>': 1, '<START>': 2, '<END>': 3}
        
        for i, token in enumerate(sorted(unique_tokens), start=4):
            self.vocab[token] = i
        
        self.reverse_vocab = {v: k for k, v in self.vocab.items()}
        self.vocab_size = len(self.vocab)
    
    def encode(self, text: str) -> List[int]:
        """
        Encode text to integer sequences.
        
        Args:
            text: Input text
            
        Returns:
            List of integer encodings
        """
        tokens = self.tokenize(text)
        return [self.vocab.get(token, self.vocab['<UNK>']) for token in tokens]
    
    def decode(self, encoded: List[int]) -> str:
        """
        Decode integer sequences back to text.
        
        Args:
            encoded: List of integer encodings
            
        Returns:
            Decoded text
        """
        tokens = [self.reverse_vocab.get(idx, '<UNK>') for idx in encoded]
        
        if self.level == 'char':
            return ''.join(tokens)
        else:
            # Reconstruct words with basic spacing
            result = []
            for token in tokens:
                if token in ['<PAD>', '<UNK>', '<START>', '<END>']:
                    continue
                result.append(token)
            return ''.join(result)


class SequenceGenerator:
    """Generates training sequences from text."""
    
    def __init__(self, seq_length: int = 100):
        """
        Initialize sequence generator.
        
        Args:
            seq_length: Length of each training sequence
        """
        self.seq_length = seq_length
    
    def create_sequences(self, encoded_text: List[int]) -> Tuple[List[List[int]], List[int]]:
        """
        Create input-output sequence pairs for training.
        
        Args:
            encoded_text: Encoded text as list of integers
            
        Returns:
            Tuple of (input_sequences, target_outputs)
        """
        sequences = []
        targets = []
        
        for i in range(len(encoded_text) - self.seq_length):
            seq = encoded_text[i:i + self.seq_length]
            target = encoded_text[i + self.seq_length]
            sequences.append(seq)
            targets.append(target)
        
        return sequences, targets
