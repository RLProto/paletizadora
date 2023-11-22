from ultralytics import YOLO
import cv2
import math 
import random

# model
model = YOLO("best.pt")

# object classes
classNames = ["colaborador", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"
              ]


# Generate random colors for each class
class_colors = {}
for i in range(len(classNames)):
    class_colors[i] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

video_directory = f"D:\\Python\\paletizadora\\videos\\originais\\1.mp4"
cap = cv2.VideoCapture(video_directory)

frame_count = 0  # Initialize a frame counter variable

while True:
    success, img = cap.read()
    
    if not success:  # Break if the video has ended
        break

    frame_count += 1  # Increment the frame counter

    if frame_count % 3 == 0:  # Process every 4th frame (i.e., skip 3 frames)
        
        img = cv2.resize(img, (1900, 1000))
        results = model(img, stream=True)

        for r in results:
            boxes = r.boxes

            for box in boxes:
                # Get the bounding box
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                # Confidence
                confidence = math.ceil((box.conf[0] * 100)) / 100
                print("Confidence --->", confidence)

                # Class name
                cls = int(box.cls[0])
                print("Class name -->", classNames[cls])

                # Object details
                org = [x1, y1]
                font = cv2.FONT_HERSHEY_SIMPLEX
                fontScale = 1
                color = class_colors[cls]
                thickness = 2

                if(cls==0):
                    # Prepare the score text
                    score_text = "colaborador: "+str(round(confidence, 2))
                    
                    # Calculate the width of the text
                    (text_width, text_height), _ = cv2.getTextSize(score_text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)

                    # Create a rectangle with red color for the text background
                    cv2.rectangle(img, (int(x1) -3, int(y2)), (int(x1) + text_width + 10, int(y2) + text_height + 10), (0, 0, 255), -1)
                    
                    cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 6)

                    # Put text on the rectangle, change the text color to white (255,255,255)
                    cv2.putText(img, score_text, (int(x1) + 5, int(y2) + text_height + 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        img = cv2.resize(img, (1200, 800))  # You can adjust the resolution as needed
        # Show the image
        cv2.imshow('video', img)
        if cv2.waitKey(1) == ord('q'):
            break

# Release the webcam and destroy all windows
cap.release()
cv2.destroyAllWindows()