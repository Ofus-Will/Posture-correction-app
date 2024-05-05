import cv2
# import tkinter as tk
from tkinter import ttk

# grab all available video capture device ports according to cv2
def get_cam_ports():
    available_ports = []
    out_of_range = False
    port_index = 0

    while out_of_range == False:
        camera = cv2.VideoCapture(port_index)
        if camera.isOpened():
            camera.release()
            available_ports.append(port_index)
        else:
            out_of_range = True
        port_index += 1
        
    return available_ports

# widget for switching between available cameras
class CameraSelector(ttk.Combobox):
    def __init__(self, parent, app):
        ports = get_cam_ports()
        port_names = [f"Camera {port + 1}" for port in ports]

        super().__init__(parent, state='readonly', values=port_names)
        self.current(0)
        
        self.app = app

        self.bind("<<ComboboxSelected>>", lambda event: self.select_port())

    # switch between available cameras from the combo box
    def select_port(self):
        index = self.get().split(" ")[1]
        self.app.set_camera_port(int(index) - 1)