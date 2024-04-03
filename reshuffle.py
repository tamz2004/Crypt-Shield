from PIL import Image, ImageTk
import numpy as np
import tkinter as tk
from tkinter import filedialog

def reshuffle_and_save(shuffled_image_path, permutation_file_path):
    # Load the shuffled image
    shuffled_image = Image.open(shuffled_image_path)
    shuffled_array = np.array(shuffled_image)

    # Load the saved permutation
    permutation = np.load(permutation_file_path)

    # Reshuffle the 1D array using the inverse permutation
    reshuffled_array = shuffled_array.reshape(-1, shuffled_array.shape[2])[np.argsort(permutation)].reshape(shuffled_array.shape)

    # Create a new image from the reshuffled array
    reshuffled_image = Image.fromarray(reshuffled_array.astype('uint8'))

    # Save the reshuffled image to the specified path
    save_path = "C:/Users/Kirubakaran/OneDrive/Pictures/images/reshuffled_image.png"
    reshuffled_image.save(save_path)

    print(f"Image reshuffled and saved to: {save_path}")

def select_image_and_reshuffle():
    # Create a Tkinter window
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Ask the user to select the shuffled image file
    shuffled_image_path = filedialog.askopenfilename(title="Select Shuffled Image File", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])

    if shuffled_image_path:
        # Ask the user to select the permutation file
        permutation_file_path = filedialog.askopenfilename(title="Select Permutation File", filetypes=[("NumPy files", "*.npy")])

        if permutation_file_path:
            # Perform reshuffling and save
            reshuffle_and_save(shuffled_image_path, permutation_file_path)

# Example usage for GUI
select_image_and_reshuffle()
