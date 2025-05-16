from ultralytics import YOLO
import cv2
from config import my_device, padding

model_path = 'PosNet.pt'
detector = YOLO(model_path)


def image(path):
    gray_img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    return cv2.merge([gray_img, gray_img, gray_img])


def data(path):
    img = image(path)
    d = detector.predict(img, conf=0.15, device=my_device)[0].boxes
    result = [map(int, el) for el in d.xyxy]
    return [(cv2.resize(cv2.threshold(img[el[1]-padding:el[3]+padding, el[0]-padding:el[2]+padding], 190, 255, cv2.THRESH_BINARY)[1], (32, 32), interpolation=cv2.INTER_LINEAR), el) for el in map(list, result)], zip(d.cls, d.conf)
