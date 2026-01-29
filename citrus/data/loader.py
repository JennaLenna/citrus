"""
Data loader for training the neural network.
"""

import os
from typing import List, Tuple
from .preprocessing import TextPreprocessor, SequenceGenerator


class DataLoader:
    """Loads and prepares text data for training."""
    
    def __init__(self, data_dir: str, seq_length: int = 100, level: str = 'char'):
        """
        Initialize data loader.
        
        Args:
            data_dir: Directory containing text files
            seq_length: Length of training sequences
            level: 'char' or 'word' level processing
        """
        self.data_dir = data_dir
        self.preprocessor = TextPreprocessor(level=level)
        self.seq_generator = SequenceGenerator(seq_length=seq_length)
        self.texts: List[str] = []
        
    def load_text_files(self, file_paths: List[str] = None) -> None:
        """
        Load text files from directory.
        
        Args:
            file_paths: Optional list of specific file paths to load
        """
        if file_paths is None:
            file_paths = []
            for filename in os.listdir(self.data_dir):
                if filename.endswith('.txt'):
                    file_paths.append(os.path.join(self.data_dir, filename))
        
        self.texts = []
        for file_path in file_paths:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                    cleaned = self.preprocessor.clean_text(text)
                    self.texts.append(cleaned)
    
    def prepare_training_data(self) -> Tuple[List[List[int]], List[int]]:
        """
        Prepare all training data.
        
        Returns:
            Tuple of (all_sequences, all_targets)
        """
        # Build vocabulary from all texts
        self.preprocessor.build_vocab(self.texts)
        
        all_sequences = []
        all_targets = []
        
        # Encode and create sequences for each text
        for text in self.texts:
            encoded = self.preprocessor.encode(text)
            sequences, targets = self.seq_generator.create_sequences(encoded)
            all_sequences.extend(sequences)
            all_targets.extend(targets)
        
        return all_sequences, all_targets
    
    def get_vocab_size(self) -> int:
        """Get the vocabulary size."""
        return self.preprocessor.vocab_size
