import cv2
import numpy as np
from .builder import Rsa,Scale
from PIL import Image
from PIL import ImageTk
from collections import namedtuple
from math import fabs

Picture = namedtuple('Picture' , 'title image display')

class Db_pictures():

    def __init__(self,rsa,img,algorithm):
        self.rsa = rsa
        self.img = img.astype(np.float64)
        self.algorithm = algorithm

    def create_pictures(self):
        self.algorithm.img = self.img
        self.code = self.algorithm.code()

        self.algorithm.img = self.code
        self.decode = self.algorithm.decode()

        self.algorithm.scale = Scale(max=max([max(i) for i in self.code]),min=min([min(i) for i in self.code]))
        self.transfer = self.algorithm.transfer()

        self.algorithm.img = self.transfer
        self.back_transfer = self.algorithm.back_transfer()

        self.algorithm.img = self.back_transfer
        self.decode_back_transfer = self.algorithm.decode()

    def preparation_for_display(self):
        title_pictures = ["початкове","закодоване","декодоване","закодоване, шкала -> 0-255","закодоване, 0-255 -> шкала","декодоване з зміною шкали"]
        images = [self.img,self.code,self.decode,self.transfer,self.back_transfer,self.decode_back_transfer]
        self.pictures = [Picture(title=title, image=image, display=ImageTk.PhotoImage(Image.fromarray(image.astype(np.uint8)))) for title,image in zip(title_pictures,images)]

    def delta(self):
        base_int = self.img.astype(np.uint8)
        decode_int = self.decode.astype(np.uint8)
        decode_back_transfer_int = self.decode_back_transfer.astype(np.uint8)

        delta_back_decode_fl = np.zeros((self.algorithm.height, self.algorithm.width), dtype=np.float64)
        delta_decode_fl = np.zeros((self.algorithm.height, self.algorithm.width), dtype=np.float64)
        delta_back_decode_int = np.zeros((self.algorithm.height, self.algorithm.width), dtype=np.uint8)
        delta_decode_int = np.zeros((self.algorithm.height, self.algorithm.width), dtype=np.uint8)

        for i in range(self.algorithm.height):
            for j in range(self.algorithm.width):
                delta_back_decode_fl[i][j] = fabs(self.decode_back_transfer[i][j] - self.img[i][j])
                delta_decode_fl[i][j] = fabs(self.decode[i][j] - self.img[i][j])
                delta_back_decode_int[i][j] = fabs(decode_back_transfer_int[i][j] - base_int[i][j])
                delta_decode_int[i][j] = fabs(decode_int[i][j] - base_int[i][j])

        max_delta_back_decode_fl = max([max(i) for i in delta_back_decode_fl])
        max_delta_decode_fl = max([max(i) for i in delta_decode_fl])
        max_delta_back_decode_int = max([max(i) for i in delta_back_decode_int])
        max_delta_decode_int = max([max(i) for i in delta_decode_int])
        sum_delta_back_decode_fl = sum([sum(i) for i in delta_back_decode_fl])
        sum_delta_decode_fl = sum([sum(i) for i in delta_decode_fl])
        sum_delta_back_decode_int = sum([sum(i) for i in delta_back_decode_int])
        sum_delta_decode_int = sum([sum(i) for i in delta_decode_int])

        return [
        max_delta_decode_fl,
        max_delta_back_decode_fl,
        sum_delta_decode_fl,
        sum_delta_back_decode_fl,
        max_delta_decode_int,
        max_delta_back_decode_int,
        sum_delta_decode_int,
        sum_delta_back_decode_int,
    ]