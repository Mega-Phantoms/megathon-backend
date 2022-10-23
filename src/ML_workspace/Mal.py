import requests
import random
from PIL import Image
import requests
from keras.models import load_model
from io import BytesIO
from keras.preprocessing import image
import tensorflow as tf
import cv2
import numpy as np


class Mal(object):
    def __init__(self, ImgID: str) -> None:
        self.ImgID = ImgID
        self.IMURL = f"https://storage.jayendramadara.repl.co/download?id={self.ImgID}"
        self.Model = rf"src\ML_workspace\hFILES\Covid_XRay_model.h5"

    def Predict(self):
        """
        """
        d = ['false', 'true']
        extension = self.IMURL.split(".")[-1]
        response = requests.get(self.IMURL)
        if response.status_code == 200:
            with open(rf"src\ML_workspace\ZDownloadIMGS\sample.{extension}", 'wb') as f:
                f.write(response.content)

        model = load_model(self.Model)
        img_path = rf"src\ML_workspace\ZDownloadIMGS\sample.{extension}"
        img = cv2.imread(img_path)
        try:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            resized = cv2.resize(gray, (100, 100))
            print(resized.shape)

            data = np.array(resized)/255.0
            data = np.reshape(data, (1, 100, 100, 1))
            ans = (model.predict(data))
            return d[np.argmax(ans)]
        except Exception as e:
            print('Exception:', e)
            return "error"

    def __repr__(self) -> str:
        return "True"
