import os
import shutil

def cleanup_letters():
    letters_dir = os.path.join('images', 'letters')
    
    # Remove the entire letters directory
    if os.path.exists(letters_dir):
        shutil.rmtree(letters_dir)
        print(f"Removed {letters_dir}")
    
    # Recreate the basic directory structure
    for color in ['black', 'blue']:
        os.makedirs(os.path.join(letters_dir, 'set1', color), exist_ok=True)
        print(f"Created directory: {os.path.join(letters_dir, 'set1', color)}")

if __name__ == '__main__':
    cleanup_letters()
