#!/usr/bin/env python3
"""
CLI for generating text using the trained Citrus AI model.
"""

import argparse
import os
import sys
import pickle

# Add current directory to path to import citrus package
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

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
        help='Sampling temperature (0.1-2.0, higher = more random)'
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
    
    model, preprocessor = Trainer.load_checkpoint(args.checkpoint, load_preprocessor=True)
    
    # Check if preprocessor was saved with checkpoint
    if preprocessor is None:
        print("\n   Warning: Preprocessor not found in checkpoint.")
        print("   This checkpoint was created with an older version.")
        print("   Generated text may not be accurate.")
        print("   Please retrain the model to include preprocessor.")
        # Create a basic preprocessor as fallback
        preprocessor = TextPreprocessor(level='char')
        # Try to build a minimal vocab (will be incomplete)
        preprocessor.vocab_size = model.vocab_size
    
    # Set up text generator
    print("\n2. Setting up text generator...")
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
