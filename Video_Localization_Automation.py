import cv2
import numpy as np
import os
import pandas as pd
from moviepy.editor import VideoFileClip
from PIL import Image, ImageDraw, ImageFont
import pillow_avif  # For AVIF support

# Path to the video file
video_path = 'video.mp4'

# Load the file containing the titles (Excel or CSV)
titles_file = 'texts.xlsx'  # Excel file
titles_df = pd.read_excel(titles_file)  # Read titles from Excel
titles_list = titles_df.iloc[:, 0].tolist()  # Take the first column as a list of titles

# Folder containing the images
images_folder = './images/'  # Folder containing images
images_list = [os.path.join(images_folder, img) for img in os.listdir(images_folder) if img.endswith(('.jpeg', '.jpg', '.png', '.webp', '.avif'))]

output_dir = './output_videos/'  # Output directory
os.makedirs(output_dir, exist_ok=True)  # Create the output directory if it doesn't exist

# Set font size and position for the text
font_size = 80  # Large font size for the text
text_position_y = 100  # Starting Y position for the top of the text

# Function to detect green area and mask
def detect_green_area_and_mask(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # Convert the frame to HSV format
    lower_green = np.array([50, 100, 100])  # Lower bound for green color
    upper_green = np.array([70, 255, 255])  # Upper bound for green color
    mask = cv2.inRange(hsv, lower_green, upper_green)  # Create a mask for green area

    # Find contours (to detect the boundaries of the green area)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        # Get the largest green area
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)  # Bounding rectangle
        longest_side = max(w, h)  # Calculate the longest side
        return x, y, w, h, longest_side, mask
    return None, None, None, None, None, None  # Return None if no green area is found

# Function to crop the image as a square
def crop_image_as_square(image):
    height, width = image.shape[:2]
    smallest_side = min(height, width)

    # Crop the image as a square from the center
    start_x = (width - smallest_side) // 2
    start_y = (height - smallest_side) // 2
    square_image = image[start_y:start_y + smallest_side, start_x:start_x + smallest_side]

    return square_image

# Function to add an image to the green area while aligning and cropping using the mask
def add_image_to_green_area(frame, image, x, y, w, h, longest_side, mask):
    # Crop the image as a square
    image = crop_image_as_square(image)

    # Resize the image based on the longest side (while preserving the aspect ratio)
    aspect_ratio = image.shape[1] / image.shape[0]
    new_width = longest_side
    new_height = int(new_width / aspect_ratio)
    
    resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
    
    # Clear the green area
    frame[mask > 0] = (0, 0, 0)  # Clear the green area by making it black

    # Align the image according to the mask and place it on the left of the green area
    x_offset = x  # Full alignment to the left
    y_offset = y + (h - new_height) // 2  # Center alignment on the Y axis
    
    # Apply the image to the green area
    for c in range(0, 3):  # Color channels (BGR)
        frame[y_offset:y_offset + new_height, x_offset:x_offset + new_width, c] = \
            resized_image[:, :, c] * (mask[y_offset:y_offset + new_height, x_offset:x_offset + new_width] / 255) + \
            frame[y_offset:y_offset + new_height, x_offset:x_offset + new_width, c] * (1 - (mask[y_offset:y_offset + new_height, x_offset:x_offset + new_width] / 255))
    
    return frame

# Function to load an image with Pillow (instead of cv2.imread)
def load_image(image_path):
    try:
        img = Image.open(image_path)
        return np.array(img.convert("RGB"))  # Convert to a numpy array for OpenCV compatibility
    except Exception as e:
        print(f"Error loading image {image_path}: {e}")
        return None

# Function to add text using Pillow (with proper alignment and font size for video)
def add_text_with_pillow(frame, title_text, font_path="arialbd.ttf", font_size=80, max_width=1000):
    # Convert the OpenCV image to a PIL image
    pil_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)

    # Load the font (bold font arialbd.ttf)
    font = ImageFont.truetype(font_path, font_size)

    # Split the text into lines by separating words
    words = title_text.split(' ')
    lines = []
    current_line = ""

    # Add each word and check the line width
    for word in words:
        test_line = current_line + " " + word if current_line else word
        bbox = draw.textbbox((0, 0), test_line, font=font)
        width = bbox[2] - bbox[0]  # Width

        if width > max_width:
            lines.append(current_line)
            current_line = word
        else:
            current_line = test_line

    if current_line:
        lines.append(current_line)

    y_offset = 200  # Starting Y position for the first line
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        position = ((frame.shape[1] - text_width) // 2, y_offset)  # Centered and at the top
        draw.text(position, line, font=font, fill="white", stroke_width=3, stroke_fill="black")
        y_offset += bbox[3] - bbox[1] + 10

    return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

# Function to process each frame and add image and text
def process_frame(frame, frame_number, overlay_image, title_text):
    frame_copy = frame.copy()
    x, y, w, h, longest_side, mask = detect_green_area_and_mask(frame_copy)

    if mask is not None:
        frame_copy = add_image_to_green_area(frame_copy, overlay_image, x, y, w, h, longest_side, mask)

    frame_copy = add_text_with_pillow(frame_copy, title_text)
    return frame_copy

# Process video frames, add images and titles
for i, image_path in enumerate(images_list):
    title_text = titles_list[i % len(titles_list)]
    
    # Load image with Pillow
    overlay_image = load_image(image_path)
    if overlay_image is None:
        print(f"Skipping frame {i+1}: Could not load image {image_path}")
        continue  # Skip this frame if the image could not be loaded
    
    clip = VideoFileClip(video_path)
    
    processed_clip = clip.fl_image(lambda gf: process_frame(gf, i, overlay_image, title_text))
    
    output_path = f"{output_dir}localized_{i+1}_{title_text.replace(' ', '_')}.mp4"
    processed_clip.write_videofile(output_path, codec='libx264', fps=clip.fps)

    print(f"Video created: {output_path}")

print("All videos created successfully!")
