#!/usr/bin/env python3
"""
Citrus AI Web Interface
A simple Flask web server for training and generating text through a web browser.
"""

import os
import sys
import json
import time
import threading
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename

# Add current directory to path to import citrus package
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from citrus.data.loader import DataLoader
from citrus.core.model import LanguageModel
from citrus.models.trainer import Trainer
from citrus.models.generator import TextGenerator

app = Flask(__name__, 
            template_folder='web/templates',
            static_folder='web/static')

# Configuration
UPLOAD_FOLDER = 'data/raw'
CHECKPOINT_FOLDER = 'checkpoints'
ALLOWED_EXTENSIONS = {'txt'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CHECKPOINT_FOLDER, exist_ok=True)

# Global training state
training_status = {
    'is_training': False,
    'progress': 0,
    'current_epoch': 0,
    'total_epochs': 0,
    'loss': 0.0,
    'message': 'Ready to train',
    'checkpoint_path': None
}


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Main landing page."""
    return render_template('index.html')


@app.route('/upload')
def upload_page():
    """Upload page for training data."""
    return render_template('upload.html')


@app.route('/train')
def train_page():
    """Training interface page."""
    return render_template('train.html')


@app.route('/generate')
def generate_page():
    """Text generation interface page."""
    return render_template('generate.html')


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle file upload."""
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'success': False, 'error': 'Only .txt files are allowed'}), 400
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    try:
        file.save(filepath)
        file_size = os.path.getsize(filepath)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'size': file_size,
            'message': f'File uploaded successfully: {filename} ({file_size} bytes)'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/files', methods=['GET'])
def list_files():
    """List all uploaded training files."""
    try:
        files = []
        if os.path.exists(UPLOAD_FOLDER):
            for filename in os.listdir(UPLOAD_FOLDER):
                if filename.endswith('.txt'):
                    filepath = os.path.join(UPLOAD_FOLDER, filename)
                    files.append({
                        'name': filename,
                        'size': os.path.getsize(filepath)
                    })
        
        return jsonify({'success': True, 'files': files})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/files/<filename>', methods=['DELETE'])
