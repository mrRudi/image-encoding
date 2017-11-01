from tkinter.filedialog import askopenfilename
from tkinter import Tk,Label,Button,Entry,W,Radiobutton,IntVar,E,Toplevel
from PIL import Image
from PIL import ImageTk
import cv2




class RSA:
    def __init__(p,q,e,d):
        self.p = p
        self.q = q
        self.e = e
        self.d = d
        self.n=p*q
        self.f=(p-1)*(q-1)


class Options:
    def update_RSA(self):
        self.rsa = RSA(p.get(), q.get(), e.get(), d.get())

    def __init__(path_img):
        self.update_RSA()
        self._img = cv2.imread(path_img,0)  

    def first_algorithm(self):
        self._algorithm = Algorithm_first(self._p,self._q,self._e,self._d)

    def second_algorithm(self):
        self._algorithm = Algorithm_second(self._p,self._q,self._e,self._d)

    def resize(self,n):
        height,width = self._img.shape[:2]
        self._img = cv2.resize(self._img,(int(width*n), int(height*n)), interpolation = cv2.INTER_CUBIC)
	
	def run():
		def create_window():
			window = Toplevel(root)


		def select_image():
			global panelA, panelB
			path = askopenfilename()
			if len(path) > 0:
				image = cv2.imread(path)
				gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
				edged = cv2.Canny(gray, 50, 100)
				image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
				image = Image.fromarray(image)
				edged = Image.fromarray(edged)
				image = ImageTk.PhotoImage(image)
				edged = ImageTk.PhotoImage(edged)

				if panelA is None or panelB is None:
					panelA = Label(image=image)
					panelA.image = image
					panelA.pack(side="left", padx=10, pady=10)
					panelB = Label(image=edged)
					panelB.image = edged
					panelB.pack(side="right", padx=10, pady=10)
				else:
					panelA.configure(image=image)
					panelB.configure(image=edged)
					panelA.image = image
					panelB.image = edged

		root = Tk()
		panelA = None
		panelB = None
		
		def show_entry_fields():
		print("%s\n%s\n%s\n%s" % (p.get(), e.get(), q.get(), d.get()))

		Label(root, text="p =").grid(row=0,column=0)
		Label(root, text="e =").grid(row=0,column=2)
		Label(root, text="q =").grid(row=1,column=0)
		Label(root, text="d =").grid(row=1,column=2)

		p = Entry(root)
		e = Entry(root)
		q = Entry(root)
		d = Entry(root)

		p.grid(row=0, column=1)
		e.grid(row=0, column=3)
		q.grid(row=1, column=1)
		d.grid(row=1, column=3)

		v = IntVar()
		Radiobutton(root,text="метод №1",padx = 20,variable=v,value=1).grid(row=3,column=0,columnspan=4,sticky=W+E)
		Radiobutton(root,text="метод №2",padx = 20,variable=v,value=2).grid(row=4,column=0,columnspan=4,sticky=W+E)

		Button(root, text='Quit', command=root.quit).grid(row=5, column=0, sticky=W, pady=4)
		Button(root, text='Show', command=show_entry_fields).grid(row=5, column=1, sticky=W, pady=4)
		Button(root, text='Create new window', command=create_window).grid(row=5, column=2, sticky=W, pady=4)

		root.mainloop()
