import cv2
import dlib
import numpy as np

# Load DNN-based face detector and Haar Cascade
detector = dlib.get_frontal_face_detector()
haar_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Create a VideoCapture object
cap = cv2.VideoCapture(0)

# Initialize the tracker
tracker = dlib.correlation_tracker()
tracking_face = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if tracking_face:
        # Update the tracker and get the updated position
        tracker.update(frame)
        pos = tracker.get_position()
        x, y, w, h = int(pos.left()), int(pos.top()), int(pos.width()), int(pos.height())
    else:
        # Convert the frame to grayscale for Haar Cascade detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = haar_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(faces) > 0:
            # Start tracking the first detected face
            x, y, w, h = faces[0]
            tracker.start_track(frame, dlib.rectangle(x, y, x + w, y + h))
            tracking_face = True
        else:
            x, y, w, h = 0, 0, 0, 0

    if tracking_face or len(faces) > 0:
        # Crop and blur the detected face region
        face_region = frame[y:y + h, x:x + w]
        blur_value = int(min(w, h) / 3) | 1  # Ensure blur value is odd
        sigma = 1000
        blurred_face = cv2.GaussianBlur(face_region, (blur_value, blur_value), sigma)
        frame[y:y + h, x:x + w] = blurred_face

    # Display the frame
    cv2.imshow('Enhanced Face Detection and Blurring', frame)

    # Break the loop when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Reset tracking if no face is detected
    if not tracking_face:
        tracker = dlib.correlation_tracker()

# Release the VideoCapture
cap.release()
cv2.destroyAllWindows()
