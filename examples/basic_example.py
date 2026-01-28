#!/usr/bin/env python3
"""
Example: Training and generating text with Citrus AI
"""

import os
import sys

# Add parent directory to path to import citrus package
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from citrus.data.loader import DataLoader
from citrus.core.model import LanguageModel
from citrus.models.trainer import Trainer
from citrus.models.generator import TextGenerator


def main():
    """Run a simple training and generation example."""
    
    print("=" * 70)
    print("Citrus AI - Example Training and Generation")
    print("=" * 70)
    
    # Configuration
    data_dir = 'data/raw'
    checkpoint_dir = 'checkpoints'
    seq_length = 50
    embedding_dim = 64
    hidden_size = 128
    epochs = 5
    batch_size = 16
    
    # Ensure directories exist
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(checkpoint_dir, exist_ok=True)
    
    print("\n1. Loading training data...")
    
    # Load data
    data_loader = DataLoader(
        data_dir=data_dir,
        seq_length=seq_length,
        level='char'
    )
    
    data_loader.load_text_files()
    
    if not data_loader.texts:
        print(f"\nNo training data found in {data_dir}")
        print("Please add .txt files with sample writing to train on.")
        return
    
    print(f"   Found {len(data_loader.texts)} text file(s)")
    
    # Prepare data
    print("\n2. Preparing training sequences...")
    sequences, targets = data_loader.prepare_training_data()
    vocab_size = data_loader.get_vocab_size()
    
    print(f"   Vocabulary size: {vocab_size}")
    print(f"   Training sequences: {len(sequences)}")
    
    # Create model
    print("\n3. Creating language model...")
    model = LanguageModel(
        vocab_size=vocab_size,
        embedding_dim=embedding_dim,
        hidden_size=hidden_size
    )
    
    print(f"   Model created with {embedding_dim}D embeddings and {hidden_size}D hidden state")
    
    # Train
    print("\n4. Training model (this may take a while)...")
    trainer = Trainer(model, learning_rate=0.001)
    
    # Note: For demonstration, using small number of samples
    # In production, you'd train on the full dataset
    num_samples = min(100, len(sequences))
    
    print(f"   Training on {num_samples} samples for demonstration...")
    trainer.train(
        sequences=sequences[:num_samples],
        targets=targets[:num_samples],
        epochs=epochs,
        batch_size=batch_size,
        checkpoint_dir=checkpoint_dir
    )
    
    # Generate text
    print("\n5. Generating sample text...")
    generator = TextGenerator(model, data_loader.preprocessor)
    
    prompts = [
        "It was",
        "The",
        "Winston"
    ]
    
    for prompt in prompts:
        print(f"\n   Prompt: '{prompt}'")
        generated = generator.generate(
            seed_text=prompt,
            length=100,
            temperature=0.7,
            top_k=5
        )
        print(f"   Generated: {generated[:200]}...")
    
    print("\n" + "=" * 70)
    print("Example completed!")
    print(f"Model checkpoint saved to: {checkpoint_dir}")
    print("=" * 70)


if __name__ == '__main__':
    main()
