from PIL import Image, ImageTk
import numpy as np
from scipy.integrate import solve_ivp
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

def encrypt_image(image_path, key_sequence):
    im = Image.open(image_path)
    im_array = np.array(im)
     
    # Flatten the image array for encryption
    flat_image = im_array.flatten().astype(int)  # Convert to integer type

    # Calculate the required length for the key sequence
    key_sequence_length = len(flat_image)

    # Ensure the key sequence length matches the number of pixels in the image
    key_sequence_flat = key_sequence.flatten().astype(int)  # Flatten and convert to integer type
    key_sequence_flat = np.tile(key_sequence_flat, key_sequence_length // len(key_sequence_flat) + 1)[:key_sequence_length]

    # XOR encryption using the chaotic key
    encrypted_image = np.bitwise_xor(flat_image, key_sequence_flat)

    # Reshape the encrypted pixels to the original image shape
    encrypted_image = encrypted_image.reshape(im_array.shape)

    # Create an encrypted image from the array
    encrypted_im = Image.fromarray(encrypted_image.astype('uint8'))

    return encrypted_im

class ImageEncryptorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Encryption App")

        # Create GUI elements with color changes
        self.select_image_button = tk.Button(root, text="Select Image", command=self.select_image, bg="lightblue", fg="black")
        self.select_image_button.pack(pady=10)

        self.encrypt_button = tk.Button(root, text="Encrypt Image", command=self.encrypt_image, bg="lightgreen", fg="black")
        self.encrypt_button.pack(pady=10)

        # Display encrypted image
        self.encrypted_image_label = tk.Label(root, text="", bg="white")
        self.encrypted_image_label.pack()

        # Set default values
        self.image_path = ""
        self.output_path = ""

    def select_image(self):
        self.image_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])

    def encrypt_image(self):
        if self.image_path:
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

            # Image encryption
            output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            encrypted_image = encrypt_image(self.image_path, lorenz_key_sequence)

            # Save the encrypted image
            encrypted_image.save(output_path)

            # Display encrypted image
            self.display_encrypted_image(output_path)
        else:
            self.encrypted_image_label.config(text="Please select an image first.")

    def display_encrypted_image(self, image_path):
        encrypted_image = Image.open(image_path)
        encrypted_image.thumbnail((300, 300))  # Resize for display if needed
        photo = ImageTk.PhotoImage(encrypted_image)

        # Update label with encrypted image
        self.encrypted_image_label.config(text="Encrypted Image", image=photo)
        self.encrypted_image_label.image = photo

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEncryptorApp(root)
    root.mainloop()
