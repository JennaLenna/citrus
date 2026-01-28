#!/usr/bin/env python3
"""
Advanced example showing all features of Citrus AI.
Demonstrates training, generation, and different configurations.
"""

import os
import sys

# Add parent directory to path to import citrus package
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from citrus.data.loader import DataLoader
from citrus.core.model import LanguageModel
from citrus.models.trainer import Trainer
from citrus.models.generator import TextGenerator


def train_model(data_dir, epochs, hidden_size, level):
    """Train a model with specified parameters."""
    
    print(f"\n{'='*60}")
    print(f"Training Configuration:")
    print(f"  Data directory: {data_dir}")
    print(f"  Epochs: {epochs}")
    print(f"  Hidden size: {hidden_size}")
    print(f"  Level: {level}")
    print(f"{'='*60}\n")
    
    # Load data
    print("Loading data...")
    loader = DataLoader(data_dir=data_dir, seq_length=50, level=level)
    loader.load_text_files()
    
    if not loader.texts:
        print(f"No data found in {data_dir}")
        return None, None
    
    # Prepare training data
    print("Preparing sequences...")
    sequences, targets = loader.prepare_training_data()
    vocab_size = loader.get_vocab_size()
    
    print(f"  Vocabulary: {vocab_size} tokens")
    print(f"  Training samples: {len(sequences)}")
    
    # Create model
    print("\nCreating model...")
    model = LanguageModel(
        vocab_size=vocab_size,
        embedding_dim=64 if hidden_size <= 128 else 128,
        hidden_size=hidden_size
    )
    
    # Train
    print("\nTraining...")
    trainer = Trainer(model, learning_rate=0.001)
    
    # Use subset for demo
    train_size = min(200, len(sequences))
    trainer.train(
        sequences=sequences[:train_size],
        targets=targets[:train_size],
        epochs=epochs,
        batch_size=16
    )
    
    return model, loader.preprocessor


def generate_samples(model, preprocessor, prompts, **kwargs):
    """Generate text samples with different prompts."""
    
    print(f"\n{'='*60}")
    print("Generating Text Samples")
    print(f"{'='*60}\n")
    
    generator = TextGenerator(model, preprocessor)
    
    for i, prompt in enumerate(prompts, 1):
        print(f"{i}. Prompt: '{prompt}'")
        print(f"   Settings: temperature={kwargs.get('temperature', 0.8)}, "
              f"top_k={kwargs.get('top_k', 5)}")
        
        generated = generator.generate(
            seed_text=prompt,
            length=kwargs.get('length', 100),
            temperature=kwargs.get('temperature', 0.8),
            top_k=kwargs.get('top_k', 5)
        )
        
        print(f"\n   Generated:\n   {generated[:200]}\n")
        print(f"   {'-'*56}\n")


def compare_temperatures(model, preprocessor, prompt):
    """Compare generation with different temperatures."""
    
    print(f"\n{'='*60}")
    print("Temperature Comparison")
    print(f"{'='*60}\n")
    
    generator = TextGenerator(model, preprocessor)
    temperatures = [0.3, 0.7, 1.2]
    
    for temp in temperatures:
        print(f"Temperature: {temp}")
        generated = generator.generate(
            seed_text=prompt,
            length=80,
            temperature=temp,
            top_k=5
        )
        print(f"  {generated[:150]}...")
        print()


def main():
    """Run advanced examples."""
    
    print("="*60)
    print("Citrus AI - Advanced Examples")
    print("="*60)
    
    data_dir = 'data/raw'
    
    # Ensure data exists
    if not os.path.exists(data_dir) or not os.listdir(data_dir):
        print(f"\nError: No data found in {data_dir}")
        print("Please add .txt files with training data.")
        return
    
    # Example 1: Train character-level model
    print("\n### Example 1: Character-Level Model ###")
    model_char, preprocessor_char = train_model(
        data_dir=data_dir,
        epochs=3,
        hidden_size=128,
        level='char'
    )
    
    if model_char:
        generate_samples(
            model_char, 
            preprocessor_char,
            prompts=["The", "It was", "In the"],
            length=100,
            temperature=0.8,
            top_k=5
        )
        
        compare_temperatures(model_char, preprocessor_char, "The")
    
    # Example 2: Train word-level model
    print("\n### Example 2: Word-Level Model ###")
    model_word, preprocessor_word = train_model(
        data_dir=data_dir,
        epochs=3,
        hidden_size=64,
        level='word'
    )
    
    if model_word:
        generate_samples(
            model_word,
            preprocessor_word,
            prompts=["The quick", "Once upon"],
            length=50,
            temperature=0.7,
            top_k=3
        )
    
    # Example 3: Different generation strategies
    if model_char:
        print("\n### Example 3: Generation Strategies ###")
        
        generator = TextGenerator(model_char, preprocessor_char)
        prompt = "It was"
        
        strategies = [
            ("Conservative", {"temperature": 0.3, "top_k": 2}),
            ("Balanced", {"temperature": 0.8, "top_k": 5}),
            ("Creative", {"temperature": 1.3, "top_k": 10})
        ]
        
        print(f"\nPrompt: '{prompt}'\n")
        
        for name, params in strategies:
            print(f"{name} (temp={params['temperature']}, top_k={params['top_k']}):")
            text = generator.generate(
                seed_text=prompt,
                length=100,
                **params
            )
            print(f"  {text[:150]}...")
            print()
    
    print("="*60)
    print("Advanced examples completed!")
    print("="*60)
    print("\nKey Takeaways:")
    print("  - Character-level: Better for style, punctuation")
    print("  - Word-level: Better for meaning, faster")
    print("  - Temperature: Controls randomness")
    print("  - Top-k: Controls diversity")
    print("  - More epochs = better learning")
    print("  - Larger hidden size = more capacity")


if __name__ == '__main__':
    main()
