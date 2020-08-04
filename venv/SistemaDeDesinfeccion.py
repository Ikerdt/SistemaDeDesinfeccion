#!/usr/bin/env python3.7

from tkinter import *
from tkinter.ttk import *
import random,time
from PIL import ImageTk, Image
import pyautogui,sensores,os

imhere='A'
State="Start"

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
        lab_wait.after(50, lambda: self.refresh_label2())

    def refresh_label2(self):
        global config_image,wait,lab_wait,Ozono, Temp, Hum
        lab_wait.configure(image=wait[self.value2])
        self.value2 += 1
        if (self.value2==12):
            self.value2=0
            if (self.value3==20):
                self.value3 += 1
                lab_wait.after(50, sensores.FAN_ON())
                lab_wait.after(50, lambda: self.refresh_label2())
            elif (self.value3==25):
                self.value3 += 1
                lab_wait.after(50, sensores.HUMIDIFIER_ON())
                lab_wait.after(50, lambda: self.refresh_label2())
            elif(self.value3==30):
                Ozono, Temp, Hum = sensores.GET_LECTURE()
                self.change.show_frame(PageTwo)
                return()
            else:
                self.value3+=1
                lab_wait.after(50, lambda: self.refresh_label2())
        else:
            lab_wait.after(50,lambda: self.refresh_label2())


class PageTwo(Frame):
    def __init__(self, parent, controller):
        global run_image,config_canvas2,lab_wait2
        Frame.__init__(self, parent)
        config_canvas2 = Canvas(self, width=480, height=280)
        run_image = Image.open("Imagenes/Configuracion.jpg")
        run_image = run_image.resize((480, 280), Image.ANTIALIAS)
        run_image = ImageTk.PhotoImage(run_image)
        config_canvas2.create_image(0, 0, anchor=NW, image=run_image)
        config_canvas2.pack()
        self.flag=False
        config_canvas2.bind("<Button 1>", lambda x: self.getorigin(controller))
        self.bind("<<ShowFrame>>",self.on_show_frame)

    def on_show_frame(self,event):
        global Ozono, Temp, Hum,config_canvas2,Oz,Hu,Te,display
        display=1
        if (self.flag==False):
            Oz=config_canvas2.create_text(80, 85, fill="gray", font="Helvetica 20 bold",
                                       text=f"{Ozono}ppm")
            Hu=config_canvas2.create_text(75, 150, fill="gray", font="Helvetica 20 bold",
                                       text=f"{Hum}%")
            Te=config_canvas2.create_text(75, 220, fill="gray", font="Helvetica 20 bold",
                                       text=f"{Temp}°C")
            self.flag==True
        config_canvas2.itemconfigure(Oz, text=f"{Ozono}ppm")
        config_canvas2.itemconfigure(Hu, text=f"{Hum}%")
        config_canvas2.itemconfigure(Te, text=f"{Temp}°C")

        self.after(10000,self.refresh_data)

        return()

    def refresh_data(self):
        global Ozono, Temp, Hum,Oz,Hu,Te,config_canvas2,display

        if (display==1):
            Ozono, Temp, Hum=sensores.GET_LECTURE()
            config_canvas2.itemconfigure(Oz,text=f"{Ozono}ppm")
            config_canvas2.itemconfigure(Hu,text=f"{Hum}%")
            config_canvas2.itemconfigure(Te,text=f"{Temp}°C")
            self.after(10000, self.refresh_data)

            return()
        return()

    def getorigin(event,control):
        global display
        x, y = pyautogui.position()
        print(x, y)
        if (x > 365 and x < 450 and y > 97 and y < 155):
            #display = 3
            control.show_frame(PageThree)
            return ()
        elif (x > 295 and x < 460 and y > 195 and y < 310):
            display = 4
            control.show_frame(PageFour)
            return ()
        return()


