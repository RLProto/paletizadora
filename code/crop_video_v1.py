import cv2

def crop_video(video_path, output_path, crop_percent):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Get the original video resolution
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Define the crop parameters
    x_crop = int(width * crop_percent)
    y_crop = 0
    new_width = width - x_crop
    new_height = height

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (new_width, new_height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Crop the frame
        cropped_frame = frame[y_crop:y_crop+new_height, x_crop:x_crop+new_width]

        # Write the cropped frame
        out.write(cropped_frame)

    # Release everything when job is finished
    cap.release()
    out.release()
    cv2.destroyAllWindows()

video_path = "D:/Python/paletizadora/videos/7.mp4"
output_path = "D:/Python/paletizadora/videos/7_cropped.mp4"
crop_percent = 0.15  # 15% of the left part

crop_video(video_path, output_path, crop_percent)
