from tkinter import *
from tkinter.ttk import *
import random,time
from PIL import ImageTk, Image


class App(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        # Setup Frame
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=100)
        container.grid_columnconfigure(0, weight=100)
        self.frames = {}
        for F in (StartPage, PageOne):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)
    def show_frame(self, context):
        frame = self.frames[context]
        frame.tkraise()
class StartPage(Frame):
    def __init__(self, parent, controller):
        global image,play,progress
        Frame.__init__(self, parent)
        canvas = Canvas(self, width=1280, height=720)
        image = Image.open("Imagenes/Inicio.jpg")
        image = image.resize((1280, 720), Image.ANTIALIAS)
        image= ImageTk.PhotoImage(image)
        canvas.create_image(0, 0, anchor=NW, image=image)
        canvas.pack()
        self.value = 0
        self.change=controller
        progress = Progressbar(self,orient=HORIZONTAL,
                               length=1000, mode='determinate')
        progress.place(x=150,y=680)
        progress.after(1000,lambda : self.refresh_label())

    def refresh_label(self):
        global progress
        progress['value']=self.value
        progress.update_idletasks()
        self.value+=10
        if (self.value==110):
            progress.after(1000, lambda: self.change.show_frame(PageOne))
        progress.after(1000, lambda: self.refresh_label())

class PageOne(Frame):
    def __init__(self, parent, controller):
        global wait,config_image, lab_wait
        wait=[]
        Frame.__init__(self, parent)
        config_canvas = Canvas(self,bg="black", width=1280, height=720)
        config_image = Image.open("Imagenes/Inicializando.jpg")
        config_image = config_image.resize((1280, 720), Image.ANTIALIAS)
        config_image = ImageTk.PhotoImage(config_image)
        config_canvas.create_image(0, 0, anchor=NW, image=config_image)
        config_canvas.pack()
        self.value=0
        for i in range(11):
            imagen=Image.open(f"Imagenes/GIF_Waiting/waiting_{i}.jpg")
            imagen=imagen.resize((200, 200), Image.ANTIALIAS)
            wait.append(ImageTk.PhotoImage(imagen))

        lab_wait = Label(self,image=wait[0])
        lab_wait.place(x=530,y=200)
        lab_wait.after(1000, lambda: self.refresh_label())

    def refresh_label(self):
        global config_image,wait,lab_wait
        lab_wait.configure(image=wait[self.value])
        self.value += 1
        if (self.value==11):
            self.value=0
            lab_wait.after(1000, lambda: self.refresh_label())
        lab_wait.after(1000,lambda: self.refresh_label())

'''
class PageTwo(Frame):
    def __init__(self, parent, controller):
        global run_image, back, home,simbolocarga,voltsimbo,altai,bajai,inrushi,microcortei,transitorioi,perdidafasei,rvci
        global start_button_image,stop_button_image,start_button
        Frame.__init__(self, parent)

        config_canvas2 = Canvas(self, width=900, height=600)
        run_image = ImageTk.PhotoImage(Image.open("run.jpg"))
        config_canvas2.create_image(0, 0, anchor=NW, image=run_image)
        config_canvas2.pack()

        #BOTONES
        start_page = Button(self, text="Start Page",image=home,borderwidth=0,highlightthickness = 0, padx=0,pady=0, command=lambda: controller.show_frame(StartPage))
        start_page.place(x=654, y=10)
        page_one = Button(self, text="Page One", image=back,borderwidth=0,highlightthickness = 0, padx=0, pady=0,command=lambda: controller.show_frame(PageOne))
        page_one.place(x=14, y=10)
'''
app = App()
app.mainloop()