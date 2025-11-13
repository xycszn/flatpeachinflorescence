import warnings
warnings.filterwarnings('ignore')
from ultralytics import YOLO

if __name__ == '__main__':
    model = YOLO('runs/train/exp13/weights/last.pt') # select your model.pt path
    model.predict(source='datasets/images/keshihuatupian',
                  imgsz=640,
                  project='runs/detect',
                  name='exp',
                  save=True,
                  # conf=0.2,
                  # iou=0.7,
                  # agnostic_nms=True,
                  # visualize=True # visualize model features maps
                )