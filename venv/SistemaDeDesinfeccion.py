#!/usr/bin/env python3.7

from tkinter import *
from tkinter.ttk import *
import random,time
from PIL import ImageTk, Image
import pyautogui,sensores



class App(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        # Setup Frame
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=100)
        container.grid_columnconfigure(0, weight=100)
        self.frames = {}
        for F in (StartPage, PageOne,PageTwo,PageThree,PageFour):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)
    def show_frame(self, context):
        frame = self.frames[context]
        frame.event_generate("<<ShowFrame>>")
        frame.tkraise()


class StartPage(Frame):
    def __init__(self, parent, controller):
        global image,play,progress
        Frame.__init__(self, parent)
        canvas = Canvas(self, width=480, height=280)
        image = Image.open("Imagenes/Inicio.jpg")
        image = image.resize((480, 280), Image.ANTIALIAS)
        image= ImageTk.PhotoImage(image)
        canvas.create_image(0, 0, anchor=NW, image=image)
        canvas.pack()
        self.value = 0
        self.change=controller
        self.can=canvas

        progress = Progressbar(self,orient=HORIZONTAL,
                               length=450, mode='determinate')
        progress.place(x=10,y=230)
        progress.after(1000,lambda : self.refresh_label())

    def refresh_label(self):
        global progress
        progress['value']=self.value
        progress.update_idletasks()
        self.value+=10
        if (self.value==110):
            progress.after(1000, lambda: self.change.show_frame(PageOne))
            return()
        progress.after(1000, lambda: self.refresh_label())


class PageOne(Frame):
    def __init__(self, parent, controller):
        global wait,config_image, lab_wait
        wait=[]
        Frame.__init__(self, parent)
        config_canvas = Canvas(self,bg="black", width=480, height=280)
        config_image = Image.open("Imagenes/Inicializando.jpg")
        config_image = config_image.resize((480, 280), Image.ANTIALIAS)
        config_image = ImageTk.PhotoImage(config_image)
        config_canvas.create_image(0, 0, anchor=NW, image=config_image)
        config_canvas.pack()
        self.value2=0
        self.value3 = 0
        for i in range(12):
            imagen=Image.open(f"Imagenes/GIF_Waiting/waiting_{i}.jpg")
            imagen=imagen.resize((60, 60), Image.ANTIALIAS)
            wait.append(ImageTk.PhotoImage(imagen))
        self.change = controller
        lab_wait = Label(self,image=wait[0],padding=-5)
        lab_wait.place(x=213,y=46)
        lab_wait.after(100, lambda: self.refresh_label2())

    def refresh_label2(self):
        global config_image,wait,lab_wait
        lab_wait.configure(image=wait[self.value2])
        self.value2 += 1
        if (self.value2==12):
            self.value2=0
            if (self.value3==20):
                self.value3 += 1
                lab_wait.after(100, sensores.FAN_ON())
                lab_wait.after(100, lambda: self.refresh_label2())
            elif (self.value3==25):
                self.value3 += 1
                lab_wait.after(100, sensores.HUMIDIFIER_ON())
                lab_wait.after(850, lambda: self.refresh_label2())
            elif(self.value3==30):
                self.change.show_frame(PageTwo)
                return()
            else:
                self.value3+=1
                lab_wait.after(100, lambda: self.refresh_label2())
        else:
            lab_wait.after(100,lambda: self.refresh_label2())


class PageTwo(Frame):
    def __init__(self, parent, controller):
        global run_image
        Frame.__init__(self, parent)
        config_canvas2 = Canvas(self, width=480, height=280)
        run_image = Image.open("Imagenes/Configuracion.jpg")
        run_image = run_image.resize((480, 280), Image.ANTIALIAS)
        run_image = ImageTk.PhotoImage(run_image)
        config_canvas2.create_image(0, 0, anchor=NW, image=run_image)
        config_canvas2.pack()
        #Botones

        config_canvas2.bind("<Button 1>", lambda x: self.getorigin(controller))
        self.bind("<<ShowFrame>>", self.on_show_frame)


    def on_show_frame(self, event):
        print("I am being shown...")

    def getorigin(event,control):
        x, y = pyautogui.position()
        print(x, y)
        if (x > 365 and x < 450 and y > 97 and y < 155):
            control.show_frame(PageThree)
            return ()
        elif (x > 295 and x < 460 and y > 195 and y < 310):
            control.show_frame(PageFour)
            return ()
        return()


class PageThree(Frame):
    def __init__(self, parent, controller):
        global config_main_image,imhere
        Frame.__init__(self, parent)
        config_canvas3 = Canvas(self, width=480, height=280)
        config_main_image = Image.open("Imagenes/Configuracion_A.jpg")
        imhere='A'
        config_main_image = config_main_image.resize((480, 280), Image.ANTIALIAS)
        config_main_image = ImageTk.PhotoImage(config_main_image)
        image_on_canvas =config_canvas3.create_image(0, 0, anchor=NW, image=config_main_image)
        #config_canvas3.create_image(0, 0, anchor=NW, image=config_main_image)
        config_canvas3.pack()
        config_canvas3.bind("<Button 1>", lambda x:self.getorigin(controller,config_canvas3,image_on_canvas))

    def getorigin(event,control,canva,image_on_canvas):
        global test_image,imhere
        x, y = pyautogui.position()
        print(x,y)
        if (x>0 and x<70 and y>50 and y<95):
            control.show_frame(PageTwo)
            return ()
        elif (x > 170 and x < 230 and y > 128 and y < 170):
            if (imhere!='A'):
                test_image = Image.open("Imagenes/Configuracion_A.jpg")
                test_image = test_image.resize((480, 280), Image.ANTIALIAS)
                test_image = ImageTk.PhotoImage(test_image)
                canva.itemconfig(image_on_canvas, image=test_image)
                canva.image = test_image
                imhere = 'A'
                return ()
        elif (x > 170 and x < 230 and y > 190 and y < 230):
            if (imhere!='B'):
                test_image = Image.open("Imagenes/Configuracion_B.jpg")
                test_image = test_image.resize((480, 280), Image.ANTIALIAS)
                test_image = ImageTk.PhotoImage(test_image)
                canva.itemconfig(image_on_canvas, image=test_image)
                canva.image = test_image
                imhere = 'B'
                return ()
        elif (x > 170 and x < 230 and y > 263 and y < 300):
            if (imhere!='C'):
                test_image = Image.open("Imagenes/Configuracion_C.jpg")
                test_image = test_image.resize((480, 280), Image.ANTIALIAS)
                test_image = ImageTk.PhotoImage(test_image)
                canva.itemconfig(image_on_canvas, image=test_image)
                canva.image = test_image
                imhere='C'
                return ()
        return()


class PageFour(Frame):
    def __init__(self, parent, controller):
        global operation_image
        Frame.__init__(self, parent)
        config_canvas4 = Canvas(self, width=480, height=280)
        operation_image = Image.open("Imagenes/operacion.jpg")
        operation_image = operation_image.resize((480, 280), Image.ANTIALIAS)
        operation_image = ImageTk.PhotoImage(operation_image)
        config_canvas4.create_image(0, 0, anchor=NW, image=operation_image)
        config_canvas4.pack()
        config_canvas4.bind("<Button 1>", lambda x:self.getorigin(controller))

    def getorigin(event,control):
        x, y = pyautogui.position()
        print(x,y)
        if (x>15 and x<180 and y>50 and y<150):
            control.show_frame(PageTwo)
            return ()


app = App()
app.title('Sistema de desinfeccion OZONO')
app.mainloop()