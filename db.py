import cv2
import numpy as np
from builder import Rsa,Scale
from PIL import Image
from PIL import ImageTk
from collections import namedtuple

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

