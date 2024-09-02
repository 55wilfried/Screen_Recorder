import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QToolBar, QAction, QFileDialog
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, QTimer
import pyautogui
import numpy as np
import cv2



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Screen Recorder with Web Browser")  # Set the window title
        self.setGeometry(200, 200, 1280, 720)  # Set the window size and position

        # Create a QWebEngineView to display a web browser inside the application
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))  # Load Google as the default webpage

        # Create a layout to manage the placement of widgets in the window
        layout = QVBoxLayout()
        layout.addWidget(self.browser)  # Add the browser widget to the layout

        # Create a container widget to hold the layout
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)  # Set the container as the central widget of the main window

        # Create a toolbar to hold actions for starting and stopping the screen recording
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        # Create "Start Recording" action and connect it to the start_recording method
        start_action = QAction("Start Recording", self)
        start_action.triggered.connect(self.start_recording)
        toolbar.addAction(start_action)  # Add the action to the toolbar

        # Create "Stop Recording" action and connect it to the stop_recording method
        stop_action = QAction("Stop Recording", self)
        stop_action.triggered.connect(self.stop_recording)
        toolbar.addAction(stop_action)  # Add the action to the toolbar

        # Create a QTimer to capture screen frames at intervals
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.record_frame)  # Connect the timer to the record_frame method

        # Variables to manage the recording state and video writer
        self.is_recording = False
        self.out = None

    def start_recording(self):
        # Method to start screen recording
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Recording", "", "Video Files (*.avi *.mp4)")
        if file_path:
            # If a file path is selected, initialize the video writer with the chosen path and settings
            self.out = cv2.VideoWriter(file_path, cv2.VideoWriter_fourcc(*'XVID'), 10, pyautogui.size())
            self.is_recording = True  # Set the recording state to True
            self.timer.start(100)  # Start the timer to capture frames every 100ms

    def record_frame(self):
        # Method to capture and save a single frame of the screen
        if self.is_recording:
            img = pyautogui.screenshot()  # Take a screenshot using pyautogui
            frame = np.array(img)  # Convert the screenshot to a numpy array
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert the image from BGR to RGB format
            self.out.write(frame)  # Write the frame to the video file

    def stop_recording(self):
        # Method to stop screen recording
        self.is_recording = False  # Set the recording state to False
        self.timer.stop()  # Stop the timer
        if self.out:
            self.out.release()  # Release the video writer resource

# Initialize the application and create the main window
app = QApplication(sys.argv)
window = MainWindow()
window.show()  # Show the main window
sys.exit(app.exec_())  # Start the application's event loop
