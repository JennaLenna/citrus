# Getting Started with Citrus AI

Welcome! This guide will walk you through using Citrus to build a custom AI that learns your writing style.

## What You'll Build

By the end of this guide, you'll have:
- A trained AI model that understands a specific writing style
- The ability to generate new text in that style
- Understanding of how to tune the system for better results

## Prerequisites

- Python 3.7 or higher
- Basic command line knowledge
- Text samples of the writing style you want to learn (at least 5-10 KB recommended)

## Step 1: Installation

```bash
# Clone the repository
git clone https://github.com/JennaLenna/citrus.git
cd citrus

# Install dependencies
pip install -r requirements.txt

# Verify installation
python verify.py
```

You should see: "All checks passed! ✓"

## Step 2: Prepare Your Training Data

The AI learns from text files you provide. The more text, the better the learning.

### Where to Put Your Files

Place your `.txt` files in the `data/raw/` directory:

```bash
# Example: Copy your writing samples
cp my_essays.txt data/raw/
cp my_stories.txt data/raw/
cp my_journal.txt data/raw/
```

### What Makes Good Training Data?

✅ **Good:**
- At least 10-50 KB of text (more is better)
- Consistent writing style
- Clean, well-formatted text
- Representative of the style you want to learn

❌ **Avoid:**
- Mixed writing styles in the same dataset
- Very short texts (< 1 KB)
- Code or structured data (unless that's what you want to learn)
- Text with lots of special formatting

### Sample Data Included

We've included a sample text file at `data/raw/sample_text.txt` so you can try the system immediately.

## Step 3: Train Your First Model

Start with default settings for your first run:

```bash
python train.py --epochs 10
```

This will:
1. Load all `.txt` files from `data/raw/`
2. Build a vocabulary from your text
3. Train for 10 epochs (passes through the data)
4. Save checkpoints every 5 epochs

### What You'll See

```
============================================================
Citrus AI Writing Style Model - Training
============================================================

1. Loading data from data/raw...
   Loaded 3 text file(s)

2. Preparing training data...
   Vocabulary size: 87
   Training samples: 2451

3. Creating model...
   Embedding dimension: 128
   Hidden size: 256

4. Starting training...
  Epoch 1/10, Batch 10, Loss: 4.2341
  Epoch 1/10, Batch 20, Loss: 3.8765
  ...
```

### Training Time

- Small dataset (10 KB): ~5-10 minutes
- Medium dataset (100 KB): ~30-60 minutes  
- Large dataset (1 MB): several hours

**Tip:** Start with fewer epochs (5-10) to test, then do a longer run.

## Step 4: Generate Your First Text

Once training completes, generate text:

```bash
python generate.py \
    --checkpoint checkpoints/checkpoint_epoch_10.pkl \
    --prompt "The sun was setting" \
    --length 300
```

### Understanding the Output

The AI will generate text continuing from your prompt. For example:

```
============================================================
Generated Text:
============================================================
The sun was setting over the distant hills, casting long 
shadows across the valley. Winston thought about the day's 
events...
============================================================
```

### Generation Parameters

**--prompt** - Starting text
- Can be a few words or a sentence
- Helps guide the generation

**--length** - How many characters/words to generate
- Start with 200-500 for testing
- Can go higher once you're happy with quality

**--temperature** (optional, default 0.8)
- **0.3-0.5**: Very conservative, safe choices
- **0.7-0.9**: Balanced, recommended
- **1.0-1.5**: More creative, riskier

**--top-k** (optional, default 5)
- Only sample from top K most likely next tokens
- Lower (2-3): More focused
- Higher (10-20): More variety

### Example Variations

```bash
# More conservative generation
python generate.py --checkpoint checkpoints/checkpoint_epoch_10.pkl \
    --prompt "Once upon a time" --temperature 0.5 --top-k 3

# More creative generation  
python generate.py --checkpoint checkpoints/checkpoint_epoch_10.pkl \
    --prompt "In the beginning" --temperature 1.2 --top-k 10
```

## Step 5: Improve Your Results

If the generated text isn't great, try these improvements:

### 1. Train Longer

```bash
python train.py --epochs 50
```

More epochs = better learning (but watch for overfitting on small datasets)

### 2. Use More Data

Add more text files to `data/raw/`. Aim for at least 50-100 KB total.

### 3. Adjust Model Size

For more complex writing styles:

```bash
python train.py --hidden-size 512 --embedding-dim 256 --epochs 20
```

Larger models can learn more complex patterns but train slower.

### 4. Try Word-Level Instead of Character-Level

```bash
python train.py --level word --epochs 20
```

Word-level can be better for:
- Semantic meaning
- Faster generation
- Clearer output

Character-level is better for:
- Style and punctuation
- Handling rare words
- More flexibility

### 5. Tune Generation Parameters

Experiment with temperature and top-k:

```bash
# Try different temperatures
python generate.py --checkpoint checkpoints/checkpoint_epoch_20.pkl \
    --prompt "The" --temperature 0.6

python generate.py --checkpoint checkpoints/checkpoint_epoch_20.pkl \
    --prompt "The" --temperature 1.0
```

## Troubleshooting

### "No training data found"

**Problem:** No `.txt` files in `data/raw/`

**Solution:** Add text files to `data/raw/` directory

### Generated text is gibberish

**Problem:** Model hasn't learned enough yet

**Solutions:**
1. Train for more epochs (20-50)
2. Add more training data
3. Increase model size (--hidden-size 512)
4. Lower the temperature (--temperature 0.5)

### Training is very slow

**Problem:** Large dataset or large model

**Solutions:**
1. Reduce batch size: `--batch-size 16`
2. Reduce sequence length: `--seq-length 50`
3. Use a smaller model: `--hidden-size 128`
4. Reduce dataset size for testing

### Out of memory

**Problem:** Model or batch size too large

**Solutions:**
1. Reduce batch size: `--batch-size 8`
2. Reduce model size: `--hidden-size 128`
3. Reduce sequence length: `--seq-length 50`

## Advanced Usage

### Using the Python API

```python
from citrus.data.loader import DataLoader
from citrus.core.model import LanguageModel
from citrus.models.trainer import Trainer
from citrus.models.generator import TextGenerator

# Load and prepare data
loader = DataLoader('data/raw', seq_length=100, level='char')
loader.load_text_files()
sequences, targets = loader.prepare_training_data()

# Create and train model
model = LanguageModel(
    vocab_size=loader.get_vocab_size(),
    embedding_dim=128,
    hidden_size=256
)

trainer = Trainer(model, learning_rate=0.001)
trainer.train(sequences, targets, epochs=20)

# Generate text
generator = TextGenerator(model, loader.preprocessor)
text = generator.generate("Once upon a time", length=500)
print(text)
```

### Resuming Training

Currently, each training run starts fresh. To continue training:

1. Load the checkpoint
2. Create a new trainer with the loaded model
3. Continue training

```python
from citrus.models.trainer import Trainer

# Load existing model
model = Trainer.load_checkpoint('checkpoints/checkpoint_epoch_20.pkl')

# Continue training
trainer = Trainer(model, learning_rate=0.0005)  # Lower LR for fine-tuning
trainer.train(sequences, targets, epochs=10)
```

## Tips for Best Results

1. **Start Small**: Use default settings first
2. **More Data**: Quality training data is key
3. **Consistent Style**: Don't mix different writing styles
4. **Patience**: Training takes time, especially for larger datasets
5. **Experiment**: Try different hyperparameters
6. **Monitor Loss**: Should decrease over time
7. **Save Often**: Checkpoints save every 5 epochs automatically

## What's Next?

- Try training on different writing styles
- Experiment with prompt engineering
- Adjust hyperparameters for better results
- Contribute improvements to the project!

## Getting Help

If you run into issues:

1. Check this guide's troubleshooting section
2. Read `DEVELOPMENT.md` for technical details
3. Review the example scripts in `examples/`
4. Open an issue on GitHub

## Contributing

Found a bug or want to add a feature? Contributions welcome!

See `DEVELOPMENT.md` for:
- Architecture details
- How to add new features
- Code style guidelines
- Testing requirements

---

Happy writing! 🍊
