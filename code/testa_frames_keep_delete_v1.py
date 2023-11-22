import cv2
import os
from ultralytics import YOLO
import math 
import random

def resize_and_plot_bounding_boxes(image_path, coord_path):
    # Read the image
    image = cv2.imread(image_path)
    # Resize the image to 1200x800
    resized_image = cv2.resize(image, (1200, 800))

    # Read coordinates from the .txt file
    with open(coord_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            _, x_min, y_min, x_max, y_max = map(float, line.strip().split(' '))

            # Scale the coordinates to match the resized image
            scale_x, scale_y = 1200 / image.shape[1], 800 / image.shape[0]
            x_min, x_max = x_min * scale_x, x_max * scale_x
            y_min, y_max = y_min * scale_y, y_max * scale_y

            # Draw rectangle on the resized image
            cv2.rectangle(resized_image, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (0, 255, 0), 2)

    return resized_image

def main():
    directory = "D:/Python/paletizadora/frames/save"
    
    # Loop through the directory
    for filename in sorted(os.listdir(directory)):
        if filename.endswith(".jpg"):
            image_path = os.path.join(directory, filename)
            coord_path = image_path.replace('.jpg', '.txt')

            # Resize the image and plot bounding boxes
            image = resize_and_plot_bounding_boxes(image_path, coord_path)

            # Display the image
            cv2.imshow('Resized Image with Bounding Box', image)
            cv2.waitKey(500)  # Display each image for 0.5 seconds

            # Optionally save the image
            # cv2.imwrite(os.path.join(directory, 'output', filename), image)

            # Break the loop with a key press (optional)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cv2.destroyAllWindows()

def main():
    directory = "D:/Python/paletizadora/frames/save"
    
    # Loop through the directory
    for filename in sorted(os.listdir(directory)):
        if filename.endswith(".jpg"):
            image_path = os.path.join(directory, filename)
            coord_path = image_path.replace('.jpg', '.txt')

            # Resize the image and plot bounding boxes
            image = resize_and_plot_bounding_boxes(image_path, coord_path)

            # Display the image
            cv2.imshow('Resized Image with Bounding Box', image)
            key = cv2.waitKey(0)  # Wait indefinitely for a key press

            if key == ord('d'):  # If 'd' is pressed, delete the frame
                os.remove(image_path)
                os.remove(coord_path)
                print(f"Deleted {image_path} and {coord_path}")
            elif key == ord('k'):  # If 'k' is pressed, keep the frame
                print(f"Kept {image_path} and {coord_path}")

            # Break the loop with a key press (optional)
            if key == ord('q'):
                break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
