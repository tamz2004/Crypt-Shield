# Crypt Shield

Crypt Shield is a Python application for securely encrypting and decrypting images using a combination of encryption techniques and chaos theory-based shuffling. This project aims to provide a secure method for transmitting images while adding an extra layer of protection through chaotic encryption.

## Features

- Encryption of images using chaotic key sequences generated from the Lorenz system.
- Shuffling of encrypted images before transmission.
- Decryption of reshuffled images using chaotic key sequences.

## Dependencies

- Python 3.x
- NumPy
- SciPy (for solving differential equations)
- PIL (Python Imaging Library)
- Tkinter (for the graphical user interface)

## Installation

1. Clone the repository to your local machine:

    ```
    git clone https://github.com/your_username/crypt-shield.git
    ```

2. Navigate to the project directory:

    ```
    cd crypt-shield
    ```

3. Install the required dependencies using pip:

    ```
    pip install -r requirements.txt
    ```

## Usage

To use Crypt Shield, follow these steps:

1. **Encryption**:
    - Run the `encryption.py` script to launch the encryption GUI.
    - Select the image you want to encrypt.
    - Click the "Encrypt Image" button to generate an encrypted image.
    - After encryption, the image will be shuffled for added security.

2. **Decryption**:
    - Run the `decryption.py` script to launch the decryption GUI.
    - Select the encrypted reshuffled image.
    - Click the "Decrypt Image" button to initiate the decryption process.
    - The decrypted image will be displayed in the GUI.


## License

This project is licensed under the MIT License - see the [LICENSE](/LICENSE) file for details.
