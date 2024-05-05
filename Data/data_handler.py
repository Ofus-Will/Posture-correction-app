import os
from pathlib import Path
import csv
import math
from typing import Dict, Tuple

class DataHandler():
    def __init__(self, app):
        self.app = app
        self.minimum_landmarks = 6
        self.good_posture = {}
        self.bad_posture = []

        # paths to where the posture data is store on system 
        self.app_directory = Path(os.getenv("LOCALAPPDATA")) / "Posture Correction"
        self.bad_path = self.app_directory / "Bad Posture Data"
        self.good_path = self.app_directory / "good_posture.csv"

        self.bad_path.mkdir(parents=True, exist_ok=True)

        self.read_to_memory()

    # get the raw landmark data from the shared landmarks while filtering non-visible and unneeded ones
    def get_raw_data(self) -> Dict[int, Tuple[float, float, float]]:
        data = self.app.camera_handler.shared_landmarks
        filter = [0, 1, 3, 4, 6, 7, 8, 9, 10]
        if data:
            to_return = {}
            for i, landmark in enumerate(data.landmark):
                if (landmark.visibility > self.app.posture_classifier.visibility_threshold) and i not in filter:
                    to_return[i] = (landmark.x, landmark.y, landmark.z)

            if len(to_return) < self.minimum_landmarks:
                self.app.show_notification("We can not get enough data from your camera, try moving it back!")

            return to_return
        
        else:
            self.app.show_notification("The app seems to be struggling to process your data!")
    
    # process the raw data, put it in a form applicable to my algorithm
    # ready to be written to file or compare current posture to posture data on file
    def process_data(self, write_to_file=False, good_instance=True) -> Dict[int, float]:
        if write_to_file:
            self.app.camera_handler.process_camera(False)

        data = self.get_raw_data()

        if data != None:

            l_shoulder = data[11]
            r_shoulder = data[12]

            mid_x = (l_shoulder[0] + r_shoulder[0]) / 2 
            mid_y = (l_shoulder[1] + r_shoulder[1]) / 2
            mid_z = (l_shoulder[2] + r_shoulder[2]) / 2

            processed_data = {}
            
            for index, coordinates in data.items():
                x, y, z = coordinates
                dist_from_origin = math.sqrt((x - mid_x) ** 2 + (y - mid_y) ** 2 + (z - mid_z) ** 2)
                processed_data[index] = dist_from_origin

            if write_to_file:
                self.write_to_file(processed_data, good_instance)

            return processed_data

    # write the processed data to its allocated file
    def write_to_file(self, data, good_instance=True) -> None:
        if good_instance:
            file_path = self.good_path
        else:
            app_directory = self.bad_path
            next_index = len(os.listdir(app_directory)) + 1
            file_path = app_directory / f"bad_posture_{next_index}.csv"

        if data:
            with open(file_path, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Index", "Distance from origin"])
                for index, distance in data.items():
                    writer.writerow([index, distance])

            self.app.show_notification("Successfully saved posture data!", background="#5cb85c")

            self.read_to_memory()

    # read the posture data from file to program memory
    def read_to_memory(self) -> None:

        self.good_posture = self.read_from_file(self.good_path)

        for file_name in os.listdir(self.bad_path):
            file_path = os.path.join(self.bad_path, file_name)
            bad_posture = self.read_from_file(file_path)
            self.bad_posture.append(bad_posture)

    # called in above method, for each individual file
    def read_from_file(self, file_path) -> Dict[int, float]:
        landmark_data = {}
        if os.path.exists(file_path) and os.path.isfile(file_path):
            with open(file_path, "r") as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    index = int(row[0])
                    distance = float(row[1])
                    landmark_data[index] = distance 
        return landmark_data
    
    # ensure that the posture data exists if not alert the user 
    def check_for_data(self) -> bool:
        if self.good_posture == {} or self.bad_posture == []:
            self.app.show_notification("You have not calibrated the posture detection system yet!")
            return False 
        elif hasattr(self.app, "notification") and self.app.notification != None:
            if(self.app.notification.text == "You have not calibrated the posture detection system yet!"):
                self.app.notification.destroy()
        return True
    
    # delete the stored data, called by posture sub pages
    def delete_data(self, type):
        if type == "good":
            if os.path.exists(self.good_path):
                os.remove(self.good_path)
                self.good_posture = {}
            self.app.show_notification("Successfully deleted all good posture data!", background="#5cb85c")

        elif type== "bad":
            for file_name in os.listdir(self.bad_path):
                file_path = os.path.join(self.bad_path, file_name)
                os.remove(file_path)
            self.bad_posture = []

            self.app.show_notification("Successfully deleted all bad posture data!", background="#5cb85c")


        