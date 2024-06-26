import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np
from sklearn.cluster import KMeans

class ImageCartoonizer:

    def __init__(self, master):
        self.master = master
        master.title("Image Cartoonizer")
        master.geometry("800x600")
        master.configure(bg="#E1F5FE") 
        
        self.upload_frame = tk.Frame(master, bg="#E1F5FE")
        self.upload_frame.pack(pady=20)
        
        self.upload_button = tk.Button(self.upload_frame, text="Upload Image", command=self.upload_image, bg="#03A9F4", fg="white", font=("Helvetica", 16, "bold"),
        padx=20, pady=10, relief=tk.RAISED, borderwidth=0,
        highlightthickness=0, activebackground="#0288D1", activeforeground="white")
        self.upload_button.pack()
        
        self.canvas_frame = tk.Frame(master, bg="#E1F5FE")
        self.canvas_frame.pack(pady=20)
        
        self.canvas = tk.Canvas(self.canvas_frame, width=600, height=400, bg="white", highlightthickness=0)
        self.canvas.pack()
        
        self.cartoonize_frame = tk.Frame(master, bg="#E1F5FE")
        self.cartoonize_frame.pack(pady=20)
        
        self.cartoonize_button = tk.Button(self.cartoonize_frame, text="Cartoonize", command=self.cartoonize_image, bg="#4CAF50", fg="white", font=("Helvetica", 16, "bold"), padx=20, pady=10, relief=tk.RAISED, borderwidth=0, highlightthickness=0, activebackground="#388E3C", activeforeground="white")
        self.cartoonize_button.pack()
        self.image_path = "" # Initialize the image path variable
    
    def upload_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if self.image_path:
            image = Image.open(self.image_path)

            # Resize the image to fit the canvas while maintaining aspect ratio
            image = image.resize((600, 400), Image.Resampling.LANCZOS)            
            photo = ImageTk.PhotoImage(image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            self.canvas.image = photo
    
    def cartoonize_image(self):
        if self.image_path:
            input_image = cv2.imread(self.image_path)            
            input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)
            
            height, width = input_image.shape[:2]
            max_size = 600            
            if height > max_size or width > max_size:
                scale = max_size / max(height, width)
                new_height = int(height * scale)
                new_width = int(width * scale)
                input_image = cv2.resize(input_image, (new_width, new_height))
            else:
                new_height = height
                new_width = width
            
            cartoonified_image = self.cartoonify(input_image)            
            cartoon_window = tk.Toplevel(self.master)
            cartoon_window.title("Cartoonized Image")
            
            cartoon_canvas_frame = tk.Frame(cartoon_window)
            cartoon_canvas_frame.pack(pady=20)
            cartoon_canvas = tk.Canvas(cartoon_canvas_frame,
            width=new_width, height=new_height)
            cartoon_canvas.pack()
            
            # Convert the cartoonified image from NumPy array and then to PhotoImage
            cartoonified_image_pil = Image.fromarray(cartoonified_image)
            cartoonified_photo = ImageTk.PhotoImage(cartoonified_image_pil)
            
            cartoon_canvas.create_image(0, 0, anchor=tk.NW, image=cartoonified_photo)
            cartoon_canvas.image = cartoonified_photo
    
    def cartoonify(self, image):
        # Apply edge detection to the input image
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        edges = cv2.adaptiveThreshold(gray, 255,
        cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
        
        # Apply bilateral filtering to reduce noise while preserving edges
        bilateral = cv2.bilateralFilter(image, 9, 75, 75)
        
        # Combine the edge map and the filtered image using bitwise AND operation
        cartoon = cv2.bitwise_and(bilateral, bilateral, mask=edges)
        
        # Perform color quantization using K-Means clustering
        h, w, c = cartoon.shape
        cartoon2d = cartoon.reshape(-1, 3)
        
        # Perform K-Means clustering with a specified number of colors
        n_colors = 16
        kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init=10)
        kmeans.fit(cartoon2d)
        cartoon_quantized = kmeans.cluster_centers_[kmeans.labels_]
        
        # Reshape the quantized image back to its original shape
        cartoon_quantized = np.uint8(cartoon_quantized).reshape(h, w, c)
        return cartoon_quantized

root = tk.Tk()
cartoonizer = ImageCartoonizer(root)
root.mainloop()