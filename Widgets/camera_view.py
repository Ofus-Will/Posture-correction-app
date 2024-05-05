import tkinter as tk
from tkinter import ttk

import mediapipe as mp
import cv2
from PIL import Image, ImageTk

class CameraView(ttk.Frame):
    def __init__(self, parent, app, page_class, subpage=0, width=600, height=480, landmarks=True, static=False):
        super().__init__(parent)
        self.app = app
        self.page_class = page_class

        self.width = width
        self.height = height
        self.static = static # Might not need, keep for future proof sake
        self.landmarks = landmarks
        self.subpage = subpage

        # handles exiting the recursive loop when updates no longer needed
        self.break_loop = False
        self.landmark_bool = tk.BooleanVar(value=False)

        self.init_ui()
        self.app.process_camera()
        self.update_view()

    # initialise all the widgets sub widgets
    def init_ui(self):
        self.lbl_image = ttk.Label(self)
        self.lbl_image.configure(background="red")
        self.lbl_image.pack()

        self.btn_landmarks = ttk.Checkbutton(self, text="Show landmarks", variable=self.landmark_bool)
        self.btn_landmarks.pack(expand=True, pady=(5,0))
    
    # called recursively, updates the camera view, drawing on mediapipe pose landmarks if conditions are met
    def update_view(self):
        page = self.app.get_current_page()
        bool_correct_page = isinstance(page, self.page_class)
        bool_valid_subpage = (hasattr(page, 'get_subpage') and self.subpage != page.get_subpage()) == False
        # print(bool_valid_subpage)
        if bool_correct_page and bool_valid_subpage:
            if self.app.state() != "iconic":
                if self.app.camera_handler.shared_frame is None:
                    print("shared frame is none")
                    return

                frame = self.app.camera_handler.shared_frame

                if (self.landmark_bool.get() and self.app.camera_handler.shared_landmarks):
                    mp.solutions.drawing_utils.draw_landmarks(frame, self.app.camera_handler.shared_landmarks, self.app.mp_pose.POSE_CONNECTIONS, landmark_drawing_spec=self.app.drawing_spec)

                frame_resized = cv2.resize(frame, (self.width, self.height))
                img_pil = Image.fromarray(frame_resized)
                img = ImageTk.PhotoImage(image=img_pil)

                self.lbl_image.imgtk = img 
                self.lbl_image.configure(image=img)

            if self.static == False and self.break_loop == False:
                self.after(50, self.update_view)