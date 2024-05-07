import cv2
from threading import Thread, Lock
import time

class ThreadedVideoCapture:
    def __init__(self, video_source=0):
        self.cap = cv2.VideoCapture(video_source)
        if not self.cap.isOpened():
            raise ValueError("Unable to open video source", video_source)
        self.ret = False
        self.frame = None
        self.stopped = False
        self.lock = Lock()

    def start(self):
        """
        Starts the thread to read frames from the video source.
        """
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()
        return self

    def update(self):
        """
        Continuously captures frames from the video source in a loop until stopped.
        """
        while True:
            if self.stopped:
                return
            ret, frame = self.cap.read()
            with self.lock:
                self.ret = ret
                self.frame = frame
                if not ret:
                    self.stop()

    def read(self):
        """
        Returns the latest frame captured.
        """
        with self.lock:
            return self.ret, self.process_frame(self.frame.copy()) if self.frame is not None else None

    def process_frame(self, frame):
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    def stop(self):
        """
        Stops the video capture.
        """
        self.stopped = True
        self.cap.release()

    def __del__(self):
        self.stop()
