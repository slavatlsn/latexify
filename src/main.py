from ultralytics import YOLO
import cv2
import numpy as np
import os

model = YOLO('yolov8n_custom.pt')
classes_names = []

def get_expr(image_path):
    image = cv2.imread(image_path)
    results = model(image)[0]
    image = results.orig_img
    classes_names = results.names
    classes = results.boxes.cls.cpu().numpy()
    boxes = results.boxes.xyxy.cpu().numpy().astype(np.int32)
    syms = set()
    for class_id, box in zip(classes, boxes):
        c_id = int(class_id)
        x1, y1, x2, y2 = box
        sym = image[x1:x2, y1:y2]
        #классификация символа с помощью классификатора
        #ансамблирование результатов классификации в fin_class_id
        syms.add((box, fin_class_id))
    return syms
