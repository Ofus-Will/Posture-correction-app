from datetime import datetime
import os
from pathlib import Path
import json
from typing import List

class SessionHandler():
    def __init__(self, app, file_name="sessions_data.json") -> None:
        self.app = app 
        self.file_name = Path(os.getenv("LOCALAPPDATA")) / "Posture Correction" / file_name

        self.sessions = self.get_sessions()

        self.reset_session()

    # initiate the monitoring session if one doesn't exist already
    def start_session(self) -> None:
        if self.start_time is not None:
            return False
        self.start_time = datetime.now()
        return True

    # end the monitoring session if one is in progress
    def end_session(self) -> None:
        if self.start_time is None:
            print("There is not currently a session in progress!")
            return False
        
        self.end_time = datetime.now()
        self.duration = (self.end_time - self.start_time).seconds
        self.record_session()

        return True

    # called from the posture classifier, tracks cumulative bad and good frames for data analytics
    def update_frame_count(self, classification: str) -> None:
        if classification == "Good":
            self.good_frame_count += 1
        elif classification == "Bad":
            self.bad_frame_count += 1

    # reset all the data when the session is recorded
    def reset_session(self) -> None:
        self.start_time = None 
        self.end_time = None
        self.duration = None
        self.good_frame_count = 0
        self.bad_frame_count = 0 

    # delete all session data assuming any exists
    def delete_sessions(self) -> bool:
        if os.path.exists(self.file_name):
            os.remove(self.file_name)
            self.sessions = []
            return True
        return False

    # get all sessions from file
    def get_sessions(self) -> List[dict[str, str, int, int, int]]:

        if os.path.exists(self.file_name):
            with open(self.file_name, "r") as file:
                data = file.read()
                if data:
                    return json.loads(data)
            
        return []

    # record a session once the session is ended
    def record_session(self) -> None:
        session = {
            "start_time": self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "end_time": self.end_time.strftime("%Y-%m-%d %H:%M:%S"),
            "duration": self.duration,
            "good_frame_count": self.good_frame_count,
            "bad_frame_count": self.bad_frame_count
        }

        if None not in session.values():
            self.sessions = self.get_sessions()
            self.sessions.append(session)
            self.save_sessions()
            self.reset_session()

    # update the sessions json file
    def save_sessions(self) -> None:
        os.makedirs(self.file_name.parent, exist_ok=True)
        temp_file = self.file_name.with_suffix('.tmp')
        with open(temp_file, "w") as file:
            json.dump(self.sessions, file, indent=4)
        os.replace(temp_file, self.file_name)
        self.reset_session()