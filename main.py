from tkinter.filedialog import askopenfilename
from tkinter import Tk,Label,Button,Entry,W,Radiobutton,IntVar,E,Toplevel,StringVar,PhotoImage,Scrollbar,Text,RIGHT,LEFT,Y,END
import numpy as np
import cv2
from libs.builder import Algorithm_first,Algorithm_second,Rsa,Scale
from libs.db import Db_pictures
from functools import partial
from PIL import Image
from PIL import ImageTk


def path_res(path):
    return "data/res/"+path


class GUI():
    """графічний інтерфейс"""

    def __init__(self, master):
        self.master = master

		#вибір зображення
        Label(self.master, text="вибране зображення:").grid(row=0,column=0, sticky=W+E)
        self.path_label = StringVar()
        Label(self.master, textvariable=self.path_label).grid(row=0,column=1,columnspan=2, sticky=W+E)
        self.path_label.set('не вибрано')
        self.btn_select_img = Button(self.master, text="Вибрати зображення", command=self.select_image)
        self.btn_select_img.grid(row=0, column=3, sticky=W+E)

		#коефіціенти RSA
        Label(self.master, text="p =").grid(row=1,column=0, sticky=W+E)
        Label(self.master, text="e =").grid(row=1,column=2, sticky=W+E)
        Label(self.master, text="q =").grid(row=2,column=0, sticky=W+E)
        Label(self.master, text="d =").grid(row=2,column=2, sticky=W+E)
        self.p = Entry(self.master)
        self.e = Entry(self.master)
        self.q = Entry(self.master)
        self.d = Entry(self.master)
        self.p.grid(row=1, column=1, sticky=W+E)
        self.e.grid(row=1, column=3, sticky=W+E)
        self.q.grid(row=2, column=1, sticky=W+E)
        self.d.grid(row=2, column=3, sticky=W+E)

        self.p.insert(0,"17")
        self.e.insert(0,"103")
        self.q.insert(0,"11")
        self.d.insert(0,"87")

		#розмір зображення
        Label(self.master, text="coeff_size =").grid(row=3,column=0, sticky=W+E)
        self.coefficient_size_img = Entry(self.master)
        self.coefficient_size_img.grid(row=3, column=1, sticky=W+E)
        self.coefficient_size_img.insert(0,"0.125")

		#вибір алгоритму шифрування
        self.method = IntVar()
        Radiobutton(self.master,text="метод №1",padx = 20,variable=self.method,value=1).grid(row=4,column=0,sticky=W+E)
        Radiobutton(self.master,text="метод №2",padx = 20,variable=self.method,value=2).grid(row=4,column=1,sticky=W+E)
        
        #зміна розміру зображення
        # Button(self.master, text='зміна розміру', command=self.resize).grid(row=3, column=2, sticky=W+E, pady=4)
		
        #обробка зображень
        self.create_button(self.master, self.create_windows, path_res("play.png"),40,3,3)

    def save_RSA(self):
        self.rsa = Rsa(int(self.p.get()),int(self.q.get()),int(self.e.get()),int(self.d.get()))

    def select_image(self):
        self.path_img = askopenfilename()
        self.img = cv2.imread(self.path_img,0)
        self.path_label.set(self.path_img)

    def select_algorithm(self):
        height, width = self.img_resize.shape[:2]
        self.select_method = self.method.get()
        if self.select_method == 1:
        	self.algorithm = Algorithm_first(self.rsa,height=height,width=width)
        elif self.select_method == 2:
            self.algorithm = Algorithm_second(self.rsa,height=height,width=width)

    def resize(self):
        self.img_resize = self.img.copy()
        coefficient_size = self.coefficient_size_img.get()
        if coefficient_size:
            coefficient_size = float(coefficient_size)
            height,width = self.img.shape[:2]
            self.img_resize = cv2.resize(self.img,(int(width*coefficient_size), int(height*coefficient_size)), interpolation = cv2.INTER_AREA)

    def create_windows(self):
        self.resize()
        self.save_RSA()
        self.select_algorithm()

        db_pictures = Db_pictures(self.rsa,self.img_resize.copy(),self.algorithm)    
        db_pictures.create_pictures()
        db_pictures.preparation_for_display()

        window = Toplevel(self.master)
        window.title("show")

        
        for number, picture in enumerate(db_pictures.pictures):
            Label(window, text="%s"%picture.title).grid(row=number,column=0, sticky=W+E)
            self.create_button(window, partial(self.show_picture, picture.title, picture.display,window), path_res("show.png"),40,number,1)
            self.create_button(window, partial(self.save_img, picture.title, picture.image), path_res("save.png"),40,number,2)
        
        self.create_button(window, partial(self.show_all_pictures, db_pictures.pictures,window), path_res("show-all.png"),40,0,3)
        self.create_button(window, partial(self.save_all_images, db_pictures.pictures), path_res("save-all.png"),40,1,3)
        self.create_button(window, partial(self.delta_show, db_pictures.delta(),window), path_res("delta.png"),40,2,3)
        
    def delta_show(self, delta,window):
        window_delta = Toplevel(window)
        message = """Похибки
1)Обрахунки похибки a_ij - b_ij, коли a та b є дробовими числами
Максимальна похибка між базовим і декодованим зображенням: {}
Максимальна похибка між базовим і декодованим зображенням із зміною шкали: {}
Сумарна похибка між базовим і декодованим зображенням: {}
Сумарна похибка між базовим і декодованим зображенням із зміною шкали: {}
1)Обрахунки похибки a_ij - b_ij, коли a та b є числами з шкали 0-255
Максимальна похибка між базовим і декодованим зображенням: {}
Максимальна похибка між базовим і декодованим зображенням із зміною шкали: {}
Сумарна похибка між базовим і декодованим зображенням: {}
Сумарна похибка між базовим і декодованим зображенням із зміною шкали: {}"""

        S = Scrollbar(window_delta)
        T = Text(window_delta)
        S.pack(side=RIGHT, fill=Y)
        T.pack(side=LEFT, fill=Y)
        S.config(command=T.yview)
        T.config(yscrollcommand=S.set)
        T.insert(END, message.format(*delta))

    def create_button(self, master,comand,path_image,size,row,column):
        b = Button(master, command=comand)
        image = ImageTk.PhotoImage(Image.open(path_image).resize((size,size),Image.ANTIALIAS))
        b.config(image=image)
        b.image = image
        b.grid(row=row, column=column)


    def save_img(self, title, image):
        image_uint8 = image.astype(np.uint8)
        cv2.imwrite('result/%s-%s.jpg'%(title,self.select_method), image_uint8)
        with open('result/%s-%s.txt'%(title,self.select_method),"w") as w_image:
            for i in range(self.algorithm.height):
                for j in range(self.algorithm.width):
                    w_image.write("{} ".format(image_uint8[i][j]))
                w_image.write("\n")

    def save_all_images(self, pictures):
        for picture in pictures:
            self.save_img(picture.title,picture.image)
    
    def show_picture(self,title,display_image,window):
        window_with_image = Toplevel(window)
        window_with_image.title(title)
        panel = Label(window_with_image,image=display_image)
        panel.pack(padx=10, pady=10)
    
    def show_all_pictures(self, pictures,window):
        for picture in pictures:
            self.show_picture(picture.title,picture.display,window)


if __name__ == "__main__":
    root = Tk()
    root.title("image encoding")
    my_gui = GUI(root)
    root.mainloop()