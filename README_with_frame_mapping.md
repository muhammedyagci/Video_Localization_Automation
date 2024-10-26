
# Video Frame Processing with Titles and Image Overlays

This project processes video frames by adding images and dynamically applying titles, resizing, and positioning based on a mapping file. The main goal is to overlay images at specific positions on each frame of the video, accompanied by text (titles) placed on the video using a custom-defined font. The project supports multiple image formats, including AVIF, JPEG, PNG, WebP, and more.

## Features

1. **Dynamic Frame Processing:**  
   Each frame of the video is processed individually. Images are overlaid based on frame-specific position and zoom data. Titles are added to each video, ensuring the text is aligned and split into lines if necessary.
   
2. **Support for Multiple Image Formats:**  
   The project supports various image formats, including AVIF, JPEG, PNG, and WebP. It uses `pillow-avif-plugin` for AVIF support.

3. **Zoom and Position Mapping:**  
   The project reads a mapping file (`frame_mappings.txt`), which contains information on zoom and position offsets for each frame of the video. If no mapping data is found for a frame, default values are used. **This frame mapping was generated using the "Frame Mapping" program, which can also be used to create new mapping files.**

4. **Title Insertion with Text Wrapping:**  
   Titles are added to the video, and long text is split into multiple lines based on a maximum width. The titles are placed at the top of the frame and centered horizontally.

5. **Green Screen Masking:**  
   Any green areas in the video are automatically masked, and the overlaid image is placed behind those areas.

---

## Requirements

1. **Python Libraries:**
   - OpenCV (`cv2`)
   - NumPy (`numpy`)
   - Pandas (`pandas`)
   - MoviePy (`moviepy`)
   - Pillow (`PIL`, including `pillow-avif-plugin` for AVIF support)

2. **Required Files:**
   - `video.mp4`: The video file to be processed.
   - `texts.xlsx`: A file containing titles for each video segment (Excel format).
   - `frame_mappings.txt`: A CSV file with frame number, zoom factor, and positional offsets for image overlay.
   - Images: A folder containing images (`.jpeg`, `.png`, `.webp`, `.avif`, etc.) to be overlaid on the video.

3. **Directory Structure:**
   - `./images/`: Folder containing images to be overlaid.
   - `./output_videos/`: Folder where the processed videos will be saved.

---

## Explanation of Mapping File (`frame_mappings.txt`)

Each line in the `frame_mappings.txt` file corresponds to a frame in the video and includes the following fields:

```
<frame_number>,<zoom_factor>,<x_offset>,<y_offset>
```

- **frame_number:**  
  The specific frame in the video.
  
- **zoom_factor:**  
  Controls the size of the image overlay. A value of `1.0` means the image retains its original size, while greater values enlarge the image, and smaller values shrink it.

- **x_offset:**  
  Horizontal offset from the left edge of the frame for positioning the image.

- **y_offset:**  
  Vertical offset from the top of the frame for positioning the image.

---

## Usage Steps

#### Step 1: Setup Environment
- Ensure all required Python libraries are installed:
  ```bash
  pip install opencv-python-headless numpy pandas moviepy pillow pillow-avif-plugin
  ```

#### Step 2: Prepare Files
- Place your `video.mp4` file in the project directory.
- Create a `texts.xlsx` file containing titles for each segment of the video (one title per row).
- Prepare the `frame_mappings.txt` file containing the zoom and position information for the video frames.
- Place your images in the `./images/` folder.

#### Step 3: Run the Script
- Execute the script to process the video and generate new videos with overlaid images and titles:
  ```bash
  python video_processing_script.py
  ```

#### Step 4: Output Videos
- The processed videos will be saved in the `./output_videos/` folder with the naming convention `localized_<index>_<title>.mp4`.

---

## Example Mapping File

```
1,1.0,320,872
2,1.05,325,875
10,1.2,350,890
```

## Example of Titles (Excel File)

| Titles        |
|---------------|
| Welcome to the Presentation |
| Video Processing Example    |
| End of the Presentation     |

---

## Key Functions

1. **load_image(image_path):**  
   This function loads images from various formats, including `.avif`, `.jpeg`, `.png`, and `.webp`.

2. **add_text_with_pillow(frame, title_text, font_path="arialbd.ttf", font_size=80, max_width=1000):**  
   Adds the specified text to the video frame using Pillow, handling text wrapping and alignment.

3. **process_frame(frame, frame_number, overlay_image, title_text):**  
   Processes each frame of the video by applying the image overlay and adding titles.

4. **Video Generation Loop:**  
   Iterates through the list of images and titles, processing the video frame-by-frame, and saving the resulting videos in sequence.

---

## Known Limitations

1. **Green Screen Detection:**  
   The mask for detecting the green areas might need adjustments depending on the video's lighting and green screen quality.

2. **Performance:**  
   Processing high-resolution videos with many frames can be resource-intensive. Consider optimizing the code or using lower-resolution videos for faster processing.

---

This project enables the efficient creation of localized video content with custom images and text overlays, supporting a wide range of image formats and offering flexibility in zoom and positioning.
