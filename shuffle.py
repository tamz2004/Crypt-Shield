from PIL import Image, ImageTk
import numpy as np
import tkinter as tk
from tkinter import filedialog

def shuffle_and_save(image_path, save_path):
    # Open the original image
    original_image = Image.open(image_path)
    original_array = np.array(original_image)

    # Get the shape of the array
    rows, cols, channels = original_array.shape

    # Reshape the 2D array to a 1D array
    flat_array = original_array.reshape(-1, channels)

    # Save the permutation used during shuffling
    permutation = np.arange(flat_array.shape[0])
    np.random.shuffle(permutation)

    # Shuffle the 1D array using the saved permutation
    shuffled_array = flat_array[permutation]

    # Reshape the shuffled array back to 2D
    shuffled_array = shuffled_array.reshape(rows, cols, channels)

    # Create a new image from the shuffled array
    shuffled_image = Image.fromarray(shuffled_array.astype('uint8'))

    # Save the shuffled image
    shuffled_image.save(save_path)

    # Save the permutation to a file
    np.save(save_path.replace(".png", "_permutation.npy"), permutation)

def select_image_and_shuffle():
    # Create a Tkinter window
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Ask the user to select an image file
    file_path = filedialog.askopenfilename(title="Select Image File", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])

    if file_path:
        # Generate a save path for the shuffled image
        save_path = file_path.replace(".", "_shuffled.")

        # Perform shuffling and save
        shuffle_and_save(file_path, save_path)

        print("Image shuffled and saved successfully.")

# Example usage for GUI
select_image_and_shuffle()
