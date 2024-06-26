# Image Cartoonizer

This project is a simple GUI application for cartoonizing images using Python, OpenCV, and Tkinter. The application allows users to upload an image and apply a cartoon effect to it.

## Features

- **Upload Image:** Users can upload an image from their file system.
- **Cartoonize Image:** Users can apply a cartoon effect to the uploaded image.
- **Image Display:** The original and cartoonized images are displayed in the application window.

## Requirements

- Python 3.x
- Tkinter
- OpenCV
- NumPy
- scikit-learn
- Pillow

The cartoonization process in this project involves several steps using image processing techniques:

* Edge Detection: Convert to grayscale and apply adaptive threshold.
* Bilateral Filtering: Smooth colors and reduce noise.
* Combining Edges and Filtered Image: Bitwise AND operation.
* Color Quantization: Reduce colors, apply K-Means clustering and replace colors with centroids.
