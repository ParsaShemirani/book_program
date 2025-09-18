import os
from PIL import Image

# Input and output folders
input_folder = "/Users/parsashemirani/Main/b2_nvc/numbered"
output_folder = "/Users/parsashemirani/Main/b2_nvc/number_rotate"

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Collect only image files and sort numerically (e.g., 1.jpg, 2.jpg, ...)
image_files = [
    f for f in os.listdir(input_folder)
    if os.path.isfile(os.path.join(input_folder, f)) 
    and f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".gif"))
]

# Sort based on the number before the extension
image_files.sort(key=lambda x: int(os.path.splitext(x)[0]))

# Loop through sorted files
for filename in image_files:
    input_path = os.path.join(input_folder, filename)
    try:
        # Open the image
        img = Image.open(input_path)

        # Rotate 90 degrees clockwise
        rotated_img = img.rotate(-90, expand=True)

        # Save to output folder with same filename
        output_path = os.path.join(output_folder, filename)
        rotated_img.save(output_path)

        print(f"Rotated and saved: {output_path}")
    except Exception as e:
        print(f"Skipping {filename} due to error: {e}")
