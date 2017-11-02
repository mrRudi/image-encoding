from math import sqrt
import cv2
import numpy as np
from collections import namedtuple

Scale = namedtuple('Scale' , 'max min')

class Rsa:
    def __init__(self,p,q,e,d):
        self.p = p
        self.q = q
        self.e = e
        self.d = d
        self.n=p*q
        self.f=(p-1)*(q-1)
        

class Algorithm():

    def __init__(self,rsa,height=None,width=None,img=None):
        self.rsa = rsa
        if img is None:
            self.height,self.width = height,width
            self.img = None
        else:
            self.height,self.width = img.shape[:2]
            self.img = img

        if self.height % 2 == 1:
            self.height -= 1
        self.scale = None

    def iter_for_img(func):
        def the_wrapper_func(self):
            new_img = np.zeros((self.height, self.width), dtype=np.float64)
            for i in range(0,self.height,2):
                line_x = iter(self.img[i])
                line_y = iter(self.img[i+1])
                for j in range(self.width):
                    x = next(line_x)
                    y = next(line_y)
                    new_img[i][j], new_img[i+1][j] = func(self,x,y,i,j)  
            return new_img
        return the_wrapper_func

    def code(self, x,y, i,j):
        raise NotImplementedError()
        
    def decode(self, x,y, i,j):
        raise NotImplementedError()

    def iter_for_transfer(func):
        def the_wrapper_func(self):
            new_img = np.zeros((self.height, self.width), dtype=np.float64)
            for i in range(self.height):
                for j in range(self.width):
                    new_img[i][j] = func(self, self.img[i][j])  
            return new_img
        return the_wrapper_func
    
    @iter_for_transfer
    def transfer(self, value):
        return (256.*(value-self.scale.min))/(self.scale.max-self.scale.min)

    @iter_for_transfer
    def back_transfer(self, value):
        return (value*(self.scale.max-self.scale.min))/256. + self.scale.min
    

class Algorithm_first(Algorithm):

    def __init__(self,rsa,*args, **kwargs):
        super(Algorithm_first,self).__init__(rsa,*args, **kwargs)

    @Algorithm.iter_for_img
    def code(self, x,y, i,j):
        next_x = x-y + (self.height - (i+1)) * (j+1) * ((self.rsa.p**self.rsa.e)%(self.rsa.f - (i+1)))
        next_y = 2*x*y + (self.height - (i+2)) * (j+1) * ((self.rsa.q**self.rsa.d)%(self.rsa.f - (i+2)))
        return next_x, next_y

    @Algorithm.iter_for_img
    def decode(self, x,y, i,j):
        a_m = x - (self.height-(i+1)) * (j+1) * ((self.rsa.p**self.rsa.e)%(self.rsa.f-(i+1)))
        b_m = ( y - (self.height - (i+2)) * (j+1) * ((self.rsa.q**self.rsa.d)%(self.rsa.f - (i+2))) )/2
        d_m = (a_m)**2 + 4*b_m
        next_x = (a_m + sqrt(d_m))/2
        next_y = (2*b_m) / (a_m + sqrt(d_m)) 
        return next_x, next_y  


class Algorithm_second(Algorithm):

    def __init__(self,rsa,*args, **kwargs):
        self.a = ((rsa.q+rsa.p)**rsa.e)%rsa.n
        super(Algorithm_second,self).__init__(rsa,*args, **kwargs)

    @Algorithm.iter_for_img
    def code(self, x,y, i,j):
        next_x = self.a*x + (i+1)**2         
        next_y = self.a*y + (i+2)**3 
        return next_x, next_y 

    @Algorithm.iter_for_img    
    def decode(self, x,y, i,j):
        delta_x = self.a*(x-(i+1)**2)
        delta_y = self.a*(y-(i+2)**3)
        next_x = delta_x/(self.a**2)        
        next_y = delta_y/(self.a**2)  
        return next_x, next_y 


if __name__ == "__main__":
    img = cv2.imread('base.jpg',0)
    rsa = Rsa(17,11,103,87)
    alg = Algorithm_second(rsa,img=img)
    print(img)
    code = alg.code()
    print(code)
    alg.img = code
    print(alg.decode())