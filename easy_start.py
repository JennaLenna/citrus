#!/usr/bin/env python3
"""
Easy Start - Interactive guided setup for Citrus AI
Makes it super simple to train and use the AI!
"""

import os
import sys
import subprocess

# Add current directory to path to import citrus package
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def print_header(text):
    """Print a nice header."""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def print_step(number, text):
    """Print a step number."""
    print(f"\n{'▶' * 3} STEP {number}: {text}")


def check_installation():
    """Check if numpy is installed."""
    try:
        import numpy
        return True
    except ImportError:
        return False


def check_training_data():
    """Check if there are any text files in data/raw/."""
    data_dir = 'data/raw'
    if not os.path.exists(data_dir):
        return False, []
    
    txt_files = [f for f in os.listdir(data_dir) if f.endswith('.txt')]
    return len(txt_files) > 0, txt_files


def get_user_choice(prompt, choices):
    """Get a choice from the user."""
    while True:
        print(f"\n{prompt}")
        for i, choice in enumerate(choices, 1):
            print(f"  {i}. {choice}")
        
        try:
            choice = input("\nYour choice (enter number): ").strip()
            choice_num = int(choice)
            if 1 <= choice_num <= len(choices):
                return choice_num
            else:
                print(f"Please enter a number between 1 and {len(choices)}")
        except ValueError:
            print("Please enter a valid number")
        except KeyboardInterrupt:
            print("\n\nExiting...")
            sys.exit(0)


