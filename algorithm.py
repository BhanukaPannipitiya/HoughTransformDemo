import numpy as np
from scipy import ndimage
from matplotlib import image as mpimg
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import tkinter as tk  # Add this line

def fast_hough_transform(image, threshold=50):
    edges = ndimage.sobel(image, mode='constant')
    
    # Separate points into two sets based on gradient vector angle
    set1 = edges.copy()
    set2 = edges.copy()
    set1[edges >= 0] = 0
    set2[edges < 0] = 0

    # Create sets of coefficients using different parametrizations
    Cq_set1 = calculate_coefficients(set1)
    Cq_set2 = calculate_coefficients(set2)

    # Apply FHT algorithm to each set
    accumulator_set1 = hough_algorithm(Cq_set1, threshold)
    accumulator_set2 = hough_algorithm(Cq_set2, threshold)

    # Combine results from both sets
    accumulator = accumulator_set1 + accumulator_set2

    accumulator[accumulator < threshold] = 0  # Thresholding to remove weak lines

    return edges, accumulator

def calculate_coefficients(set):
    # Calculate coefficients using the parametrization mentioned in the article
    rows, cols = np.nonzero(set)
    coefficients = np.column_stack((cols, rows, np.ones_like(rows)))
    return coefficients

def hough_algorithm(coefficients, threshold):
    # Initialize accumulator
    height, width = coefficients.shape[:2]
    r_max = int(np.sqrt(height**2 + width**2))
    accumulator = np.zeros((r_max, 180), dtype=int)

    for i in range(height):
        x, y, _ = coefficients[i]
        for theta in range(-90, 90):
            r = int(x * np.cos(np.radians(theta)) + y * np.sin(np.radians(theta)))
            accumulator[r, theta + 90] += 1

    return accumulator

def perform_fast_hough_transform(image_path, threshold=50):
    image = mpimg.imread(image_path)
    grayscale_image = np.mean(image, axis=-1)  # Convert to grayscale

    edges, accumulator = fast_hough_transform(grayscale_image, threshold)

    return edges, accumulator

def perform_hough_transform_ui(canvas, file_path):
    original_image = Image.open(file_path)
    img = ImageTk.PhotoImage(original_image)
    canvas.config(width=img.width(), height=img.height())
    canvas.create_image(0, 0, anchor=tk.NW, image=img)
    canvas.image = img  # To prevent garbage collection

    edges, accumulator = perform_fast_hough_transform(file_path)

    # Display the results using matplotlib (you can customize this part)
    plt.imshow(edges, cmap='gray')
    plt.title('Edge Detection')
    plt.show()

    plt.imshow(accumulator, cmap='gray')
    plt.title('Hough Transform Accumulator')
    plt.show()
