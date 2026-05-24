import cv2
import os
import numpy as np
import pickle

def train_model():
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    dataset_path = "dataset/"
    faces, ids = [], []
    labels = {}
    label_id = 0

    for root, _, files in os.walk(dataset_path):
        for file in files:
            if file.endswith(".jpg"):
                path = os.path.join(root, file)
                label = os.path.basename(root)
                if label not in labels:
                    labels[label] = label_id
                    label_id += 1
                id_ = labels[label]
                img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                faces_detected = face_cascade.detectMultiScale(img, 1.3, 5)
                for (x, y, w, h) in faces_detected:
                    roi = img[y:y+h, x:x+w]
                    faces.append(roi)
                    ids.append(id_)
    recognizer.train(faces, np.array(ids))
    recognizer.save("trained_model.yml")
    with open("student_labels.pkl", "wb") as f:
        pickle.dump(labels, f)

if __name__ == "__main__":
    train_model()
