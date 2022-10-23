from PIL import Image
import requests
from keras.models import load_model
from io import BytesIO
from keras.preprocessing import image
import tensorflow as tf
import cv2
import numpy as np
path = r"C:\tai_jutsu\megathon\megathon-backend\src\hFILES\Covid_XRay_model.h5"

d = ['true', 'false']
# response = requests.get('https://storage.jayendramadara.repl.co/download?id=0d6b6b82-aaf8-4433-98eb-fceb09e7c569')
# img = Image.open(r"C:\\Users\GVM SRAVAN KUMAR\OneDrive\Desktop\wong-0005.jpg")
# model=load_model(path)
# i=np.array(img)/255.0
# i=i.reshape(100,100,3)
# print(i.shape)
# # p=model.predict(i)
# # print(d[p[0]])
img_path = r"C:\Users\jayendra\Downloads\sravan.jpeg"
# cv2.cvtColor()
img = cv2.imread(img_path)

try:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Coverting the image into gray scale
    resized = cv2.resize(gray, (100, 100))
    # resizing the gray scale into 100x100, since we need a fixed common size for all the images in the dataset
    # appending the image and the label(categorized) into the list (dataset)
    print(resized.shape)
except Exception as e:
    print('Exception:', e)