class PageThree(Frame):
    def __init__(self, parent, controller):
        global config_main_image,imhere,all_comboboxes
        Frame.__init__(self, parent)
        config_canvas3 = Canvas(self, width=480, height=280)
        config_main_image = Image.open("Imagenes/Configuracion_A.jpg")
        imhere='A'
        config_main_image = config_main_image.resize((480, 280), Image.ANTIALIAS)
        config_main_image = ImageTk.PhotoImage(config_main_image)
        image_on_canvas =config_canvas3.create_image(0, 0, anchor=NW, image=config_main_image)
        config_canvas3.pack()
        config_canvas3.bind("<Button 1>", lambda x:self.getorigin(controller,config_canvas3,image_on_canvas))

        #
        val = []
        for a in range(61):
            if(a!=0):
                val.append(a)
        TA_A = Combobox(self, values=(val), width=2,justify="center",state='readonly')
        TA_A.set("3")
        TA_A.place(x=258, y=87)
        TB_A = Combobox(self, values=(val), width=2,justify="center",state='readonly')
        TB_A.set("10")
        TB_A.place(x=345, y=87)
        TC_A = Combobox(self, values=(val), width=2,justify="center",state='readonly')
        TC_A.set("15")
        TC_A.place(x=425, y=87)
        TA_B = Combobox(self, values=(val), width=2,justify="center",state='readonly')
        TA_B.set("4")
        TA_B.place(x=258,y=145)
        TB_B = Combobox(self, values=(val), width=2,justify="center",state='readonly')
        TB_B.set("12")
        TB_B.place(x=345, y=145)
        TC_B = Combobox(self, values=(val), width=2,justify="center",state='readonly')
        TC_B.set("18")
        TC_B.place(x=425, y=145)
        TA_C = Combobox(self, values=(val), width=2,justify="center",state='readonly')
        TA_C.set("5")
        TA_C.place(x=258, y=220)
        TB_C = Combobox(self, values=(val), width=2,justify="center",state='readonly')
        TB_C.set("15")
        TB_C.place(x=345, y=220)
        TC_C = Combobox(self, values=(val), width=2,justify="center",state='readonly')
        TC_C.set("20")
        TC_C.place(x=425, y=220)
        all_comboboxes=(TA_A,TB_A,TC_A,TA_B,TB_B,TC_B,TA_C,TB_C,TC_C)

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
        global operation_image,config_canvas4,canva_image
        Frame.__init__(self, parent)
        config_canvas4 = Canvas(self, width=480, height=280)
        operation_image = Image.open("Imagenes/operacion_1.jpg")
        operation_image = operation_image.resize((480, 280), Image.ANTIALIAS)
        operation_image = ImageTk.PhotoImage(operation_image)
        canva_image=config_canvas4.create_image(0, 0, anchor=NW, image=operation_image)
        config_canvas4.pack()
        config_canvas4.bind("<Button 1>", lambda x:self.getorigin(controller))
        self.bind("<<ShowFrame>>", self.on_show_frame)

    def on_show_frame(self, event):
        global imhere,all_comboboxes,config_canvas4
        global Ozono, Temp, Hum, Oz, Hu, Te, display
        if (imhere=='A'):
            self.TA_Value=all_comboboxes[0].get()
            self.TB_Value = all_comboboxes[1].get()
            self.TC_Value = all_comboboxes[2].get()
            print(self.TA_Value,self.TB_Value,self.TC_Value)
        elif (imhere=='B'):
            self.TA_Value=all_comboboxes[3].get()
            self.TB_Value = all_comboboxes[4].get()
            self.TC_Value = all_comboboxes[5].get()
            print(self.TA_Value,self.TB_Value,self.TC_Value)
        elif (imhere=='C'):
            self.TA_Value=all_comboboxes[6].get()
            self.TB_Value = all_comboboxes[7].get()
            self.TC_Value = all_comboboxes[8].get()
            print(self.TA_Value,self.TB_Value,self.TC_Value)
        self.values = (self.TA_Value, self.TB_Value, self.TC_Value)
        self.state=0
        self.Countdown = config_canvas4.create_text(310, 225, fill="white", font="Helvetica 38 bold",
                                        text=f"{self.TA_Value}:00")
        self.TA_Value=int(self.TA_Value)-1
        self.seconds=59
        self.after(1000, self.timer,self.Countdown,self.TA_Value)



        Oz = config_canvas4.create_text(65, 100, fill="gray", font="Helvetica 20 bold",
                                        text=f"{Ozono}ppm")
        Hu = config_canvas4.create_text(65, 155, fill="gray", font="Helvetica 20 bold",
                                        text=f"{Hum}%")
        Te = config_canvas4.create_text(65, 220, fill="gray", font="Helvetica 20 bold",
                                        text=f"{Temp}°C")
        self.after(10000, self.refresh_data)
        return()

    def timer(self,count,mins):
        global config_canvas4,test_operation_image,canva_image,Ozono,State,display,Oz, Hu, Te
        config_canvas4.itemconfigure(count, text=f"{mins}:{self.seconds}")
        self.seconds =int(self.seconds)-1
        if (self.seconds==-1):
            mins =int(mins)-1
            self.seconds = 59
            if(mins==-1):
                print("ACABE")
                config_canvas4.delete(count)
                self.state+=1
                if(self.state==1):
                    test_operation_image = Image.open("Imagenes/operacion_2.jpg")
                    test_operation_image = test_operation_image.resize((480, 280), Image.ANTIALIAS)
                    test_operation_image = ImageTk.PhotoImage(test_operation_image)
                    config_canvas4.itemconfig(canva_image, image=test_operation_image)
                    config_canvas4.image = test_operation_image
                    sensores.OZONE_ON()
                    self.Countdown = config_canvas4.create_text(310, 225, fill="white", font="Helvetica 38 bold",
                                                                text=f"{self.TB_Value}:00")
                    self.TB_Value = int(self.TB_Value) - 1
                    self.seconds = 59
                    self.after(1000, self.timer, self.Countdown, self.TB_Value)
                elif(self.state==2):
                    if (Ozono<30):
                        State="Error"
                        test_operation_image = Image.open("Imagenes/operacion_error.jpg")
                        test_operation_image = test_operation_image.resize((480, 280), Image.ANTIALIAS)
                        test_operation_image = ImageTk.PhotoImage(test_operation_image)
                        config_canvas4.itemconfig(canva_image, image=test_operation_image)
                        config_canvas4.image = test_operation_image
                        return()
                    else:
                        test_operation_image = Image.open("Imagenes/operacion_3.jpg")
                        test_operation_image = test_operation_image.resize((480, 280), Image.ANTIALIAS)
                        test_operation_image = ImageTk.PhotoImage(test_operation_image)
                        config_canvas4.itemconfig(canva_image, image=test_operation_image)
                        config_canvas4.image = test_operation_image
                        #agregar compesacion ozono
                        State="Generacion"
                        self.after(1000, self.Comp_Ozono)
                        self.Countdown = config_canvas4.create_text(310, 225, fill="white", font="Helvetica 38 bold",
                                                                    text=f"{self.TC_Value}:00")
                        self.TC_Value = int(self.TC_Value) - 1
                        self.seconds = 59
                        self.after(1000, self.timer, self.Countdown, self.TC_Value)
                elif (self.state == 3):
                    State = "Destruccion"
                    display=5
                    sensores.OZONE_OFF()
                    sensores.HUMIDIFIER_OFF()
                    test_operation_image = Image.open("Imagenes/operacion_4.jpg")
                    test_operation_image = test_operation_image.resize((480, 280), Image.ANTIALIAS)
                    test_operation_image = ImageTk.PhotoImage(test_operation_image)
                    config_canvas4.itemconfig(canva_image, image=test_operation_image)
                    config_canvas4.image = test_operation_image
                    config_canvas4.delete(Oz)
                    config_canvas4.delete(Hu)
                    config_canvas4.delete(Te)
                    Oz = config_canvas4.create_text(300,230, fill="black", font="Helvetica 20 bold",
                                                    text=f"{Ozono}ppm")
                    Hu = config_canvas4.create_text(65, 90, fill="gray", font="Helvetica 20 bold",
                                                    text=f"{Hum}%")
                    Te = config_canvas4.create_text(65, 155, fill="gray", font="Helvetica 20 bold",
                                                    text=f"{Temp}°C")
                    self.after(100, self.refresh_data2)


                return()
        if (self.seconds<10):
            self.seconds=str("0"+str(self.seconds))
        self.after(1000, self.timer,count,mins)
        return()

    def refresh_data(self):
        global Ozono, Temp, Hum,Oz,Hu,Te,config_canvas4,display
        if (display==4):
            Ozono, Temp, Hum=sensores.GET_LECTURE()
            config_canvas4.itemconfigure(Oz,text=f"{Ozono}ppm")
            config_canvas4.itemconfigure(Hu,text=f"{Hum}%")
            config_canvas4.itemconfigure(Te,text=f"{Temp}°C")
            self.after(5000, self.refresh_data)
        return()
    def refresh_data2(self):
        global Ozono, Temp, Hum, Oz, Hu, Te, config_canvas4, display,test_operation_image,canva_image,State
        if (display == 5):
            Ozono, Temp, Hum = sensores.GET_LECTURE()
            Ozono = 0.02 #BORRAR TEST VALUE
            config_canvas4.itemconfigure(Oz, text=f"{Ozono}ppm")
            config_canvas4.itemconfigure(Hu, text=f"{Hum}%")
            config_canvas4.itemconfigure(Te, text=f"{Temp}°C")

            if(Ozono<=(30*0.1) and Ozono>(30*0.01)):
                sensores.Beeper_ON()
                self.after(1000, sensores.Beeper_OFF())

            elif(Ozono<=(30*0.01)):
                sensores.Beeper_ON()
                self.after(500, sensores.Beeper_OFF())
                sensores.Beeper_ON()
                self.after(500, sensores.Beeper_OFF())
                sensores.Beeper_ON()
                self.after(500, sensores.Beeper_OFF())
                sensores.Beeper_ON()
                self.after(500, sensores.Beeper_OFF())
                sensores.Beeper_ON()
                self.after(500, sensores.Beeper_OFF())
                State = "Finalizar"
                display = 4
                test_operation_image = Image.open("Imagenes/operacion_5.jpg")
                test_operation_image = test_operation_image.resize((480, 280), Image.ANTIALIAS)
                test_operation_image = ImageTk.PhotoImage(test_operation_image)
                config_canvas4.itemconfig(canva_image, image=test_operation_image)
                config_canvas4.image = test_operation_image
                config_canvas4.delete(Oz)
                config_canvas4.delete(Hu)
                config_canvas4.delete(Te)
                Oz = config_canvas4.create_text(65, 100, fill="gray", font="Helvetica 20 bold",
                                                text=f"{Ozono}ppm")
                Hu = config_canvas4.create_text(65, 155, fill="gray", font="Helvetica 20 bold",
                                                text=f"{Hum}%")
                Te = config_canvas4.create_text(65, 220, fill="gray", font="Helvetica 20 bold",
                                                text=f"{Temp}°C")
                self.after(100, self.refresh_data)
                return()
            self.after(5000, self.refresh_data2)
        return()

    def Comp_Ozono(self):
        global Ozono,State
        while(State=="Generacion"):
            if(Ozono<30):
                sensores.OZONE_ON()
            else:
                sensores.OZONE_OFF()
            self.after(5000, self.Comp_Ozono)
            return()
        return()




    def getorigin(event,control):
        x, y = pyautogui.position()
        print(x,y)
        if (State=="Error" and x>380 and x<465 and y>250 and y<325):
            print("Reiniciando Raspberry...")
            #os.system('sudo reebot -r now')
            #os.system('sudo shutdown -r now')
            return ()
        elif(State=="Finalizar" and x>150 and x<480 and y>250 and y<325):
            print("Apagando Raspberry...")
            #os.system('sudo reebot -r now')
            #os.system('sudo shutdown -r now')
            return ()

'''
def timer(segundos,count,mins):
    global config_canvas4
    config_canvas4.itemconfigure(count, text=f"{mins}:{self.seconds}")
    self.seconds =int(self.seconds)-1
    if (self.seconds==-1):
        mins =int(mins)-1
        self.seconds = 59
        if(mins==-1):
            print("ACABE")
            config_canvas4.delete(count)
            return()
    if (self.seconds<10):
        self.seconds=str("0"+str(self.seconds))
    self.after(1000, self.timer(self.Countdown,self.TA_Value))
    return()
'''
app = App()
app.title('Sistema de desinfeccion OZONO')
app.mainloop()