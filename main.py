import cv2
import threading
from playsound import playsound
import os
import numpy as np

def load_classifier(path, name):
    classifier = cv2.CascadeClassifier(path)
    if classifier.empty():
        raise ValueError(f"Error: Unable to load {name} classifier from {path}")
    return classifier

def play_alarm():
    global alarm_triggered
    try:
        playsound('alarm.mp3')
    except Exception as e:
        print(f"Error playing alarm: {e}")
    finally:
        alarm_triggered = False

# Initialize global variables
alarm_triggered = False
frame_saved = False
detection_counter = 0
DETECTION_THRESHOLD = 3  # Reduced from 5 to 3

def is_valid_detection(x, y, w, h, frame_height, frame_width):
    """
    Filter out invalid detections based on size and position
    """
    # Relaxed size thresholds
    MIN_WIDTH = frame_width // 12  # Reduced from 8 to 12
    MIN_HEIGHT = frame_height // 12  # Reduced from 8 to 12
    
    # Relaxed maximum size thresholds
    MAX_WIDTH = frame_width * 0.9  # Increased from 0.8 to 0.9
    MAX_HEIGHT = frame_height * 0.9
    
    # Size check
    if w < MIN_WIDTH or h < MIN_HEIGHT:
        return False
    if w > MAX_WIDTH or h > MAX_HEIGHT:
        return False
    
    # Relaxed aspect ratio check
    aspect_ratio = h / w
    if aspect_ratio < 1.0 or aspect_ratio > 4.0:  # Widened range from (1.2, 3.0)
        return False
    
    return True

def main():
    try:
        # Load Haar Cascade classifiers with error handling
        body_classifier = load_classifier("haarcascade_fullbody.xml", "body")
        face_classifier = load_classifier("haarcascade_frontalface_default.xml", "face")

        # Choose the input source
        print("Choose the input source:")
        print("1. Video File")
        print("2. Laptop Camera")
        choice = input("Enter your choice (1/2): ")

        if choice == "1":
            video_source = input("Enter the path to the video file: ")
            if not os.path.exists(video_source):
                raise ValueError("Video file not found")
        elif choice == "2":
            video_source = 0  # Default laptop camera
        else:
            raise ValueError("Invalid choice")

        # Open video source
        cap = cv2.VideoCapture(video_source)
        if not cap.isOpened():
            raise ValueError("Failed to open video source")

        global alarm_triggered, frame_saved, detection_counter

        # Get frame dimensions
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("End of video or unable to access camera.")
                break

            # Preprocessing
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (5, 5), 0)

            # More relaxed detection parameters
            bodies = body_classifier.detectMultiScale(
                gray,
                scaleFactor=1.05,     # Reduced from 1.1 to 1.05
                minNeighbors=3,       # Reduced from 5 to 3
                minSize=(60, 120),    # Reduced minimum size
                maxSize=(400, 800)    # Increased maximum size
            )

            faces = face_classifier.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=4,       # Reduced from 5 to 4
                minSize=(20, 20),     # Reduced minimum size
                maxSize=(200, 200)    # Increased maximum size
            )

            # Process detections
            valid_detections = []
            
            # Process body detections
            for detection in bodies:
                x, y, w, h = detection
                if is_valid_detection(x, y, w, h, frame_height, frame_width):
                    valid_detections.append(detection)

            # Process face detections
            for detection in faces:
                x, y, w, h = detection
                if is_valid_detection(x, y, w, h, frame_height, frame_width):
                    valid_detections.append(detection)

            # Handle valid detections
            if len(valid_detections) > 0:
                detection_counter += 1
            else:
                detection_counter = max(0, detection_counter - 1)

            # Only trigger alarm if we have consistent detections
            if detection_counter >= DETECTION_THRESHOLD:
                for (x, y, w, h) in valid_detections:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    cv2.putText(frame, "Intrusion Detected", (x, y - 10), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                    if not alarm_triggered:
                        alarm_triggered = True
                        alarm_thread = threading.Thread(target=play_alarm)
                        alarm_thread.daemon = True
                        alarm_thread.start()

                    if not frame_saved:
                        try:
                            cv2.imwrite("intruder.jpg", frame)
                            print("Intrusion frame saved as 'intruder.jpg'")
                            frame_saved = True
                        except Exception as e:
                            print(f"Error saving frame: {e}")

            # Show video feed with detection counter
            cv2.putText(frame, f"Detection Confidence: {detection_counter}/{DETECTION_THRESHOLD}", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Draw all potential detections in yellow (for debugging)
            for (x, y, w, h) in bodies:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 1)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 1)
            
            cv2.imshow("Intrusion Detection System", frame)

            # Exit the loop on 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Release resources
        if 'cap' in locals():
            cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()