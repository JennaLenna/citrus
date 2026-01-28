#!/usr/bin/env python3
"""
CLI for generating text using the trained Citrus AI model.
"""

import argparse
import os
import sys
import pickle

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from citrus.models.trainer import Trainer
from citrus.models.generator import TextGenerator
from citrus.data.preprocessing import TextPreprocessor


def main():
    parser = argparse.ArgumentParser(
        description='Generate text using the trained Citrus AI model'
    )
    
    parser.add_argument(
        '--checkpoint',
        type=str,
        required=True,
        help='Path to model checkpoint file'
    )
    
    parser.add_argument(
        '--prompt',
        type=str,
        default='',
        help='Prompt or seed text for generation'
    )
    
    parser.add_argument(
        '--length',
        type=int,
        default=200,
        help='Length of text to generate'
    )
    
    parser.add_argument(
        '--temperature',
        type=float,
        default=0.8,
        help='Sampling temperature (higher = more random)'
    )
    
    parser.add_argument(
        '--top-k',
        type=int,
        default=5,
        help='Top-k sampling parameter'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        help='Output file path (optional)'
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Citrus AI Writing Style Model - Text Generation")
    print("=" * 60)
    
    # Load model
    print(f"\n1. Loading model from {args.checkpoint}...")
    
    if not os.path.exists(args.checkpoint):
        print(f"Error: Checkpoint file not found: {args.checkpoint}")
        return 1
    
    model = Trainer.load_checkpoint(args.checkpoint)
    
    # Load preprocessor info from checkpoint
    with open(args.checkpoint, 'rb') as f:
        checkpoint = pickle.load(f)
    
    # We need to reconstruct the preprocessor
    # For now, we'll create a simple one with the vocab from checkpoint
    print("\n2. Setting up text generator...")
    
    # Create a basic preprocessor (in production, this would be saved with the model)
    preprocessor = TextPreprocessor(level='char')
    
    # Try to reconstruct vocabulary if possible
    # This is a limitation - in production, save preprocessor with model
    print("   Note: Using basic preprocessor. For best results, ensure vocabulary matches training.")
    
    generator = TextGenerator(model, preprocessor)
    
    # Generate text
    print("\n3. Generating text...")
    print(f"   Prompt: '{args.prompt}'")
    print(f"   Length: {args.length} tokens")
    print(f"   Temperature: {args.temperature}")
    print(f"   Top-k: {args.top_k}")
    
    generated_text = generator.generate(
        seed_text=args.prompt,
        length=args.length,
        temperature=args.temperature,
        top_k=args.top_k
    )
    
    # Output results
    print("\n" + "=" * 60)
    print("Generated Text:")
    print("=" * 60)
    print(generated_text)
    print("=" * 60)
    
    # Save to file if requested
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(generated_text)
        print(f"\nText saved to: {args.output}")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
