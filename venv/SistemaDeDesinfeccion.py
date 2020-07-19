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
        for F in (StartPage, PageOne,PageTwo):
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
        canvas = Canvas(self, width=1280, height=720)
        image = Image.open("Imagenes/Inicio.jpg")
        image = image.resize((1280, 720), Image.ANTIALIAS)
        image= ImageTk.PhotoImage(image)
        canvas.create_image(0, 0, anchor=NW, image=image)
        canvas.pack()
        self.value = 0
        self.change=controller
        self.can=canvas

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
            return()
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
        self.value2=0
        self.value3 = 0
        for i in range(12):
            imagen=Image.open(f"Imagenes/GIF_Waiting/waiting_{i}.jpg")
            imagen=imagen.resize((200, 200), Image.ANTIALIAS)
            wait.append(ImageTk.PhotoImage(imagen))
        self.change = controller
        lab_wait = Label(self,image=wait[0])
        lab_wait.place(x=530,y=200)
        lab_wait.after(100, lambda: self.refresh_label2())

    def refresh_label2(self):
        global config_image,wait,lab_wait
        lab_wait.configure(image=wait[self.value2])
        self.value2 += 1
        if (self.value2==11):
            self.value2=0
            if (self.value3==10):
                self.value3 += 1
                lab_wait.after(10, lambda: self.FAN_ON())
                lab_wait.after(80, lambda: self.refresh_label2())
            elif (self.value3==15):
                self.value3 += 1
                lab_wait.after(10, lambda: self.HUMIDIFIER_ON())
                lab_wait.after(80, lambda: self.refresh_label2())
            elif(self.value3==20):
                self.change.show_frame(PageTwo)
                return()
            else:
                self.value3+=1
                lab_wait.after(100, lambda: self.refresh_label2())
        else:
            lab_wait.after(100,lambda: self.refresh_label2())
    def FAN_ON(self):
        '''Prender Ventilador'''
        print("Ventilador ON")
        return ()
    def HUMIDIFIER_ON(self):
        """Prender humidificador"""
        print("HUMIDIFICADOR ON")
        return()


class PageTwo(Frame):
    def __init__(self, parent, controller):
        global run_image
        Frame.__init__(self, parent)
        config_canvas2 = Canvas(self, width=1280, height=720)
        run_image = Image.open("Imagenes/Configuracion.jpg")
        run_image = run_image.resize((1280, 720), Image.ANTIALIAS)
        run_image = ImageTk.PhotoImage(run_image)
        config_canvas2.create_image(0, 0, anchor=NW, image=run_image)
        config_canvas2.pack()
        self.bind("<<ShowFrame>>", self.on_show_frame)

    def on_show_frame(self, event):
        print("I am being shown...")


        #BOTONES
        '''
        start_page = Button(self, text="Start Page",image=home,borderwidth=0,highlightthickness = 0, padx=0,pady=0, command=lambda: controller.show_frame(StartPage))
        start_page.place(x=654, y=10)
        page_one = Button(self, text="Page One", image=back,borderwidth=0,highlightthickness = 0, padx=0, pady=0,command=lambda: controller.show_frame(PageOne))
        page_one.place(x=14, y=10)
        '''

app = App()
app.title('Sistema de desinfeccion OZONO')
app.mainloop()