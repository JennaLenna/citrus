# Citrus AI - Development Guide

## System Architecture

### Overview

Citrus is a character/word-level language model built from scratch that learns writing styles and generates new text. The system uses LSTM (Long Short-Term Memory) networks to capture sequential patterns in text.

### Core Components

#### 1. Data Processing (`citrus/data/`)

**TextPreprocessor** (`preprocessing.py`)
- Cleans and normalizes input text
- Tokenizes text at character or word level
- Builds vocabulary mapping tokens ↔ integers
- Encodes/decodes between text and integer sequences

**SequenceGenerator** (`preprocessing.py`)
- Creates fixed-length training sequences
- Generates (input, target) pairs for supervised learning

**DataLoader** (`loader.py`)
- Loads text files from directory
- Coordinates preprocessing and sequence generation
- Prepares batches for training

#### 2. Neural Network (`citrus/core/`)

**Activation Functions** (`layers.py`)
- Sigmoid: σ(x) = 1/(1 + e^(-x))
- Tanh: tanh(x)
- Softmax: for probability distributions

**LSTMCell** (`layers.py`)
- Implements LSTM cell with 4 gates:
  - Input gate: controls what to add to cell state
  - Forget gate: controls what to remove from cell state
  - Output gate: controls what to output
  - Cell state update: candidate values for cell state

**EmbeddingLayer** (`layers.py`)
- Maps token IDs to dense vectors
- Learned during training

**DenseLayer** (`layers.py`)
- Fully connected layer
- Output layer for vocabulary prediction

**LanguageModel** (`model.py`)
- Combines all layers into a complete model
- Forward pass: embedding → LSTM → dense → softmax
- Maintains hidden and cell states

#### 3. Training (`citrus/models/`)

**Optimizer** (`optimizer.py`)
- SGD: Basic gradient descent
- Adam: Adaptive learning rates with momentum
- Gradient clipping: prevent exploding gradients

**Trainer** (`trainer.py`)
- Training loop implementation
- Gradient computation (currently using finite differences)
- Checkpoint saving/loading
- Loss tracking

**Generator** (`generator.py`)
- Text generation from trained model
- Sampling strategies:
  - Temperature scaling: controls randomness
  - Top-k sampling: sample from k most likely tokens

### Training Algorithm

1. **Initialization**
   - Load and preprocess text data
   - Build vocabulary
   - Initialize model weights randomly (Xavier initialization)

2. **Forward Pass**
   ```
   For each sequence:
     1. Look up token embeddings
     2. Feed through LSTM cell by cell
     3. Project LSTM output to vocabulary size
     4. Apply softmax to get probabilities
   ```

3. **Loss Computation**
   ```
   Cross-Entropy Loss:
   L = -log(P(target_token | sequence))
   ```

4. **Backward Pass** (Simplified)
   - Currently using finite differences for gradients
   - Production would use Backpropagation Through Time (BPTT)

5. **Parameter Update**
   ```
   Adam optimizer:
   m_t = β1 * m_{t-1} + (1-β1) * gradient
   v_t = β2 * v_{t-1} + (1-β2) * gradient^2
   θ_t = θ_{t-1} - α * m_t / (√v_t + ε)
   ```

### Generation Algorithm

1. **Initialization**
   - Start with seed text or random token
   - Reset LSTM hidden/cell states

2. **Autoregressive Generation**
   ```
   For each new token:
     1. Feed current token through model
     2. Get probability distribution over vocabulary
     3. Sample next token:
        - Apply temperature: probs^(1/temp)
        - Top-k filter: keep only k highest probs
        - Sample from filtered distribution
     4. Use sampled token as next input
   ```

## Implementation Details

### LSTM Mathematics

The LSTM cell computes:

```python
# Input gate
i_t = σ(W_i * x_t + U_i * h_{t-1} + b_i)

# Forget gate  
f_t = σ(W_f * x_t + U_f * h_{t-1} + b_f)

# Output gate
o_t = σ(W_o * x_t + U_o * h_{t-1} + b_o)

# Cell candidate
c̃_t = tanh(W_c * x_t + U_c * h_{t-1} + b_c)

# Cell state update
c_t = f_t ⊙ c_{t-1} + i_t ⊙ c̃_t

# Hidden state update
h_t = o_t ⊙ tanh(c_t)
```

Where:
- σ = sigmoid function
- ⊙ = element-wise multiplication
- W, U, b = learned parameters

### Weight Initialization

**Xavier Initialization:**
```python
scale = sqrt(2.0 / (fan_in + fan_out))
W = random.randn(shape) * scale
```

This prevents vanishing/exploding gradients during initialization.

### Training Tips

1. **Start Small**
   - Begin with small datasets (few KB of text)
   - Use smaller hidden sizes (64-128) for faster iteration
   - Gradually scale up

2. **Monitor Loss**
   - Loss should decrease over epochs
   - If loss plateaus, try adjusting learning rate
   - If loss explodes, decrease learning rate or check gradient clipping

3. **Hyperparameters**
   - Learning rate: 0.0001 - 0.01 (start with 0.001)
   - Hidden size: 128 - 512 (larger for more complex styles)
   - Sequence length: 50 - 200 (longer for better context)
   - Batch size: 16 - 64 (larger for stability)

4. **Generation Quality**
   - Temperature < 0.5: Very conservative, repetitive
   - Temperature 0.7-0.9: Good balance
   - Temperature > 1.2: Very creative, possibly nonsensical
   - Top-k: 3-10 works well (lower = more focused)

## Future Improvements

### High Priority

1. **Backpropagation Through Time (BPTT)**
   - Replace finite differences with proper BPTT
   - Much faster and more accurate gradients

2. **Preprocessing Persistence**
   - Save preprocessor with model checkpoints
   - Ensures vocabulary consistency

3. **Batch Processing**
   - Process multiple sequences simultaneously
   - Vectorize operations for speed

### Medium Priority

4. **Attention Mechanism**
   - Allow model to "attend" to different parts of input
   - Better long-range dependencies

5. **Multi-layer LSTM**
   - Stack LSTM layers for more capacity
   - Better modeling of complex styles

6. **Validation Set**
   - Split data into train/validation
   - Monitor overfitting

### Low Priority

7. **Beam Search**
   - Alternative to sampling for generation
   - More deterministic outputs

8. **Perplexity Metric**
   - Standard metric for language models
   - Evaluate model quality

## Debugging Guide

### Common Issues

**Issue: "No training data found"**
- Ensure .txt files are in data/raw/
- Check file permissions

**Issue: Loss is NaN**
- Decrease learning rate
- Check for invalid characters in input
- Ensure gradient clipping is enabled

**Issue: Model generates gibberish**
- Train for more epochs
- Increase model size (hidden_size)
- Check that vocabulary was built correctly

**Issue: Out of memory**
- Reduce batch size
- Reduce sequence length
- Reduce hidden size

**Issue: Training is too slow**
- This is expected with finite differences
- Reduce dataset size for testing
- Reduce number of epochs
- Consider implementing BPTT for speed

## Code Style Guide

- Follow PEP 8
- Use type hints where possible
- Document all classes and public methods
- Keep functions focused and modular
- Add unit tests for new features

## Testing

Run tests before committing:
```bash
python -m unittest discover tests
```

Add tests for new features in `tests/` directory.
