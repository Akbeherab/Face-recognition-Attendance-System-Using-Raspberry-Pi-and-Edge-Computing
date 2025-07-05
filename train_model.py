import face_recognition
import os
import pickle
import cv2

dataset_dir = "dataset"
encodings = []
names = []

print("[INFO] Starting training...")

for person in os.listdir(dataset_dir):
    person_path = os.path.join(dataset_dir, person)
    if not os.path.isdir(person_path):
        continue

    print(f"[INFO] Processing '{person}'...")

    for image_name in os.listdir(person_path):
        image_path = os.path.join(person_path, image_name)

        try:
            image = face_recognition.load_image_file(image_path)
            face_locations = face_recognition.face_locations(image)

            if not face_locations:
                print(f"[WARNING] No face found in {image_path}")
                continue

            encoding = face_recognition.face_encodings(image, face_locations)[0]
            encodings.append(encoding)
            names.append(person)

        except Exception as e:
            print(f"[ERROR] Failed to process {image_path}: {e}")

# Save encodings to a file
if encodings:
    data = {"encodings": encodings, "names": names}
    with open("encodings.pkl", "wb") as f:
        pickle.dump(data, f)
    print("[] Training completed and saved to encodings.pkl")
else:
    print("[] No encodings found. Training failed.")