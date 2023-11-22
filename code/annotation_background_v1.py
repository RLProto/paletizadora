import cv2
import os

videos_folder = r"D:\Python\paletizadora\videos\background"
save_path = r"D:\Python\paletizadora\frames\background"

if not os.path.exists(save_path):
    os.makedirs(save_path)

video_files = [f for f in os.listdir(videos_folder) if f.endswith(".mp4")]

for video_file in video_files:
    video_path = os.path.join(videos_folder, video_file)
    cap = cv2.VideoCapture(video_path)

    # Get the frame rate and frame count
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Calculate video duration in seconds
    duration = frame_count / fps
    
    # Determine the frame interval based on the video duration
    if duration < 30:
        save_frame_interval = 8  # Save 1 frame and skip 2
    else:
        save_frame_interval = 60  # Save 1 frame and skip 5
    
    frame_id = 0
    frame_count_since_last_save = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        if frame_count_since_last_save >= save_frame_interval:
            cv2.imwrite(os.path.join(save_path, f"{video_file}_frame_{frame_id}.jpg"), frame)
            frame_count_since_last_save = 0
        else:
            frame_count_since_last_save += 1

        frame_id += 1

    cap.release()
