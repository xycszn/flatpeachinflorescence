import warnings
warnings.filterwarnings('ignore')
from ultralytics import YOLO
import torch
if __name__ == '__main__':
    model = YOLO('ultralytics/cfg/models/v8/yolov8l.yaml')
    model.load('yolov8l.pt') # loading pretrain weights
    # torch.cuda.empty_cache()
    model.train(data='F:/YOLOv8/ultralytics-main/datasets/mydata.yaml',
                cache=True,
                imgsz=640,
                epochs=200,
                batch=16,
                close_mosaic=0,
                workers=8,
                device='0',
                optimizer='SGD', # using SGD
                # patience=0, # close earlystop
                # resume='', # last.pt path
                # amp=False, # close amp
                # fraction=0.2,
                project='runs/train',
                name='exp',
                )