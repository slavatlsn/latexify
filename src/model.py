from ultralytics import YOLO
import os

model = YOLO('yolov8n.pt')

results = model.train(
   data='dataset/dataset.yaml',
   imgsz=640,
   epochs=10,
   batch=8,
   name='yolov8n_custom')