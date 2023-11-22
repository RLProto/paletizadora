import traceback
from ultralytics import YOLO

def train_yolo(config):
    try:
        # Load the model.
        model = YOLO(config['model'])

        # Training.
        results = model.train(
            data='D:/Python/paletizadora/code/path.yaml',
            imgsz=config['imgsz'],
            epochs=config['epochs'],
            batch=7,
            patience=500,
            resume=True,
            name=config['name'],

            
        )
    except Exception as e:
        print(f"An error occurred during training: {str(e)}")
        traceback.print_exc()

if __name__ == '__main__':
    configs = [
        {
            'model': 'last.pt',
            'imgsz': 560,
            'epochs': 2000,
            'name': 'yolov8x_560_7_2000'
        },
    ]

    for config in configs:
        train_yolo(config)
