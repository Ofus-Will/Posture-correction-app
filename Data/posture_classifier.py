import math
from Pages.monitoring import MonitoringPage

class PostureClassifier():

    def __init__(self, app, buffer_size = 5, visibility_threshold = 0.9, distance_limit=0.20) -> None:
        self.app = app
        self.classification = ""
        self.distance_limit = distance_limit
        self.buffer_size = buffer_size
        self.visibility_threshold = visibility_threshold
        self.consecutive_bad_frames = 0

    # analyse current camera feed and classify the extracted landmarks as either goor or bad comparatively to stored landmarks
    def update_classification(self) -> None:
        self.curr_posture = self.app.data_handler.process_data()

        if self.curr_posture != None:
            (good_posture, bad_posture) = (self.app.data_handler.good_posture, self.app.data_handler.bad_posture)
            if good_posture is {} or bad_posture is []:
                return
            
            all_distances = [self.euclidean_distance(good_posture)] + [self.euclidean_distance(posture) for posture in bad_posture]
            closest_distance, closest_posture = min((dist, posture) for dist, posture in zip(all_distances, ['Good'] + ['Bad']*len(bad_posture)))

            if closest_posture == "Good" and closest_distance <= self.distance_limit:
                self.consecutive_bad_frames = 0
                self.classification = "Good"
            else:
                self.consecutive_bad_frames += 1
                if self.consecutive_bad_frames >= self.buffer_size:
                    self.classification = "Bad"
                    self.notify_user()

            self.app.session_handler.update_frame_count(self.classification)
        else:
            self.app.show_notification("We can not find you in your camera!")
            self.app.toggle_monitoring()


    # square root of the sum of all euclidean distances between posture datasets
    # possibly remove square root since iirc i'm just using value comparatively?
    def euclidean_distance(self, to_compare) -> float:
        distance_sum = 0
        common_indices = set(self.curr_posture.keys()) & set(to_compare.keys())

        for index in common_indices:
            distance_sum += (self.curr_posture[index] - to_compare[index]) ** 2

        return math.sqrt(distance_sum)
    
    # the recursive main loop that occurs when the app is in monitoring mode, reclassifying the posture every frame
    def classify_posture(self, first_call=False) -> None:
        if self.app.monitoring == True:

            if first_call:
                self.app.process_camera(False)

            self.update_classification()

            if isinstance(self.app.current_page, MonitoringPage) and self.app.state() != "iconic":
                self.app.current_page.update_ui()

            self.app.after(200, self.classify_posture)

    # method for notifying the user when their posture is bad, called in update_classification method
    def notify_user(self):
        if self.app.settings_handler.get_setting("alert_mode") == "Notification":
            self.app.show_notification(text="Bad Posture Detected - Adjust your posture!", windows=True)
