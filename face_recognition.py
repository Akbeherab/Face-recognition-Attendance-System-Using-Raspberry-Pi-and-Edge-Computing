import cv2
import pickle
import os
import time

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trained_model.yml")
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

with open("student_labels.pkl", "rb") as f:
    labels = pickle.load(f)
    labels = {v: k for k, v in labels.items()}

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        id_, confidence = recognizer.predict(roi_gray)
        if confidence < 60:
            name = labels[id_]
            cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            with open("attendance.txt", "a") as f:
                f.write(f"{name},{time.ctime()}\n")
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()
