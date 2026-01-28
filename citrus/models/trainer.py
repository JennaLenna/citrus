"""
Training loop for the language model.
"""

import os
import pickle
import numpy as np
from typing import List, Optional
from ..core.model import LanguageModel
from ..core.optimizer import Adam, clip_gradients


class Trainer:
    """Trains the language model on text data."""
    
    def __init__(self, model: LanguageModel, learning_rate: float = 0.001):
        """
        Initialize trainer.
        
        Args:
            model: Language model to train
            learning_rate: Learning rate for optimization
        """
        self.model = model
        self.optimizer = Adam(learning_rate=learning_rate)
        self.train_losses: List[float] = []
    
    def compute_gradients(self, sequence: List[int], target: int) -> dict:
        """
        Compute gradients using finite differences (simple but slow).
        For a full implementation, backpropagation through time would be used.
        
        Args:
            sequence: Input sequence
            target: Target token
            
        Returns:
            Gradients dictionary
        """
        epsilon = 1e-4
        gradients = {}
        
        # Get all parameters
        params = self.model.get_all_params()
        
        # Compute base loss
        base_loss = self.model.compute_loss(sequence, target)
        
        # Compute gradients for each parameter using finite differences
        def compute_param_gradients(param_dict: dict) -> dict:
            grads = {}
            for key, value in param_dict.items():
                if isinstance(value, dict):
                    grads[key] = compute_param_gradients(value)
                elif isinstance(value, np.ndarray):
                    grad = np.zeros_like(value)
                    
                    # For large matrices, sample random subset
                    if value.size > 1000:
                        # Sample only 100 parameters for efficiency
                        indices = np.random.choice(value.size, min(100, value.size), replace=False)
                        for idx in indices:
                            idx_tuple = np.unravel_index(idx, value.shape)
                            
                            # Perturb parameter
                            original = value[idx_tuple]
                            value[idx_tuple] = original + epsilon
                            
                            # Compute perturbed loss
                            self.model.set_params(params)
                            perturbed_loss = self.model.compute_loss(sequence, target)
                            
                            # Gradient approximation
                            grad[idx_tuple] = (perturbed_loss - base_loss) / epsilon
                            
                            # Restore original value
                            value[idx_tuple] = original
                    else:
                        # For small matrices, compute all gradients
                        it = np.nditer(value, flags=['multi_index'])
                        for _ in it:
                            idx = it.multi_index
                            
                            # Perturb parameter
                            original = value[idx]
                            value[idx] = original + epsilon
                            
                            # Compute perturbed loss
                            self.model.set_params(params)
                            perturbed_loss = self.model.compute_loss(sequence, target)
                            
                            # Gradient approximation
                            grad[idx] = (perturbed_loss - base_loss) / epsilon
                            
                            # Restore original value
                            value[idx] = original
                    
                    grads[key] = grad
            
            return grads
        
        gradients = compute_param_gradients(params)
        
        # Restore original parameters
        self.model.set_params(params)
        
        return gradients
    
    def train_step(self, sequence: List[int], target: int) -> float:
        """
        Perform one training step.
        
        Args:
            sequence: Input sequence
            target: Target token
            
        Returns:
            Loss value
        """
        # Compute loss
        loss = self.model.compute_loss(sequence, target)
        
        # Compute gradients (simplified - in production would use BPTT)
        gradients = self.compute_gradients(sequence, target)
        
        # Clip gradients
        gradients = clip_gradients(gradients, max_norm=5.0)
        
        # Update parameters
        params = self.model.get_all_params()
        self.optimizer.update(params, gradients)
        self.model.set_params(params)
        
        return loss
    
    def train(self, sequences: List[List[int]], targets: List[int], 
              epochs: int = 10, batch_size: int = 32, 
              checkpoint_dir: Optional[str] = None,
              preprocessor=None) -> None:
        """
        Train the model.
        
        Args:
            sequences: List of input sequences
            targets: List of target tokens
            epochs: Number of training epochs
            batch_size: Number of samples per batch
            checkpoint_dir: Directory to save checkpoints
            preprocessor: TextPreprocessor instance to save with checkpoints
        """
        num_samples = len(sequences)
        
        print(f"Starting training with {num_samples} samples for {epochs} epochs...")
        
        for epoch in range(epochs):
            epoch_loss = 0.0
            num_batches = 0
            
            # Shuffle data
            indices = np.random.permutation(num_samples)
            
            for i in range(0, num_samples, batch_size):
                batch_indices = indices[i:i + batch_size]
                batch_loss = 0.0
                
                for idx in batch_indices:
                    loss = self.train_step(sequences[idx], targets[idx])
                    batch_loss += loss
                
                batch_loss /= len(batch_indices)
                epoch_loss += batch_loss
                num_batches += 1
                
                if num_batches % 10 == 0:
                    print(f"  Epoch {epoch + 1}/{epochs}, Batch {num_batches}, Loss: {batch_loss:.4f}")
            
            avg_loss = epoch_loss / num_batches
            self.train_losses.append(avg_loss)
            
            print(f"Epoch {epoch + 1}/{epochs} completed. Average Loss: {avg_loss:.4f}")
            
            # Save checkpoint
            if checkpoint_dir and (epoch + 1) % 5 == 0:
                self.save_checkpoint(checkpoint_dir, epoch + 1, preprocessor)
    
    def save_checkpoint(self, checkpoint_dir: str, epoch: int, preprocessor=None) -> None:
        """
        Save training checkpoint.
        
        Args:
            checkpoint_dir: Directory to save checkpoint
            epoch: Current epoch number
            preprocessor: TextPreprocessor instance to save with model (optional but recommended)
        """
        os.makedirs(checkpoint_dir, exist_ok=True)
        
        checkpoint = {
            'model_params': self.model.get_all_params(),
            'epoch': epoch,
            'train_losses': self.train_losses,
            'vocab_size': self.model.vocab_size,
            'embedding_dim': self.model.embedding_dim,
            'hidden_size': self.model.hidden_size
        }
        
        # Save preprocessor if provided
        if preprocessor is not None:
            checkpoint['preprocessor'] = {
                'level': preprocessor.level,
                'vocab': preprocessor.vocab,
                'reverse_vocab': preprocessor.reverse_vocab,
                'vocab_size': preprocessor.vocab_size
            }
        
        checkpoint_path = os.path.join(checkpoint_dir, f'checkpoint_epoch_{epoch}.pkl')
        with open(checkpoint_path, 'wb') as f:
            pickle.dump(checkpoint, f)
        
        print(f"Checkpoint saved to {checkpoint_path}")
    
    @staticmethod
    def load_checkpoint(checkpoint_path: str, load_preprocessor: bool = True):
        """
        Load model from checkpoint.
        
        Args:
            checkpoint_path: Path to checkpoint file
            load_preprocessor: Whether to also load and return the preprocessor
            
        Returns:
            If load_preprocessor=False: LanguageModel
            If load_preprocessor=True: Tuple of (LanguageModel, TextPreprocessor or None)
        """
        from ..data.preprocessing import TextPreprocessor
        
        with open(checkpoint_path, 'rb') as f:
            checkpoint = pickle.load(f)
        
        model = LanguageModel(
            vocab_size=checkpoint['vocab_size'],
            embedding_dim=checkpoint['embedding_dim'],
            hidden_size=checkpoint['hidden_size']
        )
        
        model.set_params(checkpoint['model_params'])
        
        if not load_preprocessor:
            return model
        
        # Load preprocessor if available
        preprocessor = None
        if 'preprocessor' in checkpoint:
            prep_data = checkpoint['preprocessor']
            preprocessor = TextPreprocessor(level=prep_data['level'])
            preprocessor.vocab = prep_data['vocab']
            preprocessor.reverse_vocab = prep_data['reverse_vocab']
            preprocessor.vocab_size = prep_data['vocab_size']
        
        return model, preprocessor
