# Citrus 🍊

**A from-scratch AI writing style transfer system**

Citrus is a custom-built neural network that learns writing styles from text samples and generates new content in that style. Built entirely from scratch using only NumPy, without any pre-trained models or existing AI frameworks.

---

## 🌐 NEW: Web Interface! (No Coding Required!)

**The easiest way to use Citrus - through your web browser!**

```bash
./start_web.sh
# Then open: http://localhost:5000
```

**Perfect for non-coders!** Upload files, train, and generate - all through a nice web interface.

👉 **[See WEB_INTERFACE.md for the complete guide](WEB_INTERFACE.md)** 👈

---

## ⚡ TL;DR - Just Want to Use It? (Not Hard!)

**👉 [See HOW_TO_USE.md for the visual step-by-step guide](HOW_TO_USE.md) 👈**

**Option 1: Web Interface (Easiest!)**
```bash
./start_web.sh              # Start web server
# Open browser: http://localhost:5000
```

**Option 2: Interactive Command Line**
```bash
pip install -r requirements.txt    # Install (30 seconds)
python easy_start.py               # Interactive guided mode
```

**Option 3: Direct Commands**
```bash
pip install -r requirements.txt
python add_writing.py              # Add your writing samples
python train.py --epochs 10        # Train the AI (5 minutes)
python generate.py --checkpoint checkpoints/checkpoint_epoch_10.pkl --prompt "Your prompt here"
```

**📚 Documentation for different needs:**
- **[WEB_INTERFACE.md](WEB_INTERFACE.md)** - Use through web browser (NO CODING!)
- **[HOW_TO_USE.md](HOW_TO_USE.md)** - Visual guide, answers "Is it hard?" (NO!)
- **[QUICKSTART.md](QUICKSTART.md)** - Ultra-simple 3-step guide
- **[GETTING_STARTED.md](GETTING_STARTED.md)** - Detailed tutorial with tips
- **[DEVELOPMENT.md](DEVELOPMENT.md)** - Technical deep dive

---

## 🎯 What Citrus Does

Citrus learns to write like you (or any author you provide samples from):
1. **Upload writing samples** - Provide text files of the writing style you want to learn
2. **Train the model** - The neural network learns patterns, vocabulary, and style from your samples
3. **Generate new content** - Give it a prompt and it generates new text in the learned writing style

## 🏗️ Architecture

Citrus implements a complete LSTM-based language model from scratch:

- **Character/Word-level tokenization** - Process text at character or word level
- **Embedding layer** - Dense vector representations of tokens
- **LSTM cells** - Long Short-Term Memory units for sequence modeling
- **Softmax output** - Probability distribution over vocabulary
- **Adam optimizer** - Adaptive learning rate optimization
- **Gradient clipping** - Prevent exploding gradients

All components are implemented in pure Python + NumPy without using TensorFlow, PyTorch, or other ML frameworks.

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/JennaLenna/citrus.git
cd citrus

# Install dependencies
pip install -r requirements.txt
```

### Training a Model

1. **Prepare your training data:**
   ```bash
   # Add your text files to data/raw/
   cp your_writing_samples.txt data/raw/
   ```

2. **Train the model:**
   ```bash
   python train.py \
       --data-dir data/raw \
       --epochs 20 \
       --batch-size 32 \
       --hidden-size 256
   ```

3. **Monitor training progress:**
   - Training loss will be displayed for each epoch
   - Checkpoints are saved every 5 epochs to `checkpoints/`

### Generating Text

Once trained, generate new text in the learned style:

```bash
python generate.py \
    --checkpoint checkpoints/checkpoint_epoch_20.pkl \
    --prompt "It was a dark and stormy night" \
    --length 500 \
    --temperature 0.8
```

## 📖 Detailed Usage

### Training Options

```bash
python train.py --help

Options:
  --data-dir DIR          Directory with .txt training files (default: data/raw)
  --checkpoint-dir DIR    Where to save checkpoints (default: checkpoints)
  --seq-length N          Length of training sequences (default: 100)
  --embedding-dim N       Embedding vector size (default: 128)
  --hidden-size N         LSTM hidden state size (default: 256)
  --epochs N              Number of training epochs (default: 10)
  --batch-size N          Training batch size (default: 32)
  --learning-rate F       Learning rate (default: 0.001)
  --level {char,word}     Process at char or word level (default: char)
```

### Generation Options

```bash
python generate.py --help

Options:
  --checkpoint FILE       Path to trained model checkpoint
  --prompt TEXT           Starting text for generation
  --length N              Number of tokens to generate (default: 200)
  --temperature F         Sampling temperature 0.1-2.0 (default: 0.8)
                         Lower = more conservative, Higher = more creative
  --top-k N              Sample from top K tokens (default: 5)
  --output FILE          Save generated text to file (optional)
