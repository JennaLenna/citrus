#!/usr/bin/env python3
"""
Add Writing - Helper script to easily add your writing samples to Citrus AI
"""

import os
import sys
import shutil


def print_header(text):
    """Print a nice header."""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def get_file_size_kb(filepath):
    """Get file size in KB."""
    size_bytes = os.path.getsize(filepath)
    return size_bytes / 1024


def main():
    """Interactive script to help users add their writing."""
    
    print_header("📝 Add Your Writing to Citrus AI")
    
    print("\nThis tool helps you add your writing samples for training.")
    print("\nYour writing can be:")
    print("  • Blog posts")
    print("  • Essays")
    print("  • Stories or fiction")
    print("  • Journal entries")
    print("  • Any text you've written!")
    
    print("\n💡 Tips:")
    print("  • Save your writing as .txt files (plain text)")
    print("  • More text = better results (aim for 10-50 KB total)")
    print("  • Keep consistent writing style in each file")
    
    # Ensure data/raw exists
    data_dir = 'data/raw'
    os.makedirs(data_dir, exist_ok=True)
    
    # Show current files
    existing_files = [f for f in os.listdir(data_dir) if f.endswith('.txt')]
    
    if existing_files:
        print(f"\n📁 Current files in {data_dir}:")
        total_size = 0
        for f in existing_files:
            filepath = os.path.join(data_dir, f)
            size_kb = get_file_size_kb(filepath)
            total_size += size_kb
            print(f"   • {f} ({size_kb:.1f} KB)")
        print(f"\n   Total: {total_size:.1f} KB")
    else:
        print(f"\n📁 No files in {data_dir} yet")
    
    print("\n" + "-" * 70)
    
    # Guide user through adding files
    print("\n🎯 How to add your writing:")
    print("\n  Option 1: Copy files manually")
    print(f"    → Copy your .txt files to: {os.path.abspath(data_dir)}")
    
    print("\n  Option 2: Let me help you copy files")
    
    response = input("\nWould you like me to help copy files? (y/n): ").strip().lower()
    
    if response not in ['y', 'yes']:
        print(f"\n👍 OK! Just copy your .txt files to:")
        print(f"   {os.path.abspath(data_dir)}")
        print("\nThen run:")
        print("   python easy_start.py")
        return
    
    # Help copy files
    print("\n" + "=" * 70)
    print("  File Copy Helper")
    print("=" * 70)
    
    while True:
        print("\n📂 Enter the path to a text file you want to add:")
        print("   (or type 'done' when finished)")
        
        file_path = input("\nFile path: ").strip()
        
        if file_path.lower() == 'done':
            break
        
        # Remove quotes if user included them
        file_path = file_path.strip('"').strip("'")
        
        # Expand user home directory
        file_path = os.path.expanduser(file_path)
        
        # Check if file exists
        if not os.path.exists(file_path):
            print(f"\n❌ File not found: {file_path}")
            print("   Make sure the path is correct and try again.")
            continue
        
        # Check if it's a file
        if not os.path.isfile(file_path):
            print(f"\n❌ This is a directory, not a file: {file_path}")
            continue
        
        # Get filename
        filename = os.path.basename(file_path)
        
        # Ensure it's a .txt file
        if not filename.endswith('.txt'):
            print(f"\n⚠️  File doesn't end with .txt: {filename}")
            response = input("   Add it anyway? (y/n): ").strip().lower()
            if response not in ['y', 'yes']:
                continue
            
            # Add .txt extension
            if '.' in filename:
                filename = filename.rsplit('.', 1)[0] + '.txt'
            else:
                filename = filename + '.txt'
            
            print(f"   Will save as: {filename}")
        
        # Check size
        size_kb = get_file_size_kb(file_path)
        
        if size_kb < 1:
            print(f"\n⚠️  File is very small ({size_kb:.1f} KB)")
            print("   For best results, aim for at least 5-10 KB")
            response = input("   Add it anyway? (y/n): ").strip().lower()
            if response not in ['y', 'yes']:
                continue
        
        # Copy the file
        dest_path = os.path.join(data_dir, filename)
        
        if os.path.exists(dest_path):
            print(f"\n⚠️  File already exists: {filename}")
            response = input("   Overwrite? (y/n): ").strip().lower()
            if response not in ['y', 'yes']:
                # Ask for new name
                new_name = input("   Enter new filename: ").strip()
                if not new_name:
                    continue
                if not new_name.endswith('.txt'):
                    new_name += '.txt'
                dest_path = os.path.join(data_dir, new_name)
        
        try:
            shutil.copy2(file_path, dest_path)
            print(f"\n✅ Added: {os.path.basename(dest_path)} ({size_kb:.1f} KB)")
        except Exception as e:
            print(f"\n❌ Error copying file: {e}")
            continue
    
    # Show final summary
    print("\n" + "=" * 70)
    print("  Summary")
    print("=" * 70)
    
    final_files = [f for f in os.listdir(data_dir) if f.endswith('.txt')]
    
    if final_files:
        total_size = 0
        print(f"\n📚 Files ready for training ({len(final_files)} files):")
        for f in final_files:
            filepath = os.path.join(data_dir, f)
            size_kb = get_file_size_kb(filepath)
            total_size += size_kb
            print(f"   • {f} ({size_kb:.1f} KB)")
        
        print(f"\n   Total: {total_size:.1f} KB")
        
        if total_size < 5:
            print("\n💡 Tip: For better results, add more text (aim for 10-50 KB)")
        elif total_size < 20:
            print("\n💡 Good amount! More text will improve results further.")
        else:
            print("\n✅ Great! This should produce good results.")
        
        print("\n🚀 Next step: Train the AI!")
        print("   python easy_start.py")
        
    else:
        print("\n📁 No files added yet.")
        print("\nTo add files manually:")
        print(f"   1. Save your writing as .txt files")
        print(f"   2. Copy them to: {os.path.abspath(data_dir)}")
        print(f"   3. Run: python easy_start.py")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
