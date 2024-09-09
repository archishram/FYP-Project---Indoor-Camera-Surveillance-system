import tkinter as tk
from camera_detection import CameraDetection
from face_recognition_module import FaceRecognition

class VideoCaptureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Monitor")

        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.video_frame = tk.Frame(self.main_frame)
        self.video_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.video_label = tk.Label(self.video_frame)
        self.video_label.pack()

        self.alert_frame = tk.Frame(self.main_frame)
        self.alert_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.toggle_button = tk.Button(self.alert_frame, text="Start Camera", command=self.toggle_camera)
        self.toggle_button.pack(pady=10)

        self.status_label = tk.Label(self.alert_frame, text="No detections", fg="green", font=("Arial", 14))
        self.status_label.pack(pady=10)

        self.recording_label = tk.Label(self.alert_frame, text="Recording: Off", fg="blue", font=("Arial", 12))
        self.recording_label.pack(pady=10)

        self.videos_button = tk.Button(self.alert_frame, text="View Recorded Videos", command=self.view_videos)
        self.videos_button.pack(pady=10)

        # Initialize the detection and face recognition modules
        self.camera_detection = CameraDetection(self)
        self.face_recognition_module = FaceRecognition()

    def toggle_camera(self):
        self.camera_detection.toggle_camera()

    def start_camera(self):
        self.camera_detection.start_camera()

    def stop_camera(self):
        self.camera_detection.stop_camera()

    def update_video(self):
        self.camera_detection.update_video()

    def start_recording(self, frame):
        self.camera_detection.start_recording(frame)

    def stop_recording(self):
        self.camera_detection.stop_recording()

    def view_videos(self):
        self.camera_detection.view_videos()

    def __del__(self):
        self.camera_detection.__del__()

root = tk.Tk()
app = VideoCaptureApp(root)
root.mainloop()
