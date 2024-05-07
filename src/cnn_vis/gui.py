import cv2
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QMainWindow
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap

class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()

    def initUI(self):
        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)
        self.layout = QVBoxLayout()
        self.widget.setLayout(self.layout)

        self.image_label = QLabel(self)
        self.layout.addWidget(self.image_label)

        # Update the QLabel every 40 milliseconds (25 frames per second)
        self.timer = QTimer(self)
        self.timer.setInterval(40)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start()

    def update_frame(self, frame):
        if ret:
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            p = convert_to_Qt_format.scaled(640, 480, Qt.KeepAspectRatio)
            self.image_label.setPixmap(QPixmap.fromImage(p))

    def closeEvent(self, event):
        self.video_capture.stop()
        super().closeEvent(event)