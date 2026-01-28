"""Utility functions for the Citrus system."""

import os
from typing import List


def create_directory_structure(base_dir: str) -> None:
    """
    Create necessary directory structure.
    
    Args:
        base_dir: Base directory path
    """
    directories = [
        os.path.join(base_dir, 'data', 'raw'),
        os.path.join(base_dir, 'data', 'processed'),
        os.path.join(base_dir, 'checkpoints'),
        os.path.join(base_dir, 'logs')
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)


def load_text_from_file(file_path: str) -> str:
    """
    Load text from a file.
    
    Args:
        file_path: Path to text file
        
    Returns:
        File contents as string
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def save_text_to_file(text: str, file_path: str) -> None:
    """
    Save text to a file.
    
    Args:
        text: Text to save
        file_path: Output file path
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(text)


def list_text_files(directory: str) -> List[str]:
    """
    List all text files in a directory.
    
    Args:
        directory: Directory path
        
    Returns:
        List of file paths
    """
    if not os.path.exists(directory):
        return []
    
    text_files = []
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            text_files.append(os.path.join(directory, filename))
    
    return text_files