def get_yes_no(prompt):
    """Get yes/no from user."""
    while True:
        response = input(f"\n{prompt} (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            print("Please enter 'y' or 'n'")


def main():
    """Run the interactive setup."""
    
    print_header("🍊 Welcome to Citrus AI - Easy Start Mode! 🍊")
    
    print("\nThis interactive guide will help you:")
    print("  1. Set up the AI")
    print("  2. Train it on your writing")
    print("  3. Generate new text in your style")
    print("\nIt's easy - just follow the prompts!")
    
    input("\nPress Enter to continue...")
    
    # Step 1: Check installation
    print_step(1, "Checking Installation")
    
    if not check_installation():
        print("\n⚠️  NumPy is not installed.")
        print("\nLet's install it now!")
        print("Running: pip install -r requirements.txt")
        
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
                         check=True)
            print("\n✅ Installation complete!")
        except subprocess.CalledProcessError:
            print("\n❌ Installation failed. Please run manually:")
            print("   pip install -r requirements.txt")
            sys.exit(1)
    else:
        print("\n✅ Installation looks good!")
    
    # Step 2: Check training data
    print_step(2, "Checking Your Writing Samples")
    
    has_data, txt_files = check_training_data()
    
    if has_data:
        print(f"\n✅ Found {len(txt_files)} text file(s):")
        for f in txt_files:
            file_path = os.path.join('data/raw', f)
            size = os.path.getsize(file_path)
            print(f"   - {f} ({size:,} bytes)")
    else:
        print("\n⚠️  No training data found in data/raw/")
        print("\nYou have two options:")
        
        choice = get_user_choice(
            "What would you like to do?",
            [
                "Use the included sample text (try it out first)",
                "Add my own writing files now",
                "Exit and add files manually later"
            ]
        )
        
        if choice == 1:
            print("\n✅ Great! We'll use the sample text included with Citrus.")
            print("   (You can add your own writing later)")
            has_data = True
        elif choice == 2:
            print("\n📝 To add your writing:")
            print("   1. Save your writing as .txt files")
            print(f"   2. Copy them to: {os.path.abspath('data/raw/')}")
            print("   3. Come back and run this script again")
            print("\nOR use the helper script:")
            print("   python add_writing.py")
            sys.exit(0)
        else:
            print("\n👋 No problem! Add your .txt files to data/raw/ and run this again.")
            sys.exit(0)
    
    # Step 3: Train the model
    print_step(3, "Training the AI")
    
    print("\nNow we'll train the AI to learn the writing style.")
    print("\nTraining options:")
    print("  • Quick test (5 epochs, ~2 minutes)")
    print("  • Standard (10 epochs, ~5 minutes)")
    print("  • High quality (20 epochs, ~10 minutes)")
    
    choice = get_user_choice(
        "How much training?",
        [
            "Quick test (5 epochs) - Good for trying it out",
            "Standard (10 epochs) - Recommended",
            "High quality (20 epochs) - Best results",
            "Custom number of epochs"
        ]
    )
    
    epoch_map = {1: 5, 2: 10, 3: 20}
    
    if choice in epoch_map:
        epochs = epoch_map[choice]
    else:
        while True:
            try:
                epochs = int(input("\nEnter number of epochs (1-100): "))
                if 1 <= epochs <= 100:
                    break
                print("Please enter a number between 1 and 100")
            except ValueError:
                print("Please enter a valid number")
    
    print(f"\n🚀 Starting training with {epochs} epochs...")
    print("This will take a few minutes. You'll see progress updates.\n")
    
    input("Press Enter to start training...")
    
    # Run training
    try:
        result = subprocess.run(
            [sys.executable, "train.py", "--epochs", str(epochs), "--batch-size", "16"],
            check=True
        )
        
        print("\n✅ Training complete!")
        
    except subprocess.CalledProcessError:
        print("\n❌ Training failed. Check the error messages above.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Training interrupted.")
        sys.exit(1)
    
    # Step 4: Generate text
    print_step(4, "Generate New Text!")
    
    print("\nNow let's generate some text in your learned style!")
    
    # Find the checkpoint
    checkpoint_path = f"checkpoints/checkpoint_epoch_{epochs}.pkl"
    
    if not os.path.exists(checkpoint_path):
        print(f"\n⚠️  Checkpoint not found at {checkpoint_path}")
        print("Looking for any available checkpoints...")
        
        checkpoints = [f for f in os.listdir('checkpoints') if f.endswith('.pkl')]
        if checkpoints:
            checkpoint_path = os.path.join('checkpoints', checkpoints[-1])
            print(f"Found: {checkpoint_path}")
        else:
            print("No checkpoints found. Training may have failed.")
            sys.exit(1)
    
    # Get prompt from user
    print("\n📝 Enter a prompt (starting text) for generation.")
    print("Examples:")
    print('  - "The sun was setting"')
    print('  - "It was a dark"')
    print('  - "Once upon a time"')
    
    prompt = input("\nYour prompt: ").strip()
    
    if not prompt:
        prompt = "The"
        print(f"Using default prompt: '{prompt}'")
    
    # Get length
    print("\n📏 How much text to generate?")
    choice = get_user_choice(
        "Choose length:",
        [
            "Short (~100 characters)",
            "Medium (~300 characters)",
            "Long (~500 characters)"
        ]
    )
    
    length_map = {1: 100, 2: 300, 3: 500}
    length = length_map[choice]
    
    print(f"\n🎨 Generating {length} characters of text...")
    print("Temperature: 0.8 (balanced creativity)")
    print()
    
    # Run generation
    try:
        subprocess.run(
            [
                sys.executable, "generate.py",
                "--checkpoint", checkpoint_path,
                "--prompt", prompt,
                "--length", str(length),
                "--temperature", "0.8"
            ],
            check=True
        )
        
    except subprocess.CalledProcessError:
        print("\n❌ Generation failed. Check the error messages above.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Generation interrupted.")
        sys.exit(1)
    
    # Done!
    print_header("🎉 Success! 🎉")
    
    print("\nYou've successfully:")
    print("  ✅ Trained an AI on writing samples")
    print("  ✅ Generated new text in that style")
    
    print("\n💡 What's next?")
    print("  • Add more of your writing to data/raw/ for better results")
    print("  • Train for more epochs for higher quality")
    print("  • Experiment with different prompts")
    print("  • Try different temperatures (0.3 = conservative, 1.2 = creative)")
    
    print("\n📚 To generate more text:")
    print(f'  python generate.py --checkpoint {checkpoint_path} --prompt "Your text here"')
    
    print("\n🔁 Want to try again?")
    if get_yes_no("Run easy start again"):
        print("\n" * 2)
        main()
    else:
        print("\n👋 Thanks for using Citrus AI!")
        print("Check QUICKSTART.md for quick commands")
        print("Check GETTING_STARTED.md for detailed tutorial")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
