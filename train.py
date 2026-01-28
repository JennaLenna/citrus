#!/usr/bin/env python3
"""
CLI for training the Citrus AI writing model.
"""

import argparse
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from citrus.data.loader import DataLoader
from citrus.core.model import LanguageModel
from citrus.models.trainer import Trainer
from citrus.utils.helpers import create_directory_structure


def main():
    parser = argparse.ArgumentParser(
        description='Train the Citrus AI writing style model'
    )
    
    parser.add_argument(
        '--data-dir',
        type=str,
        default='data/raw',
        help='Directory containing training text files'
    )
    
    parser.add_argument(
        '--checkpoint-dir',
        type=str,
        default='checkpoints',
        help='Directory to save model checkpoints'
    )
    
    parser.add_argument(
        '--seq-length',
        type=int,
        default=100,
        help='Length of training sequences'
    )
    
    parser.add_argument(
        '--embedding-dim',
        type=int,
        default=128,
        help='Dimension of embedding vectors'
    )
    
    parser.add_argument(
        '--hidden-size',
        type=int,
        default=256,
        help='Size of LSTM hidden state'
    )
    
    parser.add_argument(
        '--epochs',
        type=int,
        default=10,
        help='Number of training epochs'
    )
    
    parser.add_argument(
        '--batch-size',
        type=int,
        default=32,
        help='Training batch size'
    )
    
    parser.add_argument(
        '--learning-rate',
        type=float,
        default=0.001,
        help='Learning rate'
    )
    
    parser.add_argument(
        '--level',
        type=str,
        choices=['char', 'word'],
        default='char',
        help='Character or word level processing'
    )
    
    args = parser.parse_args()
    
    # Create directory structure
    create_directory_structure('.')
    
    print("=" * 60)
    print("Citrus AI Writing Style Model - Training")
    print("=" * 60)
    
    # Load data
    print(f"\n1. Loading data from {args.data_dir}...")
    data_loader = DataLoader(
        data_dir=args.data_dir,
        seq_length=args.seq_length,
        level=args.level
    )
    
    data_loader.load_text_files()
    
    if not data_loader.texts:
        print(f"Error: No text files found in {args.data_dir}")
        print(f"Please add .txt files with training data to {args.data_dir}")
        return 1
    
    print(f"   Loaded {len(data_loader.texts)} text file(s)")
    
    # Prepare training data
    print("\n2. Preparing training data...")
    sequences, targets = data_loader.prepare_training_data()
    vocab_size = data_loader.get_vocab_size()
    
    print(f"   Vocabulary size: {vocab_size}")
    print(f"   Training samples: {len(sequences)}")
    
    # Create model
    print("\n3. Creating model...")
    model = LanguageModel(
        vocab_size=vocab_size,
        embedding_dim=args.embedding_dim,
        hidden_size=args.hidden_size
    )
    
    print(f"   Embedding dimension: {args.embedding_dim}")
    print(f"   Hidden size: {args.hidden_size}")
    
    # Create trainer
    print("\n4. Starting training...")
    trainer = Trainer(model, learning_rate=args.learning_rate)
    
    trainer.train(
        sequences=sequences,
        targets=targets,
        epochs=args.epochs,
        batch_size=args.batch_size,
        checkpoint_dir=args.checkpoint_dir
    )
    
    # Save final model
    print("\n5. Saving final model...")
    trainer.save_checkpoint(args.checkpoint_dir, args.epochs)
    
    print("\n" + "=" * 60)
    print("Training completed successfully!")
    print(f"Checkpoints saved to: {args.checkpoint_dir}")
    print("=" * 60)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
