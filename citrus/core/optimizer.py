"""
Optimizer implementations from scratch.
"""

import numpy as np
from typing import Dict


class Optimizer:
    """Base optimizer class."""
    
    def __init__(self, learning_rate: float = 0.001):
        """
        Initialize optimizer.
        
        Args:
            learning_rate: Learning rate
        """
        self.learning_rate = learning_rate
    
    def update(self, params: dict, gradients: dict) -> None:
        """Update parameters using gradients."""
        raise NotImplementedError


class SGD(Optimizer):
    """Stochastic Gradient Descent optimizer."""
    
    def update(self, params: dict, gradients: dict) -> None:
        """
        Update parameters using SGD.
        
        Args:
            params: Model parameters
            gradients: Parameter gradients
        """
        for key in params:
            if isinstance(params[key], dict):
                self.update(params[key], gradients[key])
            elif isinstance(params[key], np.ndarray):
                params[key] -= self.learning_rate * gradients[key]


class Adam(Optimizer):
    """Adam optimizer with momentum and adaptive learning rates."""
    
    def __init__(self, learning_rate: float = 0.001, beta1: float = 0.9, 
                 beta2: float = 0.999, epsilon: float = 1e-8):
        """
        Initialize Adam optimizer.
        
        Args:
            learning_rate: Learning rate
            beta1: Exponential decay rate for first moment
            beta2: Exponential decay rate for second moment
            epsilon: Small constant for numerical stability
        """
        super().__init__(learning_rate)
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon = epsilon
        self.m = {}  # First moment
        self.v = {}  # Second moment
        self.t = 0   # Time step
    
    def _init_moments(self, params: dict, prefix: str = '') -> None:
        """Initialize moment estimates."""
        for key, value in params.items():
            full_key = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict):
                self._init_moments(value, full_key)
            elif isinstance(value, np.ndarray):
                if full_key not in self.m:
                    self.m[full_key] = np.zeros_like(value)
                    self.v[full_key] = np.zeros_like(value)
    
    def _update_recursive(self, params: dict, gradients: dict, prefix: str = '') -> None:
        """Recursively update parameters."""
        for key in params:
            full_key = f"{prefix}.{key}" if prefix else key
            if isinstance(params[key], dict):
                self._update_recursive(params[key], gradients[key], full_key)
            elif isinstance(params[key], np.ndarray):
                # Update biased first moment estimate
                self.m[full_key] = self.beta1 * self.m[full_key] + (1 - self.beta1) * gradients[key]
                
                # Update biased second moment estimate
                self.v[full_key] = self.beta2 * self.v[full_key] + (1 - self.beta2) * (gradients[key] ** 2)
                
                # Compute bias-corrected first moment estimate
                m_hat = self.m[full_key] / (1 - self.beta1 ** self.t)
                
                # Compute bias-corrected second moment estimate
                v_hat = self.v[full_key] / (1 - self.beta2 ** self.t)
                
                # Update parameters
                params[key] -= self.learning_rate * m_hat / (np.sqrt(v_hat) + self.epsilon)
    
    def update(self, params: dict, gradients: dict) -> None:
        """
        Update parameters using Adam.
        
        Args:
            params: Model parameters
            gradients: Parameter gradients
        """
        self.t += 1
        self._init_moments(params)
        self._update_recursive(params, gradients)


def clip_gradients(gradients: dict, max_norm: float = 5.0) -> dict:
    """
    Clip gradients by global norm.
    
    Args:
        gradients: Gradient dictionary
        max_norm: Maximum norm
        
    Returns:
        Clipped gradients
    """
    def get_total_norm(grads: dict) -> float:
        """Calculate total gradient norm."""
        total_norm = 0.0
        for key, value in grads.items():
            if isinstance(value, dict):
                total_norm += get_total_norm(value)
            elif isinstance(value, np.ndarray):
                total_norm += np.sum(value ** 2)
        return np.sqrt(total_norm)
    
    def clip_recursive(grads: dict, clip_factor: float) -> dict:
        """Recursively clip gradients."""
        clipped = {}
        for key, value in grads.items():
            if isinstance(value, dict):
                clipped[key] = clip_recursive(value, clip_factor)
            elif isinstance(value, np.ndarray):
                clipped[key] = value * clip_factor
        return clipped
    
    total_norm = get_total_norm(gradients)
    
    if total_norm > max_norm:
        clip_factor = max_norm / (total_norm + 1e-6)
        return clip_recursive(gradients, clip_factor)
    
    return gradients