```

## 🧪 Examples

### Basic Example

Run the included example to see Citrus in action:

```bash
python examples/basic_example.py
```

This will:
- Load sample training data
- Train a small model
- Generate text samples with different prompts

### Training on Custom Data

```python
from citrus.data.loader import DataLoader
from citrus.core.model import LanguageModel
from citrus.models.trainer import Trainer

# Load your data
loader = DataLoader(data_dir='data/raw', seq_length=100, level='char')
loader.load_text_files()
sequences, targets = loader.prepare_training_data()

# Create and train model
model = LanguageModel(
    vocab_size=loader.get_vocab_size(),
    embedding_dim=128,
    hidden_size=256
)

trainer = Trainer(model, learning_rate=0.001)
trainer.train(sequences, targets, epochs=20, batch_size=32)
```

### Generating Text Programmatically

```python
from citrus.models.trainer import Trainer
from citrus.models.generator import TextGenerator

# Load trained model
model = Trainer.load_checkpoint('checkpoints/checkpoint_epoch_20.pkl')

# Create generator
generator = TextGenerator(model, preprocessor)

# Generate text
text = generator.generate(
    seed_text="Once upon a time",
    length=300,
    temperature=0.8,
    top_k=5
)

print(text)
```

## 🧬 How It Works

### Training Process

1. **Text Preprocessing**
   - Clean and normalize input text
   - Build vocabulary from all unique tokens
   - Create sequences of fixed length for training

2. **Model Initialization**
   - Initialize embedding matrix randomly
   - Initialize LSTM weights using Xavier initialization
   - Initialize output layer for vocabulary prediction

3. **Training Loop**
   - Feed sequences through embedding → LSTM → output layers
   - Compute cross-entropy loss against target tokens
   - Calculate gradients (using finite differences or BPTT)
   - Update weights using Adam optimizer
   - Save checkpoints periodically

4. **Generation Process**
   - Start with seed text or random token
   - Feed through trained network to get next token probabilities
   - Sample next token using temperature and top-k
   - Repeat until desired length is reached

### Key Components

- **`citrus/data/`** - Data loading and preprocessing
- **`citrus/core/`** - Neural network layers and model
- **`citrus/models/`** - Training and generation logic
- **`citrus/utils/`** - Helper utilities
- **`train.py`** - Training CLI
- **`generate.py`** - Generation CLI

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
python -m unittest discover tests

# Run specific test file
python -m unittest tests.test_preprocessing
python -m unittest tests.test_layers
```

## ⚙️ Advanced Configuration

### Hyperparameter Tuning

- **Sequence Length**: Longer = better context but slower training
- **Embedding Dimension**: Larger = more expressive but more parameters
- **Hidden Size**: Larger = more capacity but slower and prone to overfitting
- **Learning Rate**: Tune based on loss convergence (0.0001 - 0.01)
- **Temperature**: Lower (0.5) = conservative, Higher (1.5) = creative

### Character vs Word Level

- **Character-level**: Better for style, punctuation, spelling
- **Word-level**: Better for semantic meaning, faster generation

## 📊 Project Structure

```
citrus/
├── citrus/                 # Main package
│   ├── core/              # Neural network components
│   │   ├── layers.py      # LSTM, Dense, Embedding layers
│   │   ├── model.py       # Language model
│   │   └── optimizer.py   # SGD, Adam optimizers
│   ├── data/              # Data processing
│   │   ├── preprocessing.py  # Tokenization, encoding
│   │   └── loader.py         # Data loading
│   ├── models/            # Training & generation
│   │   ├── trainer.py     # Training loop
│   │   └── generator.py   # Text generation
│   └── utils/             # Utilities
├── data/
│   ├── raw/               # Training text files
│   └── processed/         # Processed data (auto-generated)
├── checkpoints/           # Model checkpoints
├── examples/              # Example scripts
├── tests/                 # Unit tests
├── train.py              # Training CLI
├── generate.py           # Generation CLI
└── requirements.txt      # Dependencies
```

## 🎓 Learning Resources

This project demonstrates:
- LSTM/RNN implementation from scratch
- Sequence-to-sequence modeling
- Neural text generation
- Optimization algorithms (SGD, Adam)
- Gradient descent and backpropagation
- Sampling strategies (temperature, top-k)

## 🤝 Contributing

This is a learning project built from scratch. Contributions are welcome!

Areas for improvement:
- Implement full backpropagation through time (BPTT)
- Add attention mechanisms
- Implement beam search for generation
- Add perplexity metrics
- Improve training speed with vectorization
- Add multi-layer LSTM support

## ⚠️ Limitations

As a from-scratch implementation:
- **Training is slow** - No GPU acceleration
- **Limited scalability** - Pure Python/NumPy
- **Basic gradients** - Uses finite differences (simplified)
- **Memory intensive** - Stores full gradients

This is intentional - the goal is learning and transparency, not production performance.

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

Built from scratch as a learning exercise in:
- Neural network architecture
- Natural language processing
- Writing style transfer
- Deep learning fundamentals

No pre-trained models or existing AI frameworks were used.
