import os, shutil
from sklearn.model_selection import train_test_split

val_size = 0.1
test_size = 0.2
postfix = 'jpg'
imgpath = 'F:/YOLOv8/ultralytics-main/datasets/peachflower/VOCdevkit/images'
txtpath = 'F:/YOLOv8/ultralytics-main/datasets/peachflower/VOCdevkit/txt'

os.makedirs('F:/YOLOv8/ultralytics-main/datasets/peachflower/images/train2017', exist_ok=True)
os.makedirs('F:/YOLOv8/ultralytics-main/datasets/peachflower/images/val2017', exist_ok=True)
os.makedirs('F:/YOLOv8/ultralytics-main/datasets/peachflower/images/test2017', exist_ok=True)
os.makedirs('F:/YOLOv8/ultralytics-main/datasets/peachflower/labels/train2017', exist_ok=True)
os.makedirs('F:/YOLOv8/ultralytics-main/datasets/peachflower/labels/val2017', exist_ok=True)
os.makedirs('F:/YOLOv8/ultralytics-main/datasets/peachflower/labels/test2017', exist_ok=True)

listdir = os.listdir(txtpath)
train, test = train_test_split(listdir, test_size=test_size, shuffle=True, random_state=0)
train, val = train_test_split(train, test_size=val_size, shuffle=True, random_state=0)

for i in train:
    shutil.copy('{}/{}.{}'.format(imgpath, i[:-4], postfix), 'images/train2017/{}.{}'.format(i[:-4], postfix))
    shutil.copy('{}/{}'.format(txtpath, i), 'labels/train2017/{}'.format(i))

for i in val:
    shutil.copy('{}/{}.{}'.format(imgpath, i[:-4], postfix), 'images/val2017/{}.{}'.format(i[:-4], postfix))
    shutil.copy('{}/{}'.format(txtpath, i), 'labels/val2017/{}'.format(i))

for i in test:
    shutil.copy('{}/{}.{}'.format(imgpath, i[:-4], postfix), 'images/test2017/{}.{}'.format(i[:-4], postfix))
    shutil.copy('{}/{}'.format(txtpath, i), 'labels/test2017/{}'.format(i))