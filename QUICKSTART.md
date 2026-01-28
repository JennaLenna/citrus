# QUICKSTART - Get Up and Running in 5 Minutes! ⚡

**Is it hard to use? NO!** Just follow these 3 simple steps.

## Step 1: Install (30 seconds)

```bash
pip install -r requirements.txt
```

That's it! Only one dependency (NumPy).

## Step 2: Add Your Writing (1 minute)

**Option A - Use the helper script (easiest):**
```bash
python add_writing.py
```
Just follow the prompts! It will help you add your text files.

**Option B - Do it manually:**
```bash
# Copy any .txt file with your writing into data/raw/
cp my_writing.txt data/raw/
```

**Don't have writing ready?** No problem! We included sample text so you can try it right now.

## Step 3: Run It! (2 minutes)

**Start the easy interactive mode:**
```bash
python easy_start.py
```

This will guide you through training and generating text step by step.

**OR use the command line directly:**
```bash
# Train the AI on your writing (takes 2-5 minutes)
python train.py --epochs 5

# Generate new text in your style
python generate.py --checkpoint checkpoints/checkpoint_epoch_5.pkl --prompt "The sun was setting"
```

## That's It! 🎉

You just trained an AI to write like you!

---

## What Each File Does (Simple Explanation)

- `add_writing.py` - Helps you add your writing samples
- `easy_start.py` - Interactive guided mode (easiest way)
- `train.py` - Trains the AI on your writing
- `generate.py` - Generates new text in your style
- `data/raw/` - Put your `.txt` files here

## Quick Tips

💡 **More writing = better results**
   - Aim for at least 10-20 KB of text
   - One or more .txt files is fine

💡 **Training takes time**
   - Small files: 2-5 minutes
   - Larger files: 10-30 minutes
   - This is normal!

💡 **First try the sample data**
   - We included a sample file so you can test immediately
   - Just run `python easy_start.py` right now!

## Need Help?

1. **Something not working?** Run `python verify.py` to check installation
2. **Want more control?** See `GETTING_STARTED.md` for detailed guide
3. **Technical details?** Check `README.md` and `DEVELOPMENT.md`

## Common Questions

**Q: Do I need to know programming?**
A: No! Just copy and paste the commands above.

**Q: Will this work on my computer?**
A: Yes! Works on Mac, Linux, and Windows with Python 3.7+

**Q: Is it really not hard to use?**
A: Really! The `easy_start.py` script guides you through everything.

**Q: How much text do I need?**
A: Start with whatever you have. Even 5-10 KB works. More is better but not required.

**Q: Can I use my blog posts / essays / stories?**
A: Yes! Any text you've written works great.

---

**Ready? Let's go!** 🚀

```bash
python easy_start.py
```
