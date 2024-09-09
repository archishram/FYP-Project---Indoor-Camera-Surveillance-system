import face_recognition
import numpy as np
import cv2

class FaceRecognition:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []
        self.load_faces()
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.process_this_frame = True

    def load_faces(self):
        # Add your face images and encodings here
        neha_image = face_recognition.load_image_file("me.jpg")
        neha_face_encoding = face_recognition.face_encodings(neha_image)[0]

        srk_image = face_recognition.load_image_file("me2.jpg")
        srk_face_encoding = face_recognition.face_encodings(srk_image)[0]

        self.known_face_encodings = [
            neha_face_encoding,
            srk_face_encoding
        ]
        self.known_face_names = [
            "owner",
            "owmer 2"
        ]

    def process_frame(self, frame, detected):
        if self.process_this_frame:
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            self.face_locations = face_recognition.face_locations(rgb_small_frame)
            self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

            self.face_names = []
            for face_encoding in self.face_encodings:
                face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)

                if face_distances[best_match_index] < 0.6:
                    name = self.known_face_names[best_match_index]
                else:
                    name = "Unknown"

                self.face_names.append(name)

        self.process_this_frame = not self.process_this_frame

        for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            if name != "Unknown" and name not in detected:
                detected.append(name)
