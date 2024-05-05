import cv2 
# import mediapipe as mp
from Widgets.camera_view import CameraView

class CameraHandler():
    def __init__(self, app):
        self.app = app
        self.shared_frame = None 
        self.shared_landmarks = None
        self.subscribed = False

    # retrieve the frame and landmarks from the current capture device during monitoring, handling other edge cases
    def process_camera(self, recursive: bool = True) -> None:
        returned, frame = self.app.cap.read()
        if frame is None:
            self.app.show_notification("Camera In Use! - Another application is using your camera, please free up the camera and restart!", windows=True)

        if not returned:
            return
        
        if not self.subscribed:
            self.subscribed = True

        frame = self.process_frame(frame)
        camera_view = self.get_camera_view()

        bool_camera_view = camera_view is not None
        bool_monitoring = (self.app.monitoring == True) 
        bool_landmarks = bool_camera_view and camera_view.landmark_bool.get() == True

        if bool_monitoring or (bool_landmarks and self.app.state() != "iconic") or not recursive:
            results = self.app.pose.process(frame)
            if results.pose_landmarks:
                self.shared_landmarks = results.pose_landmarks
        elif self.shared_landmarks is not None:
            self.shared_landmarks = None
        self.shared_frame = frame

        if bool_monitoring and self.app.session_handler.start_time is None:
            self.app.session_handler.start_session()

        if recursive and self.subscribed and (bool_camera_view or bool_monitoring):
            self.app.after(75, self.process_camera)
        else:
            self.subscribed = False

    # get the camera view from the current page if one exists
    def get_camera_view(self) -> CameraView:
        camera_view = None
        page = self.app.current_page
        if hasattr(page, "camera_view"):
            camera_view = page.camera_view
        elif hasattr(page, "current_subpage") and hasattr(page.current_subpage, "camera_view"):
            camera_view = page.current_subpage.camera_view

        return camera_view

    # process the frame before displaying and/or extracting data
    def process_frame(self, frame):
        processed_frame = cv2.flip(frame, 1)
        processed_frame_rgb = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
        return processed_frame_rgb