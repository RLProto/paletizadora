import os
import shutil
import random
from PIL import Image

# Get the dimensions of your images
image_width = 1920
image_height = 1080

#image_width = 2688
#image_height = 1520

#image_width = 960
#image_height = 540


# Define the source directory and target directories
src_dir = r"D:\Python\paletizadora\frames\save\selected"
train_images_dir = r"D:\Python\paletizadora\frames\save2\train\images"
train_labels_dir = r"D:\Python\paletizadora\frames\save2\train\labels"
val_images_dir = r"D:\Python\paletizadora\frames\save2\valid\images"
val_labels_dir = r"D:\Python\paletizadora\frames\save2\valid\labels"
non_used_images_dir = r"D:\Python\paletizadora\frames\save2\not_used\images"
non_used_labels_dir = r"D:\Python\paletizadora\frames\save2\not_used\labels"

# Create the target directories if they don't exist
os.makedirs(train_images_dir, exist_ok=True)
os.makedirs(train_labels_dir, exist_ok=True)
os.makedirs(val_images_dir, exist_ok=True)
os.makedirs(val_labels_dir, exist_ok=True)
os.makedirs(non_used_images_dir, exist_ok=True)
os.makedirs(non_used_labels_dir, exist_ok=True)

# Get the list of all files in source directory
src_files = [f for f in os.listdir(src_dir) if f.endswith('.jpg')]

# Shuffle the list
random.shuffle(src_files)

# Split the list into 40/15/45 proportion
split_idx1 = int(0.1 * len(src_files))
split_idx2 = int(0.13 * len(src_files))  # 0.50 + 0.12 = 0.52
train_files = src_files[:split_idx1]
val_files = src_files[split_idx1:split_idx2]
non_used_files = src_files[split_idx2:]

def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[2])/2.0
    y = (box[1] + box[3])/2.0
    w = box[2] - box[0]
    h = box[3] - box[1]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)


def normalize_and_copy_label(file_name, img_file_name, dest_dir):
    with open(file_name, 'r') as f:
        lines = f.readlines()

    im = Image.open(img_file_name)
    size = im.size  # size[0] = width, size[1] = height

    new_lines = []
    for line in lines:
        elements = line.split()
        try:
            # Assuming your label files are in format: class xmin xmax ymin ymax
            box = (float(elements[1]), float(elements[2]), float(elements[3]), float(elements[4]))
            (x, y, w, h) = convert(size, box)
            elements[1:] = [str(x), str(y), str(w), str(h)]
        except IndexError:
            print(f"Error in file {file_name} on line: {line}")
            continue
        new_lines.append(' '.join(elements))
    # Write the normalized labels to new files
    with open(os.path.join(dest_dir, os.path.basename(file_name)), 'w') as f:
        f.write('\n'.join(new_lines))

# Copy and normalize files
for file_name in train_files:
    full_file_name = os.path.join(src_dir, file_name)
    if os.path.isfile(full_file_name):
        shutil.copy(full_file_name, train_images_dir)
        normalize_and_copy_label(full_file_name.replace('.jpg', '.txt'), full_file_name, train_labels_dir)

for file_name in val_files:
    full_file_name = os.path.join(src_dir, file_name)
    if os.path.isfile(full_file_name):
        shutil.copy(full_file_name, val_images_dir)
        normalize_and_copy_label(full_file_name.replace('.jpg', '.txt'), full_file_name, val_labels_dir)

for file_name in non_used_files:
    full_file_name = os.path.join(src_dir, file_name)
    if os.path.isfile(full_file_name):
        shutil.copy(full_file_name, non_used_images_dir)
        normalize_and_copy_label(full_file_name.replace('.jpg', '.txt'), full_file_name, non_used_labels_dir)
