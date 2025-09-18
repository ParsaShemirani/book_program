import os
import shutil

# --- Variables (set these paths) ---
input_folder = r"/Users/parsashemirani/Main/b2_nvc/originals"
output_folder = r"/Users/parsashemirani/Main/b2_nvc/numbered"
# -----------------------------------

def rename_and_copy_images(input_folder, output_folder):
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Get all .jpg files and sort them by name
    jpg_files = sorted([f for f in os.listdir(input_folder) if f.lower().endswith(".jpg")])

    # Rename and copy
    for i, filename in enumerate(jpg_files, start=1):
        old_path = os.path.join(input_folder, filename)
        new_filename = f"{i}.jpg"
        new_path = os.path.join(output_folder, new_filename)

        shutil.copy2(old_path, new_path)  # copy with metadata preserved
        print(f"Copied {filename} -> {new_filename}")

if __name__ == "__main__":
    rename_and_copy_images(input_folder, output_folder)
