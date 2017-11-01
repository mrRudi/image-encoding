from tkinter.filedialog import askopenfilename
from tkinter import Tk,Label,Button,Entry,W,Radiobutton,IntVar,E,Toplevel,StringVar
from PIL import Image
from PIL import ImageTk
import cv2
from builder import Algorithm_first,Algorithm_second,Rsa,Scheme
import numpy as np


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
        self.r1 = Radiobutton(self.master,text="метод №1",padx = 20,variable=self.method,value=1).grid(row=4,column=0,sticky=W+E)
        self.r2 = Radiobutton(self.master,text="метод №2",padx = 20,variable=self.method,value=2).grid(row=4,column=1,sticky=W+E)
        
        #зміна розміру зображення
        Button(self.master, text='зміна розміру', command=self.resize).grid(row=3, column=2, sticky=W+E, pady=4)
		
        #обробка зображень
        Button(self.master, text='запустити', command=self.create_windows).grid(row=3, column=3, sticky=W+E, pady=4)
	
    def save_RSA(self):
        self.rsa = Rsa(int(self.p.get()),int(self.q.get()),int(self.e.get()),int(self.d.get()))

    def select_image(self):
        self.path_img = askopenfilename()
        self.img = cv2.imread(self.path_img,0)
        self.img_resize = self.img.copy()
        self.path_label.set(self.path_img)

    def select_algorithm(self):
        self.height,self.width = self.img_resize.shape[:2]
        if self.height % 2 == 1:
            self.height -= 1
        if self.method.get() == 1:
        	self.algorithm = Algorithm_first(self.rsa,self.height,self.width)
        elif self.method.get() == 2:
            self.algorithm = Algorithm_second(self.rsa,self.height,self.width)

    def resize(self):
        coefficient_size = float(self.coefficient_size_img.get())
        height,width = self.img.shape[:2]
        self.img_resize = cv2.resize(self.img,(int(width*coefficient_size), int(height*coefficient_size)), interpolation = cv2.INTER_AREA)

    def create_windows(self):
        self.save_RSA()
        self.select_algorithm()
        base = self.img_resize.copy().astype(np.float64)

        scheme = Scheme(self.algorithm)

        code = scheme.code(base)
        decode = scheme.decode(code)

        base = Image.fromarray(base.astype(np.uint8))
        code = Image.fromarray(code.astype(np.uint8))
        base = ImageTk.PhotoImage(base)
        code = ImageTk.PhotoImage(code)

        window = Toplevel(self.master)

        panelA = Label(window,image=base)
        panelA.image = base
        panelA.pack(side="left", padx=10, pady=10)
 
			# while the second panel will store the edge map
        panelB = Label(window,image=base)
        panelB.image = base
        panelB.pack(side="right", padx=10, pady=10)



if __name__ == "__main__":
    root = Tk()
    my_gui = GUI(root)
    root.mainloop()