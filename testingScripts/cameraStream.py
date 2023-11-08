import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import picamera
import io
import threading #use threading to improve camera stream flow

class CameraApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        
        self.camera = picamera.PiCamera()
        self.camera.resolution = (640, 480)
        self.camera.vflip = True
        self.camera.framerate = 30  # Adjust as needed
        
        self.label = tk.Label(self.window)
        self.label.pack()
        
        self.stream = io.BytesIO()
        self.update_thread = threading.Thread(target=self.update_loop)
        self.update_thread.daemon = True
        self.update_thread.start()

        self.window.mainloop()

    def update_loop(self):
        for _ in self.camera.capture_continuous(self.stream, format='jpeg', use_video_port=True):
            self.stream.seek(0)
            image = Image.open(self.stream)
            photo = ImageTk.PhotoImage(image)
            self.label.config(image=photo)
            self.label.image = photo
            self.stream.seek(0)
            self.stream.truncate()

if __name__ == "__main__":
    root = tk.Tk()
    app = CameraApp(root, "Camera Stream")
