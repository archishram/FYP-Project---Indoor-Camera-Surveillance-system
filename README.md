# FYP-Project---Indoor-Camera-Surveillance-system




Guide to use the system:
Users will be able to use their own webcam or the stock videos provided in the GitHub repository.

The idea of using these stock videos is to simulate the usage of the surveillance system in different scenarios and the users can simulate this by changing the value of cv2.VideoCapture( ) inside the class CameraDetection in the camera_detection.py file to the path of the video or the value 0 if they want to use their own webcam.

def start_camera(self):
        if self.cap is None:
            self.cap = cv2.VideoCapture("C:\\Users\\archi\\Pictures\\FYP Videos\\WhatsApp Video 2024-09-02 at 00.28.50_2cb4ff63.mp4")
        self.camera_on = True
        self.app.toggle_button.config(text="Stop Camera")
        self.update_video() 
The value of cv2.VideoCapture( ) is to be changed inside this function.
