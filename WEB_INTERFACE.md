# Web Interface Guide - Citrus AI 🍊

## No Coding Required! Use Citrus AI Through Your Web Browser

The easiest way to use Citrus AI - just open your browser! Perfect if you're not comfortable with command lines or coding.

---

## 🚀 Quick Start

### 1. Start the Web Server

**On Mac/Linux:**
```bash
./start_web.sh
```

**On Windows:**
```bash
python web_app.py
```

**Or manually:**
```bash
pip install -r requirements.txt
python web_app.py
```

### 2. Open Your Browser

Go to: **http://localhost:5000**

That's it! You're ready to use Citrus AI! 🎉

---

## 📖 How to Use the Web Interface

### Step 1: Upload Your Writing

1. Click **"Upload Files"** in the navigation menu
2. Click the upload area or drag and drop your .txt files
3. Click **"Upload File"**
4. See your files listed on the right
5. You can upload multiple files!

**Tips:**
- Upload plain text (.txt) files only
- More text = better results (aim for 10-20 KB)
- Already have sample data? You can use that to test!

### Step 2: Train the Model

1. Click **"Train Model"** in the navigation menu
2. Choose your settings:
   - **Epochs:** 5 for quick test, 10 recommended, 20+ for best quality
   - **Model Size:** Medium is recommended
3. Click **"Start Training"**
4. Watch the progress bar - training takes 5-15 minutes
5. When complete, you'll see "Training complete!"

**What happens during training:**
- The AI reads all your uploaded text files
- It learns your vocabulary and writing patterns
- A "checkpoint" file is saved with the trained model

### Step 3: Generate Text

1. Click **"Generate Text"** in the navigation menu
2. Select your trained model from the dropdown
3. Enter a starting prompt (e.g., "The sun was setting")
4. Adjust length and creativity:
   - **Length:** How many characters to generate
   - **Creativity:** Lower = predictable, Higher = creative
5. Click **"Generate Text"**
6. See your AI-generated text appear!
7. Click **"Copy Text"** to copy it
8. Click **"Generate Again"** to try with different settings

**Try the example prompts** for quick ideas!

---

## 🎨 Interface Features

### Home Page
- Overview of the 3-step process
- Quick tips for best results
- Links to all sections

### Upload Page
- Drag and drop file upload
- View all uploaded files
- Delete files you don't want
- See total size of your training data

### Train Page
- Easy slider controls
- Progress tracking in real-time
- Training statistics (epoch, loss)
- Advanced settings available (optional)

### Generate Page
- Select from your trained models
- Adjustable generation length
- Creativity slider (temperature)
- Copy generated text with one click
- Example prompts to try

---

## 💡 Tips & Tricks

### For Best Results:

1. **Use Enough Text**
   - Minimum: 5 KB (about 2-3 pages)
   - Recommended: 10-20 KB (5-10 pages)
   - Best: 50+ KB (20+ pages)

2. **Training Settings**
   - Start with 10 epochs to see results
   - Use "Medium" model size
   - Let training complete fully

3. **Generation Tips**
   - Try different prompts
   - Experiment with creativity (0.5-1.2 works well)
   - Generate multiple times with same prompt for variety

4. **Be Patient**
   - Training takes time (normal!)
   - First epoch is slowest
   - Progress bar shows status

### Troubleshooting:

**"No files uploaded yet"**
- Go to Upload page and add your .txt files

**"No trained models found"**
- Train a model first on the Train page

**Training seems stuck**
- Check the progress bar and status message
- First epoch can take a while
- Be patient, it's learning!

**Generation produces gibberish**
- Train for more epochs (try 15-20)
- Add more training text
- Lower the creativity slider

---

## 🔧 Advanced Features

### Multiple Models
- Train different models with different settings
- Each checkpoint is saved separately
- Select which model to use for generation

### Settings Explained:

**Epochs:** Number of times the AI reviews your writing
- More epochs = better learning
- But takes longer

**Model Size:** How big the neural network is
- Small (64): Fast, less accurate
- Medium (128): Balanced (recommended)
- Large (256): Slow, more accurate

**Sequence Length:** How much text the AI looks at once
- Affects context understanding
- 50 is a good default

**Temperature:** Controls randomness
- 0.3-0.5: Conservative, safe
- 0.7-0.9: Balanced, creative
- 1.0-1.5: Very creative, risky

---

## 📱 Using on Different Devices

### Desktop/Laptop (Recommended)
- Open any browser (Chrome, Firefox, Safari, Edge)
- Best experience with full screen

### Mobile/Tablet
- Works on mobile browsers!
- Upload might be tricky (use cloud storage)
- Best for viewing and generating, not training

### Local Network Access
- Server runs on your computer
- Can access from other devices on same WiFi
- Use your computer's IP address instead of localhost

---

## 🆘 Common Questions

**Q: Do I need to install anything?**
A: Just Python and the requirements (Flask, NumPy). The startup script does this for you.

**Q: Can I close the browser?**
A: Yes! The server keeps running. Just go back to http://localhost:5000

**Q: What if I close the terminal/command prompt?**
A: The server stops. Your trained models are saved though!

**Q: Can I use this offline?**
A: Yes! Everything runs on your computer, no internet needed.

**Q: Where are my files stored?**
A: In the `data/raw/` and `checkpoints/` folders in the Citrus directory.

**Q: Can I train multiple models?**
A: Yes! Each training creates a new checkpoint file.

**Q: How do I stop the server?**
A: Press Ctrl+C in the terminal where it's running.

---

## 🎓 Learning More

- **Not working?** Check the terminal for error messages
- **Want command line?** See QUICKSTART.md or GETTING_STARTED.md
- **Technical details?** Check README.md and DEVELOPMENT.md

---

## 🌟 Why Use the Web Interface?

✅ **No coding required** - Just click and use  
✅ **Visual feedback** - See progress in real-time  
✅ **User-friendly** - Clear instructions on every page  
✅ **Modern design** - Nice, clean interface  
✅ **Easy to share** - Show it to non-technical friends  
✅ **All features** - Upload, train, generate - all in one place  

---

**Enjoy using Citrus AI through your browser!** 🍊

Questions? Issues? Check the terminal output for helpful error messages!
