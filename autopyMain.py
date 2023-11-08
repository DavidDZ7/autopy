"""
Script for a remote control car using a Raspberry Pi 3

David Norman Diaz Estrada
November 2023
"""

import RPi.GPIO as GPIO
import customtkinter
from PIL import Image, ImageTk
import picamera
import io
import threading #use threading to improve camera stream flow


#-------------------------------------------------------------------------
# GPIO configuration
#-------------------------------------------------------------------------
GPIO.setwarnings(False)
#Declare Raspberry PI 3 GPIO's according to BCM (NOT physical pin numbers)
GPIO.setmode(GPIO.BCM)

#Declare pins to control RIGHT motor
GPIO.setup(4, GPIO.OUT)  #GPIO4 is at physical pin 7
GPIO.setup(14, GPIO.OUT) #GPIO14 is at physical pin 8
#Declare pins to control LEFT motor
GPIO.setup(17, GPIO.OUT) #GPIO17 is at physical pin 11
GPIO.setup(15, GPIO.OUT) #GPIO15 is at physical pin 10
#Ensure all pins are off at start
GPIO.output(4, False)
GPIO.output(14, False)
GPIO.output(17, False)
GPIO.output(15, False)
#-------------------------------------------------------------------------



def close_app():
    app.destroy()

def go_LEFT(event):
    print('Left')
    GPIO.output(4, True) #right motor forward
    GPIO.output(14, False) #right motor forward
    GPIO.output(17, False) #left motor backward
    GPIO.output(15, True) #left motor backward

def go_RIGHT(event):
    print('Right')
    GPIO.output(4, False) #right motor backward
    GPIO.output(14, True) #right motor backward
    GPIO.output(17, True) #left motor forward
    GPIO.output(15, False) #left motor forward

def go_forward(event):
    print('Forward')
    GPIO.output(4, True) #right motor forward
    GPIO.output(14, False) #right motor forward
    GPIO.output(17, True) #left motor forward
    GPIO.output(15, False) #left motor forward

def go_reverse(event):
    print('Reverse')
    GPIO.output(4, False) #right motor backward
    GPIO.output(14, True) #right motor backward
    GPIO.output(17, False) #left motor backward
    GPIO.output(15, True) #left motor backward

def stopCar(event):
    print('Stop Car')
    GPIO.output(4, False)
    GPIO.output(14, False)
    GPIO.output(17, False)
    GPIO.output(15, False)



class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #------------------------------------------------------------------------
        #Global variables
        #------------------------------------------------------------------------
        self.title("Autopy")
        self.geometry("1250x1000+0+0")# Set the width,height of the window, and x and y coordinates
        customtkinter.set_appearance_mode("dark")#sets the window/App in dark mode
        
        #------------------------------------------------------------------------
        #GUI
        #------------------------------------------------------------------------
        #self.grid_columnconfigure(0, weight=1) # configure to expand columns horizontally
            
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        print(f"Window size: {screen_width}x{screen_height}")
        buttonsWidth=screen_width//8
        
        self.FORWARD = customtkinter.CTkButton(master=self,text="FORWARD",font=("Roboto",20), width=buttonsWidth, height=buttonsWidth, corner_radius=int(buttonsWidth*0.10))
        self.FORWARD.grid(row=0, column=1, columnspan=1,padx=10, pady=10, sticky="N")
        self.FORWARD.bind('<ButtonPress-1>',go_forward)
        self.FORWARD.bind('<ButtonRelease-1>',stopCar)
        
        self.LEFT = customtkinter.CTkButton(master=self,text="LEFT", font=("Roboto",20), width=buttonsWidth, height=buttonsWidth, corner_radius=int(buttonsWidth*0.10))
        self.LEFT.grid(row=1, column=0, padx=10, pady=10, sticky="NEW")
        self.LEFT.bind('<ButtonPress-1>',go_LEFT)
        self.LEFT.bind('<ButtonRelease-1>',stopCar)

        self.RIGHT = customtkinter.CTkButton(master=self,text="RIGHT", font=("Roboto",20), width=buttonsWidth, height=buttonsWidth, corner_radius=int(buttonsWidth*0.10))
        self.RIGHT.grid(row=1, column=2, padx=10, pady=10, sticky="NEW")
        self.RIGHT.bind('<ButtonPress-1>',go_RIGHT)
        self.RIGHT.bind('<ButtonRelease-1>',stopCar)


        self.REVERSE = customtkinter.CTkButton(master=self,text="REVERSE", font=("Roboto",20), width=buttonsWidth, height=buttonsWidth, corner_radius=int(buttonsWidth*0.10))
        self.REVERSE.grid(row=2, column=1, padx=10, columnspan=1, pady=10, sticky="N")
        self.REVERSE.bind('<ButtonPress-1>',go_reverse)
        self.REVERSE.bind('<ButtonRelease-1>',stopCar)

        self.closeApp = customtkinter.CTkButton(master=self,text="Close App", font=("Roboto",20), width=buttonsWidth,height=buttonsWidth//2)
        self.closeApp.grid(row=3, column=0,columnspan=3, padx=10, pady=(40,10), sticky="NEW")
        self.closeApp.configure(command=close_app)

        #CAMERA
        self.camera = picamera.PiCamera()
        self.camera.resolution = (640, 480)
        self.camera.vflip = True
        self.camera.framerate = 30  # Adjust as needed
        
        self.label = customtkinter.CTkLabel(master=self)
        self.label.grid(row=0, column=3,rowspan=3,columnspan=3, padx=10, pady=10, sticky="NEW")
        
        self.stream = io.BytesIO()
        self.update_thread = threading.Thread(target=self.updateCameraLoop)
        self.update_thread.daemon = True
        self.update_thread.start()

    def updateCameraLoop(self):
        for _ in self.camera.capture_continuous(self.stream, format='jpeg', use_video_port=True):
            self.stream.seek(0)
            image = Image.open(self.stream)
            
            photo = customtkinter.CTkImage(dark_image=image, size=(640, 480))
            self.label.configure(image=photo, text="")
            self.label.image = photo
    
            self.stream.seek(0)
            self.stream.truncate()


app = App()
app.mainloop()
