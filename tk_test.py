from tkinter.filedialog import askopenfilename
from tkinter import Tk,Label,Button,Entry,W,Radiobutton,IntVar,E,Toplevel
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
        self.btn_select_img = Button(self.master, text="Вибрати зображення", command=self.select_image)
        self.btn_select_img.grid(row=0, column=0, columnspan=4, sticky=W+E)

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

		#обробка зображень
        Button(self.master, text='запустити', command=self.create_window).grid(row=3, column=2, columnspan=2, sticky=W+E, pady=4)
	
    def save_RSA(self):
        self.rsa = Rsa(int(self.p.get()),int(self.q.get()),int(self.e.get()),int(self.d.get()))

    def select_image(self):
        self.path_img = askopenfilename()
        self.img = cv2.imread(self.path_img,0)

    def select_algorithm(self):
        if self.method.get() == 1:
        	self.algorithm = Algorithm_first(self.rsa,self.height,self.width)
        elif self.method.get() == 2:
            self.algorithm = Algorithm_second(self.rsa,self.height,self.width)

    def resize(self):
        coefficient_size = float(self.coefficient_size_img.get())
        height,width = self.img.shape[:2]
        self.img = cv2.resize(self.img,(int(width*coefficient_size), int(height*coefficient_size)), interpolation = cv2.INTER_CUBIC)
        self.height,self.width = self.img.shape[:2]

    def update(self):
        self.save_RSA()
        self.resize()
        self.select_algorithm()

    def create_window(self):
        self.update()
        base = self.img.copy().astype(np.float64)

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