# How to Use Citrus AI - Visual Guide

## Is It Hard to Use? 

**NO!** Here's proof - follow along:

---

## Method 1: Interactive Mode (Easiest!) 🎯

Just run one command and follow the prompts:

```bash
python easy_start.py
```

### What You'll See:

```
======================================================================
  🍊 Welcome to Citrus AI - Easy Start Mode! 🍊
======================================================================

This interactive guide will help you:
  1. Set up the AI
  2. Train it on your writing
  3. Generate new text in your style

It's easy - just follow the prompts!

Press Enter to continue...
```

The script will:
1. ✅ Check if NumPy is installed (installs if needed)
2. ✅ Check for your writing samples (or use the sample we included)
3. ✅ Train the AI (you choose how many epochs)
4. ✅ Generate text for you

**That's it!** No technical knowledge required.

---

## Method 2: Step by Step 📝

### Step 1: Install (30 seconds)

```bash
pip install -r requirements.txt
```

Output:
```
Successfully installed numpy-1.21.0
```

### Step 2: Add Your Writing (1 minute)

**Option A - Use the helper:**
```bash
python add_writing.py
```

You'll see:
```
======================================================================
  📝 Add Your Writing to Citrus AI
======================================================================

📁 Current files in data/raw:
   • sample_text.txt (2.3 KB)

Would you like me to help copy files? (y/n):
```

Just answer the questions!

**Option B - Do it manually:**
```bash
# Copy your .txt file
cp my_writing.txt data/raw/
```

### Step 3: Train (2-5 minutes)

```bash
python train.py --epochs 5
```

You'll see:
```
============================================================
Citrus AI Writing Style Model - Training
============================================================

1. Loading data from data/raw...
   Loaded 1 text file(s)

2. Preparing training data...
   Vocabulary size: 87
   Training samples: 234

3. Creating model...
   Embedding dimension: 128
   Hidden size: 256

4. Starting training...
  Epoch 1/5, Batch 10, Loss: 4.2341
  Epoch 1/5, Batch 20, Loss: 3.8765
  ...
  
Epoch 5/5 completed. Average Loss: 2.1234

Checkpoint saved to: checkpoints/checkpoint_epoch_5.pkl
```

### Step 4: Generate Text!

```bash
python generate.py \
    --checkpoint checkpoints/checkpoint_epoch_5.pkl \
    --prompt "The sun was setting"
```

Output:
```
============================================================
Citrus AI Writing Style Model - Text Generation
============================================================

1. Loading model from checkpoints/checkpoint_epoch_5.pkl...
   ✓ Model loaded

2. Setting up text generator...
   ✓ Generator ready

3. Generating text...
   Prompt: 'The sun was setting'
   Length: 200 tokens
   Temperature: 0.8
   Top-k: 5

============================================================
Generated Text:
============================================================
The sun was setting over the distant hills, casting long 
shadows across the valley. Winston looked out over the 
landscape, his thoughts wandering back to the events of 
the day...
============================================================
```

**You just created AI-generated text in your style!** 🎉

---

## Common Questions

### "Do I need to know programming?"

**No!** Just copy and paste the commands. The `easy_start.py` script guides you through everything.

### "Where do I type these commands?"

In your **terminal** (also called command prompt or shell):
- **Mac**: Open "Terminal" app
- **Windows**: Open "Command Prompt" or "PowerShell"  
- **Linux**: Open your terminal emulator

### "What is a .txt file?"

A plain text file! You can create one by:
1. Opening Notepad (Windows) or TextEdit (Mac)
2. Writing or pasting your text
3. Saving as "myfile.txt"

### "How much writing do I need?"

- **Minimum**: 5 KB (about 2-3 pages)
- **Good**: 10-20 KB (5-10 pages)
- **Better**: 50+ KB (20+ pages)

Don't have any? Use our sample file to try it out first!

### "How long does training take?"

- **Quick test** (5 epochs): 2-5 minutes
- **Standard** (10 epochs): 5-10 minutes
- **High quality** (20 epochs): 10-20 minutes

Depends on:
- Amount of text
- Your computer speed
- Number of epochs chosen

### "What's an epoch?"

Don't worry about it! Just know:
- **5 epochs** = Quick test
- **10 epochs** = Recommended
- **20 epochs** = Best results

The `easy_start.py` script will help you choose!

---

## Quick Reference Card

Save this for later:

```bash
# Interactive mode (easiest)
python easy_start.py

# Or individual commands:
pip install -r requirements.txt        # Install
python add_writing.py                  # Add your writing
python train.py --epochs 10            # Train
python generate.py --checkpoint checkpoints/checkpoint_epoch_10.pkl --prompt "Text here"

# Verify installation
python verify.py

# Get help
python train.py --help
python generate.py --help
```

---

## Still Confused?

1. Just run `python easy_start.py` - it's interactive!
2. See [QUICKSTART.md](QUICKSTART.md) for the 3-step guide
3. See [GETTING_STARTED.md](GETTING_STARTED.md) for detailed tutorial
4. See [README.md](README.md) for technical details

---

**Bottom Line**: Run `python easy_start.py` and follow the prompts. That's it! 🍊
