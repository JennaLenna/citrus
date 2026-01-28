#!/usr/bin/env python3
"""
Citrus AI - Super Simple Server
Just run this file and open citrus_simple.html in your browser!
"""

import os
import sys
import json
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Try to import dependencies, install if needed
try:
    import numpy as np
except ImportError:
    print("📦 Installing numpy... (one-time setup)")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy"])
    import numpy as np

from citrus.data.preprocessing import TextPreprocessor
from citrus.core.model import LanguageModel
from citrus.models.trainer import Trainer
from citrus.models.generator import TextGenerator

# Global state
stored_text = ""
model = None
preprocessor = None
training_status = {"training": False, "message": "Ready"}

class SimpleHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        """Handle GET requests"""
        parsed = urlparse(self.path)
        
        # Health check
        if parsed.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok"}).encode())
            return
        
        # Training status
        if parsed.path == '/status':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(training_status).encode())
            return
        
        self.send_error(404)
    
    def do_POST(self):
        """Handle POST requests"""
        global stored_text, model, preprocessor, training_status
        
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        parsed = urlparse(self.path)
        
        # Save text
        if parsed.path == '/save_text':
            stored_text = data.get('text', '')
            response = {"status": "ok", "size": len(stored_text)}
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            return
        
        # Start training
        if parsed.path == '/train':
            if not stored_text:
                self.send_error(400, "No text saved yet")
                return
            
            epochs = data.get('epochs', 5)
            
            # Start training in background
            def train():
                global model, preprocessor, training_status
                try:
                    training_status = {"training": True, "message": "Preparing data..."}
                    
                    # Prepare data
                    preprocessor = TextPreprocessor(level='char')
                    preprocessor.fit(stored_text)
                    
                    encoded = preprocessor.encode(stored_text)
                    vocab_size = preprocessor.get_vocab_size()
                    
                    # Create simple sequences
                    seq_length = 30
                    sequences = []
                    targets = []
                    for i in range(len(encoded) - seq_length):
                        sequences.append(encoded[i:i+seq_length])
                        targets.append(encoded[i+seq_length])
                    
                    training_status["message"] = f"Creating model..."
                    
                    # Create model
                    model = LanguageModel(
                        vocab_size=vocab_size,
                        embedding_dim=64,
                        hidden_size=64
                    )
                    
                    trainer = Trainer(model, learning_rate=0.01)
                    
                    # Train
                    for epoch in range(epochs):
                        training_status["message"] = f"Training: epoch {epoch+1}/{epochs}"
                        
                        # Train on subset for speed
                        train_size = min(100, len(sequences))
                        for i in range(train_size):
                            trainer.train_step(sequences[i], targets[i])
                    
                    training_status = {"training": False, "message": "Training complete!"}
                    
                except Exception as e:
                    training_status = {"training": False, "message": f"Error: {str(e)}"}
            
            thread = threading.Thread(target=train)
            thread.daemon = True
            thread.start()
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "training_started"}).encode())
            return
        
        # Generate text
        if parsed.path == '/generate':
            if model is None or preprocessor is None:
                self.send_error(400, "Model not trained yet")
                return
            
            prompt = data.get('prompt', 'The')
            length = data.get('length', 200)
            
            try:
                generator = TextGenerator(model, preprocessor)
                generated = generator.generate(
                    seed_text=prompt,
                    length=length,
                    temperature=0.8,
                    top_k=5
                )
                
                response = {"text": generated}
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())
                return
                
            except Exception as e:
                self.send_error(500, str(e))
                return
        
        self.send_error(404)
    
    def log_message(self, format, *args):
        """Suppress default logging"""
        pass

def run_server(port=5555):
    """Start the simple server"""
    server = HTTPServer(('localhost', port), SimpleHandler)
    print("=" * 70)
    print("  🍊 Citrus AI - Super Simple Server 🍊")
    print("=" * 70)
    print()
    print(f"✅ Server is running on http://localhost:{port}")
    print()
    print("📝 NEXT STEP:")
    print(f"   Open the file 'citrus_simple.html' in your web browser!")
    print()
    print("   Just double-click the file and it will open.")
    print()
    print("💡 TIP: Keep this window open while using the app")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 70)
    print()
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped. Goodbye!")
        server.shutdown()

if __name__ == '__main__':
    run_server()
