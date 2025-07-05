import cv2
import os
import time

name = input("Enter your name: ").strip()
folder = f"dataset/{name}"
os.makedirs(folder, exist_ok=True)

cap = cv2.VideoCapture(0)
count = 0

print("Starting camera...")

# Warm-up time for camera
time.sleep(2)

while count < 10:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    img_path = os.path.join(folder, f"{count}.jpg")
    cv2.imwrite(img_path, frame)
    print(f"[INFO] Saved {img_path}")
    count += 1

    # Show preview
    cv2.imshow("Capturing Faces", frame)
    cv2.waitKey(500)  # Show for half a second

    time.sleep(1)  # Wait 1 second before next capture

cap.release()
cv2.destroyAllWindows()

print(" Capture complete: 10 images saved.")