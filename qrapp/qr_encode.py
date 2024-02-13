import qrcode
import cv2
import os
import numpy as np
from PIL import Image


class Encoder:
    def __init__(self):
        self.id = 0000

    def create_qrcode(self, data):
        self.id = 2367
        new_data = data.split(" ")
        data_x = ""
        for x in new_data:
            data_x += x

        filepath = f"./media/qrcode/{data_x}.png"

        qr_image = qrcode.make(data)
        qr_image.save(filepath)
        return f"/qrcode/{data_x}.png"

    def decode_qr(self, qr_image):
        self.id = 45
        filepath = f".{qr_image}"
        image = cv2.imread(filepath)
        detector = cv2.QRCodeDetector()

        data, vertices_array, binary_qrcode = detector.detectAndDecode(image)

        if vertices_array is not None:
            return data
        else:
            return 4953
