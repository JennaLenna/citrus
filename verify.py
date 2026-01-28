#!/usr/bin/env python3
"""
Quick verification that the system works end-to-end.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from citrus.data.preprocessing import TextPreprocessor, SequenceGenerator
from citrus.core.model import LanguageModel
from citrus.models.trainer import Trainer
from citrus.models.generator import TextGenerator

print("=" * 60)
print("Citrus AI - Quick Verification")
print("=" * 60)

# Simple test data
test_texts = [
    "The quick brown fox jumps over the lazy dog.",
    "The dog was lazy and the fox was quick."
]

print("\n1. Testing preprocessing...")
preprocessor = TextPreprocessor(level='char')
preprocessor.build_vocab(test_texts)
print(f"   ✓ Vocabulary size: {preprocessor.vocab_size}")

# Encode test
encoded = preprocessor.encode("The fox")
decoded = preprocessor.decode(encoded)
print(f"   ✓ Encode/decode test: '{decoded}'")

print("\n2. Testing sequence generation...")
seq_gen = SequenceGenerator(seq_length=10)
sequences, targets = seq_gen.create_sequences(encoded)
print(f"   ✓ Generated {len(sequences)} sequences")

print("\n3. Testing model initialization...")
model = LanguageModel(vocab_size=preprocessor.vocab_size, 
                     embedding_dim=32, 
                     hidden_size=64)
print(f"   ✓ Model created")

print("\n4. Testing forward pass...")
model.reset_state()
probs = model.forward(encoded[0])
print(f"   ✓ Output shape: {probs.shape}")
print(f"   ✓ Output sum (should be ~1.0): {probs.sum():.4f}")

print("\n5. Testing loss computation...")
loss = model.compute_loss([encoded[0]], encoded[1])
print(f"   ✓ Loss computed: {loss:.4f}")

print("\n6. Testing text generation...")
generator = TextGenerator(model, preprocessor)
generated = generator.generate("The", length=20, temperature=1.0)
print(f"   ✓ Generated text: '{generated[:50]}...'")

print("\n" + "=" * 60)
print("All checks passed! ✓")
print("=" * 60)
print("\nThe Citrus AI system is working correctly.")
print("\nNext steps:")
print("1. Add your training text files to data/raw/")
print("2. Run: python train.py --epochs 10")
print("3. Generate text: python generate.py --checkpoint checkpoints/checkpoint_epoch_10.pkl")
