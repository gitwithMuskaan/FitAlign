import cv2
import mediapipe as mp
import math as m
import pygame


# Function to calculate distance between two points
def findDistance(x1, y1, x2, y2):
    return m.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# Function to calculate angle between three points
def calculate_angle(a, b, c):
    # Calculate the angle using cosine law
    ang = m.degrees(
        m.atan2(c[1] - b[1], c[0] - b[0]) - m.atan2(a[1] - b[1], a[0] - b[0])
    )
    return abs(ang)


# Function to play a warning sound
def sendWarning():
    pygame.mixer.init()
    pygame.mixer.music.load("warning.mp3")
    pygame.mixer.music.play()


# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Video capture
cap = cv2.VideoCapture(0)

# Select exercise
exercise = input("Select exercise (squats, pushups, lunges): ").lower()

# Track frames for posture
good_frames = 0
bad_frames = 0
fps = cap.get(cv2.CAP_PROP_FPS)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # Convert image to RGB and process with MediaPipe Pose
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Extract landmarks
    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        h, w = image.shape[:2]

        if exercise == "squats":
            # Landmarks for Squats: Left hip, knee, ankle
            l_hip = [int(landmarks[mp_pose.PoseLandmark.LEFT_HIP].x * w),
                     int(landmarks[mp_pose.PoseLandmark.LEFT_HIP].y * h)]
            l_knee = [int(landmarks[mp_pose.PoseLandmark.LEFT_KNEE].x * w),
                      int(landmarks[mp_pose.PoseLandmark.LEFT_KNEE].y * h)]
            l_ankle = [int(landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].x * w),
                       int(landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].y * h)]

            # Calculate the angle between the three points
            knee_angle = calculate_angle(l_hip, l_knee, l_ankle)

            # Display knee angle
            cv2.putText(image, str(int(knee_angle)), (l_knee[0], l_knee[1] - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            # Posture evaluation for squats
            if 80 <= knee_angle <= 120:
                good_frames += 1
                bad_frames = 0
                cv2.putText(image, "Good Squat", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 255, 0), 2)
            else:
                bad_frames += 1
                good_frames = 0
                cv2.putText(image, "Bad Squat", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 0, 255), 2)

        elif exercise == "pushups":
            # Landmarks for Pushups: Left shoulder, elbow, wrist
            l_shoulder = [int(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].x * w),
                          int(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y * h)]
            l_elbow = [int(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].x * w),
                       int(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].y * h)]
            l_wrist = [int(landmarks[mp_pose.PoseLandmark.LEFT_WRIST].x * w),
                       int(landmarks[mp_pose.PoseLandmark.LEFT_WRIST].y * h)]

            # Calculate the elbow angle
            elbow_angle = calculate_angle(l_shoulder, l_elbow, l_wrist)

            # Display elbow angle
            cv2.putText(image, str(int(elbow_angle)), (l_elbow[0], l_elbow[1] - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            # Posture evaluation for pushups
            if 70 <= elbow_angle <= 100:
                good_frames += 1
                bad_frames = 0
                cv2.putText(image, "Good Pushup", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 255, 0), 2)
            else:
                bad_frames += 1
                good_frames = 0
                cv2.putText(image, "Bad Pushup", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 0, 255), 2)

        elif exercise == "lunges":
            # Landmarks for Lunges: Left hip, knee, ankle
            l_hip = [int(landmarks[mp_pose.PoseLandmark.LEFT_HIP].x * w),
                     int(landmarks[mp_pose.PoseLandmark.LEFT_HIP].y * h)]
            l_knee = [int(landmarks[mp_pose.PoseLandmark.LEFT_KNEE].x * w),
                      int(landmarks[mp_pose.PoseLandmark.LEFT_KNEE].y * h)]
            l_ankle = [int(landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].x * w),
                       int(landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].y * h)]

            # Calculate the angle between hip, knee, and ankle
            knee_angle = calculate_angle(l_hip, l_knee, l_ankle)

            # Display knee angle
            cv2.putText(image, str(int(knee_angle)), (l_knee[0], l_knee[1] - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            # Posture evaluation for lunges
            if 80 <= knee_angle <= 120:
                good_frames += 1
                bad_frames = 0
                cv2.putText(image, "Good Lunge", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 255, 0), 2)
            else:
                bad_frames += 1
                good_frames = 0
                cv2.putText(image, "Bad Lunge", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 0, 255), 2)

        # Calculate time for good and bad posture
        good_time = (1 / fps) * good_frames
        bad_time = (1 / fps) * bad_frames

        # Display posture times
        cv2.putText(image, f"Good Time: {round(good_time, 1)}s", (10, h - 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        cv2.putText(image, f"Bad Time: {round(bad_time, 1)}s", (10, h - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        # Play warning sound if bad posture exceeds a certain threshold
        if bad_time > 10:
            sendWarning()

    # Display the image
    cv2.imshow("Posture Detection", image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
