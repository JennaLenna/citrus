"""
Text generation using the trained model.
"""

import numpy as np
from typing import List, Optional
from ..core.model import LanguageModel
from ..data.preprocessing import TextPreprocessor


class TextGenerator:
    """Generates text in a learned style."""
    
    def __init__(self, model: LanguageModel, preprocessor: TextPreprocessor):
        """
        Initialize generator.
        
        Args:
            model: Trained language model
            preprocessor: Text preprocessor with vocabulary
        """
        self.model = model
        self.preprocessor = preprocessor
    
    def sample(self, probs: np.ndarray, temperature: float = 1.0, top_k: int = 0) -> int:
        """
        Sample from probability distribution.
        
        Args:
            probs: Probability distribution
            temperature: Sampling temperature (higher = more random). Range: 0.1 to 2.0
            top_k: If > 0, sample from top k tokens only
            
        Returns:
            Sampled token index
        """
        probs = probs.flatten()
        
        # Validate and clip temperature
        temperature = max(0.1, min(2.0, temperature))
        
        # Apply temperature
        if temperature != 1.0:
            probs = np.power(probs, 1.0 / temperature)
            probs = probs / np.sum(probs)
        
        # Top-k sampling
        if top_k > 0:
            top_indices = np.argsort(probs)[-top_k:]
            top_probs = probs[top_indices]
            top_probs = top_probs / np.sum(top_probs)
            
            sampled_idx = np.random.choice(top_indices, p=top_probs)
        else:
            sampled_idx = np.random.choice(len(probs), p=probs)
        
        return sampled_idx
    
    def generate(self, seed_text: str, length: int = 200, 
                 temperature: float = 0.8, top_k: int = 5) -> str:
        """
        Generate text starting from seed text.
        
        Args:
            seed_text: Starting text
            length: Number of tokens to generate
            temperature: Sampling temperature
            top_k: Top-k sampling parameter
            
        Returns:
            Generated text
        """
        # Encode seed text
        seed_text = self.preprocessor.clean_text(seed_text)
        encoded_seed = self.preprocessor.encode(seed_text)
        
        if len(encoded_seed) == 0:
            # Start with a random token if seed is empty
            encoded_seed = [np.random.randint(0, self.preprocessor.vocab_size)]
        
        # Initialize with seed
        generated = encoded_seed.copy()
        self.model.reset_state()
        
        # Process seed text to set up model state
        for token_idx in encoded_seed:
            self.model.forward(token_idx)
        
        # Generate new tokens
        for _ in range(length):
            # Get next token probabilities
            probs = self.model.forward(generated[-1])
            
            # Sample next token
            next_token = self.sample(probs, temperature, top_k)
            
            # Add to generated sequence
            generated.append(next_token)
        
        # Decode to text
        generated_text = self.preprocessor.decode(generated)
        
        return generated_text
    
    def generate_with_prompt(self, prompt: str, max_length: int = 500,
                            temperature: float = 0.8, top_k: int = 5) -> str:
        """
        Generate text based on a prompt.
        
        Args:
            prompt: User prompt describing what to write
            max_length: Maximum length of generated text
            temperature: Sampling temperature
            top_k: Top-k sampling parameter
            
        Returns:
            Generated text
        """
        # For now, use the prompt as seed text
        # In a more advanced version, we could condition on the prompt differently
        return self.generate(
            seed_text=prompt,
            length=max_length,
            temperature=temperature,
            top_k=top_k
        )
