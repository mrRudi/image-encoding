from math import sqrt
import cv2
import numpy as np


class Rsa:
    def __init__(self,p,q,e,d):
        self.p = p
        self.q = q
        self.e = e
        self.d = d
        self.n=p*q
        self.f=(p-1)*(q-1)
        

class Scheme:

    def __init__(self,algorithm):
        self.algorithm = algorithm

    # def iter_img(self,func):
    #     def the_wrapper_func():
    #         code = np.zeros((height, width), dtype=np.float64)
    #         for i in range(0,self.height,2):
    #             line_x = iter(self.img[i])
    #             line_y = iter(self.img[i+1])
    #             # print(i)
    #             for j in range(width):
    #                 x = next(line_x)
    #                 y = next(line_y)
    #                 code[i][j], code[i+1][j] = self.algorithm.code(x,y,i,j)  
    #         return code

    #         func()
    #     return the_wrapper_func


    def code(self,img):
        code = np.zeros((self.algorithm.height, self.algorithm.width), dtype=np.float64)
        for i in range(0,self.algorithm.height,2):
            line_x = iter(img[i])
            line_y = iter(img[i+1])
            for j in range(self.algorithm.width):
                x = next(line_x)
                y = next(line_y)
                code[i][j], code[i+1][j] = self.algorithm.code(x,y,i,j)  
        return code
        
    def decode(self,img):
        decode = np.zeros((self.algorithm.height, self.algorithm.width), dtype=np.float64)
        for i in range(0,self.algorithm.height,2):
            line_x = iter(img[i])
            line_y = iter(img[i+1])
            for j in range(self.algorithm.width):
                x = next(line_x)
                y = next(line_y)
                decode[i][j], decode[i+1][j] = self.algorithm.decode(x,y,i,j)  
        return decode

    # def transfer(self, img):
    #     min_val = min([min(i) for i in img])
    #     max_val = max([max(i) for i in img])
    #     transfer = np.zeros((height, width), dtype=np.float64)
    #     for i in range(height):
    #         for j in range(width):
    #             transfer[i][j] = (256*(code[i][j]-min_val))/(max_val-min_val)
    
    # def back_transfer(self, img):
    #     back_transfer = np.zeros((height, width), dtype=np.float64)
    #     for i in range(height):
    #         for j in range(width):
    #             back_transfer[i][j] = (transfer[i][j]*(max_val-min_val))/256 + min_val


class Algorithm():

    def __init__(self,rsa,height,width):
        self.rsa = rsa
        self.height = height
        self.width = width

    def code(self, x,y, i,j):
        raise NotImplementedError()
        
    def decode(self, x,y, i,j):
        raise NotImplementedError()
    

class Algorithm_first(Algorithm):

    def __init__(self,rsa,height,width):
        super(Algorithm_first,self).__init__(rsa,height,width)

    def code(self, x,y, i,j):
        next_x = x-y + (self.height - (i+1)) * (j+1) * ((self.rsa.p**rsa.e)%(self.rsa.f - (i+1)))
        next_y = 2*x*y + (self.height - (i+2)) * (j+1) * ((self.rsa.q**rsa.d)%(self.rsa.f - (i+2)))
        return next_x, next_y

    def decode(self, x,y, i,j):
        a_m = x - (self.height-(i+1)) * (j+1) * ((self.rsa.p**self.rsa.e)%(self.rsa.f-(i+1)))
        b_m = ( y - (self.height - (i+2)) * (j+1) * ((self.rsa.q**self.rsa.d)%(self.rsa.f - (i+2))) )/2
        d_m = (a_m)**2 + 4*b_m
        next_x = (a_m + sqrt(d_m))/2
        next_y = (2*b_m) / (a_m + sqrt(d_m)) 
        return next_x, next_y  


class Algorithm_second(Algorithm):

    def __init__(self,rsa,height,width):
        self.a = ((rsa.q+rsa.p)**rsa.e)%rsa.n
        super(Algorithm_second,self).__init__(rsa,height,width)

    def code(self, x,y, i,j):
        next_x = self.a*x + (i+1)**2         
        next_y = self.a*y + (i+2)**3 
        return next_x, next_y 
        
    def decode(self, x,y, i,j):
        delta_x = self.a*(x-(i+1)**2)
        delta_y = self.a*(y-(i+2)**3)
        next_x = delta_x/(self.a**2)        
        next_y = delta_y/(self.a**2)  
        return next_x, next_y 