def delete_file(filename):
    """Delete a training file."""
    try:
        filepath = os.path.join(UPLOAD_FOLDER, secure_filename(filename))
        if os.path.exists(filepath):
            os.remove(filepath)
            return jsonify({'success': True, 'message': f'Deleted {filename}'})
        else:
            return jsonify({'success': False, 'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/checkpoints', methods=['GET'])
def list_checkpoints():
    """List all available model checkpoints."""
    try:
        checkpoints = []
        if os.path.exists(CHECKPOINT_FOLDER):
            for filename in os.listdir(CHECKPOINT_FOLDER):
                if filename.endswith('.pkl'):
                    filepath = os.path.join(CHECKPOINT_FOLDER, filename)
                    checkpoints.append({
                        'name': filename,
                        'size': os.path.getsize(filepath),
                        'modified': os.path.getmtime(filepath)
                    })
            # Sort by modification time, newest first
            checkpoints.sort(key=lambda x: x['modified'], reverse=True)
        
        return jsonify({'success': True, 'checkpoints': checkpoints})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


def train_model_thread(epochs, batch_size, seq_length, hidden_size):
    """Training function to run in a separate thread."""
    global training_status
    
    try:
        training_status['is_training'] = True
        training_status['message'] = 'Loading training data...'
        training_status['progress'] = 5
        
        # Load data
        data_loader = DataLoader(
            data_dir=UPLOAD_FOLDER,
            seq_length=seq_length,
            level='char'
        )
        
        data_loader.load_text_files()
        
        if not data_loader.texts:
            training_status['message'] = 'Error: No training files found'
            training_status['is_training'] = False
            return
        
        training_status['message'] = 'Preparing training data...'
        training_status['progress'] = 10
        
        sequences, targets = data_loader.prepare_training_data()
        vocab_size = data_loader.get_vocab_size()
        
        training_status['message'] = 'Creating model...'
        training_status['progress'] = 15
        
        # Create model
        model = LanguageModel(
            vocab_size=vocab_size,
            embedding_dim=min(128, hidden_size),
            hidden_size=hidden_size
        )
        
        training_status['message'] = 'Starting training...'
        training_status['total_epochs'] = epochs
        
        # Create custom trainer that updates status
        trainer = Trainer(model, learning_rate=0.001)
        
        # Train with progress updates
        num_samples = len(sequences)
        for epoch in range(epochs):
            training_status['current_epoch'] = epoch + 1
            training_status['message'] = f'Training epoch {epoch + 1}/{epochs}...'
            training_status['progress'] = 15 + int((epoch / epochs) * 70)
            
            # Train one epoch on a subset for demo purposes
            train_size = min(200, num_samples)
            epoch_loss = 0.0
            
            for i in range(train_size):
                loss = trainer.train_step(sequences[i], targets[i])
                epoch_loss += loss
                
                if i % 20 == 0:
                    avg_loss = epoch_loss / (i + 1)
                    training_status['loss'] = avg_loss
            
            # Save checkpoint every few epochs
            if (epoch + 1) % max(1, epochs // 3) == 0 or epoch == epochs - 1:
                training_status['message'] = f'Saving checkpoint...'
                trainer.save_checkpoint(CHECKPOINT_FOLDER, epoch + 1, data_loader.preprocessor)
        
        # Final save
        checkpoint_path = os.path.join(CHECKPOINT_FOLDER, f'checkpoint_epoch_{epochs}.pkl')
        training_status['checkpoint_path'] = checkpoint_path
        training_status['message'] = 'Training complete!'
        training_status['progress'] = 100
        
    except Exception as e:
        training_status['message'] = f'Error: {str(e)}'
        training_status['progress'] = 0
    finally:
        training_status['is_training'] = False


@app.route('/api/train', methods=['POST'])
def start_training():
    """Start model training."""
    global training_status
    
    if training_status['is_training']:
        return jsonify({
            'success': False,
            'error': 'Training is already in progress'
        }), 400
    
    try:
        data = request.get_json()
        epochs = int(data.get('epochs', 5))
        batch_size = int(data.get('batch_size', 16))
        seq_length = int(data.get('seq_length', 50))
        hidden_size = int(data.get('hidden_size', 128))
        
        # Validate parameters
        if epochs < 1 or epochs > 100:
            return jsonify({'success': False, 'error': 'Epochs must be between 1 and 100'}), 400
        
        # Reset status
        training_status['progress'] = 0
        training_status['current_epoch'] = 0
        training_status['loss'] = 0.0
        training_status['checkpoint_path'] = None
        
        # Start training in background thread
        thread = threading.Thread(
            target=train_model_thread,
            args=(epochs, batch_size, seq_length, hidden_size)
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'message': 'Training started'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/train/status', methods=['GET'])
def get_training_status():
    """Get current training status."""
    return jsonify({
        'success': True,
        'status': training_status
    })


@app.route('/api/generate', methods=['POST'])
def generate_text():
    """Generate text using a trained model."""
    try:
        data = request.get_json()
        checkpoint_name = data.get('checkpoint')
        prompt = data.get('prompt', 'The')
        length = int(data.get('length', 200))
        temperature = float(data.get('temperature', 0.8))
        
        if not checkpoint_name:
            return jsonify({'success': False, 'error': 'No checkpoint specified'}), 400
        
        checkpoint_path = os.path.join(CHECKPOINT_FOLDER, checkpoint_name)
        
        if not os.path.exists(checkpoint_path):
            return jsonify({'success': False, 'error': 'Checkpoint not found'}), 404
        
        # Load model and preprocessor
        model, preprocessor = Trainer.load_checkpoint(checkpoint_path, load_preprocessor=True)
        
        if preprocessor is None:
            return jsonify({
                'success': False,
                'error': 'Preprocessor not found in checkpoint. Please retrain the model.'
            }), 400
        
        # Generate text
        generator = TextGenerator(model, preprocessor)
        generated_text = generator.generate(
            seed_text=prompt,
            length=length,
            temperature=temperature,
            top_k=5
        )
        
        return jsonify({
            'success': True,
            'text': generated_text,
            'prompt': prompt,
            'length': len(generated_text)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    print("=" * 70)
    print("  🍊 Citrus AI Web Interface 🍊")
    print("=" * 70)
    print("\nStarting web server...")
    print("\n👉 Open your browser and go to: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
