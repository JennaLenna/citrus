#!/usr/bin/env python3
"""
Pre-train a model on the training corpus to create a smart starting point
for users instead of random weights.
"""

import os
import sys
import json
import glob

# Add citrus package to path
sys.path.insert(0, '/home/runner/work/citrus/citrus')

from citrus.core.layers import LSTMCell, DenseLayer, EmbeddingLayer
from citrus.core.model import LanguageModel
from citrus.core.optimizer import SGDOptimizer, AdamOptimizer
from citrus.data.preprocessing import TextPreprocessor
from citrus.data.loader import DataLoader
from citrus.models.trainer import Trainer

def load_training_corpus():
    """Load all training data from the corpus directory"""
    corpus_dir = '/home/runner/work/citrus/citrus/data/training_corpus'
    all_text = []
    
    for filename in glob.glob(os.path.join(corpus_dir, '*.txt')):
        print(f"Loading {filename}...")
        with open(filename, 'r', encoding='utf-8') as f:
            all_text.append(f.read())
    
    combined_text = '\n\n'.join(all_text)
    print(f"\nTotal text loaded: {len(combined_text):,} characters")
    return combined_text

def main():
    print("=" * 70)
    print("CITRUS AI - MODEL PRE-TRAINING")
    print("=" * 70)
    print()
    
    # Load training data
    print("Step 1: Loading training corpus...")
    text = load_training_corpus()
    
    # Create preprocessor
    print("\nStep 2: Creating preprocessor...")
    preprocessor = TextPreprocessor(mode='char', max_vocab_size=None)
    preprocessor.fit(text)
    print(f"Vocabulary size: {len(preprocessor.vocab)}")
    print(f"Sample characters: {list(preprocessor.vocab)[:20]}")
    
    # Create data loader
    print("\nStep 3: Creating data loader...")
    loader = DataLoader(preprocessor)
    sequences = loader.create_training_sequences(text, seq_length=50)
    print(f"Generated {len(sequences):,} training sequences")
    
    # Build model
    print("\nStep 4: Building model...")
    vocab_size = len(preprocessor.vocab)
    hidden_size = 256  # Larger model for better quality
    
    model = LanguageModel(
        vocab_size=vocab_size,
        embedding_dim=128,
        hidden_size=hidden_size,
        num_layers=2
    )
    print(f"Model created with {hidden_size} hidden units")
    
    # Create optimizer
    optimizer = AdamOptimizer(learning_rate=0.001)
    
    # Create trainer
    trainer = Trainer(
        model=model,
        optimizer=optimizer,
        preprocessor=preprocessor
    )
    
    # Train model
    print("\nStep 5: Training model...")
    print("This will take several minutes. Training on good data creates smart AI!")
    print("-" * 70)
    
    trainer.train(
        sequences=sequences,
        epochs=200,  # Substantial training
        batch_size=32,
        checkpoint_dir='/home/runner/work/citrus/citrus/checkpoints',
        checkpoint_every=50
    )
    
    print("\n" + "=" * 70)
    print("TRAINING COMPLETE!")
    print("=" * 70)
    
    # Save final model
    final_checkpoint = '/home/runner/work/citrus/citrus/checkpoints/pretrained_model.pkl'
    trainer.save_checkpoint(final_checkpoint)
    print(f"\nPre-trained model saved to: {final_checkpoint}")
    
    # Test generation
    print("\n" + "=" * 70)
    print("TESTING MODEL - Sample Generated Text:")
    print("=" * 70)
    
    prompts = [
        "The sun",
        "She walked",
        "In the morning",
        "The most important"
    ]
    
    for prompt in prompts:
        generated = model.generate(
            preprocessor.encode(prompt),
            length=100,
            temperature=0.8,
            preprocessor=preprocessor
        )
        print(f"\nPrompt: '{prompt}'")
        print(f"Generated: {generated}")
        print("-" * 70)
    
    print("\n✅ Pre-training complete! The AI is now smart and ready to use.")
    print("This pre-trained model will be embedded in index.html so users")
    print("start with an AI that actually works instead of random gibberish!")

if __name__ == '__main__':
    main()
