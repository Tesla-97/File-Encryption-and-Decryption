import os
import tkinter as tk
from tkinter import filedialog
from cryptography.fernet import Fernet
from PIL import Image, ImageTk

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("File Encryptor // Decryptor")
        self.master.geometry("300x300")
        self.pack()

        # Load the image and create a PhotoImage object
        img = Image.open("lock.jpg")
        self.img_tk = ImageTk.PhotoImage(img)

        # Create a canvas widget and add the image to it
        self.canvas = tk.Canvas(self, width=500, height=300)
        self.canvas.create_image(0, 0, image=self.img_tk, anchor="nw")
        self.canvas.pack()

        # Create the "Encrypt" button
        self.encrypt_button = tk.Button(self.canvas, text="Encrypt", command=self.encrypt_file)
        self.encrypt_button.place(relx=0.5, rely=0.3, anchor="center")

        # Create the "Decrypt" button
        self.decrypt_button = tk.Button(self.canvas, text="Decrypt", command=self.decrypt_file)
        self.decrypt_button.place(relx=0.5, rely=0.7, anchor="center")

    def get_file_path(self):
        # Open a file dialog to select a file
        file_path = filedialog.askopenfilename()
        return file_path

    def save_file_path(self):
        # Open a file dialog to save a file
        file_path = filedialog.asksaveasfilename()
        return file_path

    def encrypt_file(self):
        # Get the file path of the file to encrypt
        file_path = self.get_file_path()

        # Create a Fernet object with a generated key
        key = Fernet.generate_key()
        fernet = Fernet(key)

        # Read the contents of the file
        with open(file_path, "rb") as f:
            data = f.read()

        # Encrypt the data
        encrypted_data = fernet.encrypt(data)

        # Get the file path to save the encrypted file
        save_file_path = self.save_file_path()

        # Write the encrypted data to a new file
        with open(save_file_path, "wb") as f:
            f.write(encrypted_data)

        # Write the key to a file
        with open(save_file_path + ".key", "wb") as f:
            f.write(key)

    def decrypt_file(self):
        # Get the file path of the encrypted file
        file_path = self.get_file_path()

        # Get the key for the file
        key_path = filedialog.askopenfilename()
        with open(key_path, "rb") as f:
            key = f.read()

        # Create a Fernet object with the key
        fernet = Fernet(key)

        # Read the encrypted data from the file
        with open(file_path, "rb") as f:
            encrypted_data = f.read()

        # Decrypt the data
        decrypted_data = fernet.decrypt(encrypted_data)

        # Get the file path to save the decrypted file
        save_file_path = self.save_file_path()

        # Write the decrypted data to a new file
        with open(save_file_path, "wb") as f:
            f.write(decrypted_data)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(master=root)
    app.mainloop()
