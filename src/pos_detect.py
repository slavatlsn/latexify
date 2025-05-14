from ultralytics import YOLO
import cv2

model_path = 'PosNet.pt'
detector = YOLO(model_path)


def image(path):
    gray_img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    return cv2.merge([gray_img, gray_img, gray_img])


def data(path):
    padding = 5
    img = image(path)
    result = [map(int, el) for el in detector.predict(img, conf=0.15, device='cpu')[0].boxes.xyxy]
    return [(cv2.threshold(img[el[1]-padding:el[3]+padding, el[0]-padding:el[2]+padding], 190, 255, cv2.THRESH_BINARY)[1], el) for el in map(list, result)]
