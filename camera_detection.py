import cv2
import os
import datetime
import math
import winsound
from PIL import Image, ImageTk
from ultralytics import YOLO
from tkinter import filedialog

class CameraDetection:
    def __init__(self, app):
        self.app = app
        self.model = YOLO("best.pt")
        self.cap = None
        self.camera_on = False
        self.recording = False
        self.out = None
        self.no_detection_time = 0

    def toggle_camera(self):
        if self.camera_on:
            self.stop_camera()
        else:
            self.start_camera()

    def start_camera(self):
        if self.cap is None:
            self.cap = cv2.VideoCapture("C:\\Users\\archi\\Pictures\\FYP Videos\\WhatsApp Video 2024-09-02 at 00.28.50_2cb4ff63.mp4")
        self.camera_on = True
        self.app.toggle_button.config(text="Stop Camera")
        self.update_video()

    def stop_camera(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        self.camera_on = False
        self.app.toggle_button.config(text="Start Camera")
        self.app.video_label.config(image='')
        self.app.status_label.config(text="No detections", fg="green")
        self.app.recording_label.config(text="Recording: Off", fg="blue")
        self.app.root.config(bg="SystemButtonFace")
        if self.recording:
            self.stop_recording()

    def start_recording(self, frame):
        if not self.recording:
            self.recording = True
            self.app.recording_label.config(text="Recording: On", fg="red")
            video_filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".avi"
            self.out = cv2.VideoWriter(video_filename, cv2.VideoWriter_fourcc(*'XVID'), 20.0, (frame.shape[1], frame.shape[0]))

    def stop_recording(self):
        if self.recording:
            self.recording = False
            self.app.recording_label.config(text="Recording: Off", fg="blue")
            if self.out is not None:
                self.out.release()
                self.out = None

    def update_video(self):
        if self.camera_on and self.cap is not None:
            ret, frame = self.cap.read()
            if ret:
                results = self.model(frame)
                detected = []
                detection_text = ""

                # YOLO object detection
                for r in results:
                    boxes = r.boxes
                    for box in boxes:
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        conf = math.ceil((box.conf[0] * 100)) / 100
                        cls = int(box.cls[0])
                        currentClass = None

                        if cls == 0 and conf > 0.3:
                            currentClass = "person"
                        elif cls == 16 and conf > 0.3:
                            currentClass = "dog"
                        elif cls == 15 and conf > 0.3:
                            currentClass = "cat"

                        if currentClass:
                            if currentClass not in detected:
                                detected.append(currentClass)
                            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                # Face recognition (calls the face recognition module)
                self.app.face_recognition_module.process_frame(frame, detected)

                if detected:
                    detection_text = ", ".join([item.capitalize() for item in detected]) + " detected!"
                    self.app.status_label.config(text=detection_text, fg="red")
                    self.app.root.config(bg="red")
                    winsound.Beep(1000, 500)
                    self.start_recording(frame)
                    self.no_detection_time = 0
                else:
                    self.app.status_label.config(text="No detections", fg="green")
                    self.app.root.config(bg="SystemButtonFace")
                    if self.recording:
                        self.no_detection_time += 1
                        if self.no_detection_time > 150:  # Stop recording after 15 seconds with no detection
                            self.stop_recording()
                            self.no_detection_time = 0

                if self.recording:
                    self.out.write(frame)

                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(frame_rgb)
                photo = ImageTk.PhotoImage(image=image)
                self.app.video_label.config(image=photo)
                self.app.video_label.image = photo

            self.app.root.after(100, self.update_video)

    def view_videos(self):
        file_path = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Video File", filetypes=[("Video Files", "*.avi")])
        if file_path:
            os.startfile(file_path)

    def __del__(self):
        if self.cap is not None:
            self.cap.release()
        if self.recording:
            self.stop_recording()
