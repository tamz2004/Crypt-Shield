import numpy as np
from scipy.integrate import solve_ivp
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog

# Lorenz system equations
def lorenz_system(t, vars, sigma, rho, beta):
    x, y, z = vars
    dx_dt = sigma * (y - x)
    dy_dt = rho * x - y - x * z
    dz_dt = x * y - beta * z
    return [dx_dt, dy_dt, dz_dt]

# Function to generate chaotic key sequence using Lorenz system
def generate_lorenz_key(sigma, rho, beta, initial_conditions, t_span, t_steps):
    lorenz_sol = solve_ivp(lorenz_system, t_span, initial_conditions, args=(sigma, rho, beta), dense_output=True)
    t_values = np.linspace(t_span[0], t_span[1], t_steps)
    key_sequence = lorenz_sol.sol(t_values).T
    return key_sequence

# Function to decrypt the image using chaotic key
def decrypt_image(encrypted_image_path, key_sequence):
    encrypted_im = Image.open(encrypted_image_path)
    encrypted_array = np.array(encrypted_im)

    # Flatten the encrypted image array for decryption
    flat_encrypted = encrypted_array.flatten().astype(int)

    # Calculate the required length for the key sequence
    key_sequence_length = len(flat_encrypted)

    # Ensure the key sequence length matches the number of pixels in the encrypted image
    key_sequence_flat = key_sequence.flatten().astype(int)
    key_sequence_flat = np.tile(key_sequence_flat, key_sequence_length // len(key_sequence_flat) + 1)[:key_sequence_length]

    # XOR decryption using the chaotic key
    decrypted_array = np.bitwise_xor(flat_encrypted, key_sequence_flat)

    # Reshape the decrypted pixels to the original image shape
    decrypted_array = decrypted_array.reshape(encrypted_array.shape)

    # Create a decrypted image from the array
    decrypted_im = Image.fromarray(decrypted_array.astype('uint8'))

    return decrypted_im

class ImageDecryptorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Decryption App")
        self.root.geometry("400x400")  # Set initial window size

        # Create GUI elements
        self.select_encrypted_image_button = tk.Button(root, text="Select Encrypted Image", command=self.select_encrypted_image, bg="lightblue")
        self.select_encrypted_image_button.pack(pady=10)

        self.decrypt_button = tk.Button(root, text="Decrypt Image", command=self.decrypt_image, bg="lightgreen")
        self.decrypt_button.pack(pady=10)

        # Display decrypted image
        self.decrypted_image_label = tk.Label(root, text="", bg="white")
        self.decrypted_image_label.pack()

        # Set default values
        self.encrypted_image_path = ""

    def select_encrypted_image(self):
        self.encrypted_image_path = filedialog.askopenfilename(title="Select Encrypted Image", filetypes=[("Image files", "*.png")])

    def decrypt_image(self):
        if self.encrypted_image_path:
            # Parameters for Lorenz system
            sigma = 10
            rho = 28
            beta = 8/3

            # Initial conditions for the Lorenz system
            initial_conditions = [1.0, 1.0, 1.0]

            # Time span and steps for Lorenz system simulation
            t_span = (0, 20)
            t_steps = 10000

            # Generate chaotic key sequence using Lorenz system
            lorenz_key_sequence = generate_lorenz_key(sigma, rho, beta, initial_conditions, t_span, t_steps)

            # Decrypt the encrypted image using the Lorenz key sequence
            decrypted_image = decrypt_image(self.encrypted_image_path, lorenz_key_sequence)

            # Display decrypted image
            self.display_decrypted_image(decrypted_image)
        else:
            self.decrypted_image_label.config(text="Please select an encrypted image first.")

    def display_decrypted_image(self, decrypted_image):
        decrypted_image.thumbnail((300, 300))  # Resize for display if needed
        photo = ImageTk.PhotoImage(decrypted_image)

        # Update label with decrypted image
        self.decrypted_image_label.config(text="Decrypted Image", image=photo)
        self.decrypted_image_label.image = photo

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageDecryptorApp(root)
    root.mainloop()
