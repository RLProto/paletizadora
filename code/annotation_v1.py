import cv2
from ultralytics import YOLO
import os
import ultralytics
ultralytics.checks()

model = YOLO("yolov8x.pt")

videos_folder = r"D:\Python\paletizadora\videos"
save_path = r"D:\Python\paletizadora\frames\save"
save_frame_interval = 80  # Save every 7 frames

if not os.path.exists(save_path):
    os.makedirs(save_path)

video_files = [f for f in os.listdir(videos_folder) if f.endswith(".mp4")]

for video_file in video_files:
    video_path = os.path.join(videos_folder, video_file)
    cap = cv2.VideoCapture(video_path)

    frame_id = 0
    frame_count_since_last_save = 0

    for result in model.predict(source=video_path, stream=True):
        ret, frame = cap.read()

        if ret:
            boxes = result.boxes.xyxy.cpu().numpy()
            classes = result.boxes.cls.cpu().numpy()
            confs = result.boxes.conf.cpu().numpy()

            print(f"Frame {frame_id} total detections: {len(boxes)}")
            person_boxes = boxes[(classes == 0) & (confs > 0.60)]
            person_scores = confs[(classes == 0) & (confs > 0.60)]
            print(f"Frame {frame_id} 'person' detections: {len(person_boxes)}")

            if len(person_boxes) > 0 and frame_count_since_last_save >= save_frame_interval:
                with open(os.path.join(save_path, f"{video_file}_frame_{frame_id}.txt"), 'w') as f:
                    for b, conf in zip(person_boxes, person_scores):
                        f.write(f'0 {b[0]} {b[1]} {b[2]} {b[3]}\n')
                cv2.imwrite(os.path.join(save_path, f"{video_file}_frame_{frame_id}.jpg"), frame)
                frame_count_since_last_save = 0
            else:
                frame_count_since_last_save += 1

            frame_id += 1

    cap.release()
