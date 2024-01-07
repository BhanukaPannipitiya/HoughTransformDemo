import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from algorithm import perform_hough_transform_ui


def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
    if file_path:
        load_and_display_image(file_path)

def load_and_display_image(file_path):
    perform_hough_transform_ui(canvas, file_path)

root = tk.Tk()
root.title("Hough Transform Demo")

canvas = tk.Canvas(root)
canvas.pack()

open_button = tk.Button(root, text="Open Image", command=open_file)
open_button.pack()

root.mainloop()
