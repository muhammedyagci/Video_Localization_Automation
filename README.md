
# Image and Text Overlay on Video Project

This project performs the process of detecting green areas in video frames and overlaying images on these areas while also adding text to the video. The main goal of the project is to effectively place visuals and texts around a specific green area.

## Table of Contents

- [Project Overview](#project-overview)
- [Requirements](#requirements)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Detailed Steps](#detailed-steps)
  - [Green Area Detection](#green-area-detection)
  - [Image Cropping and Resizing](#image-cropping-and-resizing)
  - [Adding Image to Green Area](#adding-image-to-green-area)
  - [Applying the Mask to the Visual](#applying-the-mask-to-the-visual)
  - [Adding Text](#adding-text)
  - [Video Processing](#video-processing)
- [Outputs](#outputs)
- [Notes](#notes)
- [Troubleshooting](#troubleshooting)

## Project Overview

This Python project executes the following steps to add visuals and text to video frames:
1. Detects green areas in the video.
2. Adds visuals to the detected green areas.
3. Adds titles (texts) obtained from an Excel file to the video frames.
4. Saves the output after processing each frame.

### Techniques Used

1. **Green Area Detection**:
   - The project uses OpenCV to detect green areas in the video frames. The hue, saturation, and value (HSV) color space is utilized to set the lower and upper limits for a specific shade of green.
   - A green area mask is created using the `cv2.inRange()` function. Values of 255 (white) represent the green areas, while 0 (black) represents other areas.
   - Contours are detected, and the coordinates of the largest green area are determined.

2. **Image Cropping and Resizing**:
   - The images to be loaded are cropped into a square shape from the center. This means taking a square from the center of the visual.
   - The size of the image is adjusted proportionally based on the distance between the farthest two points of the green area (for example, 12 cm). This ensures the aspect ratio of the visual is maintained while resizing.

3. **Adding Image to Green Area**:
   - The visual is aligned using the mask of the detected green area. It is placed on the left side of the mask to perfectly fit over the green area.
   - This process ensures the visual is placed correctly without leaving any gaps in the background.

4. **Applying the Mask to the Visual**:
   - The green area mask is then used to assemble the pieces like a puzzle. This means that using the mask of the detected green area, the pieces of the visual are placed over the corresponding areas.
   - This ensures that the visual is only visible in the regions where the green area is located, and the rest of the areas are either made transparent using the alpha channel or cropped.

5. **Adding Text**:
   - Titles read from the Excel file are added to the video frames using the Pillow library. The text is centered and placed appropriately at the top of the frames.
   - A suitable font and type are set to ensure the text has a proper appearance.

6. **Video Processing**:
   - The above steps are applied to each frame. Once the process is completed, a new video file is created for output.
   - Separate video files are created for each visual and saved in the `output_videos/` folder.

## Requirements

The following tools and libraries are required for the project to run:
- Python 3.x
- OpenCV
- NumPy
- Pandas
- MoviePy
- Pillow (with pillow-avif for AVIF format support)
- FFmpeg (required by MoviePy for video encoding/decoding)

### Python Libraries

Required Python libraries for the project:
- `opencv-python`
- `numpy`
- `pandas`
- `moviepy`
- `pillow`
- `pillow-avif`

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install the required Python packages:**
   ```bash
   pip install opencv-python numpy pandas moviepy pillow pillow-avif
   ```

3. **Install FFmpeg:**
   - FFmpeg is required for video encoding. You can install it using your package manager or download it from [FFmpeg's official website](https://ffmpeg.org/download.html).

   For example, on Ubuntu:
   ```bash
   sudo apt-get install ffmpeg
   ```

4. **Ensure the paths to images and video files are set correctly in the script.**

## Project Structure

```bash
├── video.mp4                # Input video file
├── texts.xlsx               # Excel file containing titles
├── images/                  # Folder containing the overlay images
│   ├── image1.jpeg
│   ├── image2.png
│   └── ...
├── output_videos/           # Folder for the output videos
├── video_localization.py     # Main Python script
└── README.md                # This README file
```

## Usage

To run the project, follow these steps:

1. **Prepare the video file:**
   - Ensure your video file is named `video.mp4` and is placed in the project directory (or update the path in the script).

2. **Prepare the image files:**
   - Place your images in the `images/` folder.
   - Supported image formats are `.jpeg`, `.jpg`, `.png`, `.webp`, and `.avif`.

3. **Prepare the text file:**
   - Ensure your text file is named `texts.xlsx` and placed in the project directory. The first column of this Excel file should contain the text or titles you want to overlay on the video frames.

4. **Run the script:**
   ```bash
   python video_localization.py
   ```

5. **Check the output:**
   - Processed videos will be saved in the `output_videos/` folder, with filenames indicating the titles and images used for each video.

## Outputs

- Each output video will be saved in the `output_videos/` folder.
- The filenames will follow the pattern: `localized_{i}_{title}.mp4`, where `{i}` is the index of the image and `{title}` is the associated text/title from the Excel file.

## Notes

- **Green area detection**: The green area must be clearly visible and distinct from other elements in the video to be detected properly. Adjust the HSV ranges in the `detect_green_area_and_mask()` function if necessary.
- **Text formatting**: The text is formatted to fit within the frame, but long text may wrap over multiple lines. Ensure that your text entries are reasonably short to avoid cluttering the video.
- **FFmpeg**: Ensure FFmpeg is installed and properly configured on your system. If you encounter issues with video encoding, verify that FFmpeg is available by running `ffmpeg -version` in your terminal.

## Troubleshooting

- **Image not loading**: Ensure the image files are correctly named and located in the `images/` folder. The script currently supports `.jpeg`, `.jpg`, `.png`, `.webp`, and `.avif` formats.
- **FFmpeg issues**: Ensure FFmpeg is installed and properly configured on your system. If you encounter issues with video encoding, verify that FFmpeg is available by running `ffmpeg -version` in your terminal.
- **Green area not detected**: If the green area is not being detected correctly, try adjusting the HSV bounds for the green color in the `detect_green_area_and_mask()` function.
