import cv2
import time
import json
import spotipy
from gesture_detection import HandGestureRecognizer, FaceGestureRecognizer

class SpotifyController:
    def __init__(self):
        try:
            with open("token_info.json", "r") as f:
                token_info = json.load(f)
        except FileNotFoundError:
            print("❌ token_info.json not found. Run spotify_auth_grad.py first.")
            self.ready = False
            return

        access_token = token_info.get("access_token")
        if not access_token:
            print("❌ Access token missing in token_info.json.")
            self.ready = False
            return

        self.sp = spotipy.Spotify(auth=access_token)
        self.ready = True

    def execute_command(self, command):
        if not self.ready:
            print("Not authenticated")
            return

        try:
            current = self.sp.current_playback()
            if command == "Play":
                self.sp.start_playback()
            elif command == "Pause":
                self.sp.pause_playback()
            elif command == "Next Track":
                self.sp.next_track()
            elif command == "Previous Track":
                self.sp.previous_track()
            elif command == "Volume Up":
                volume = current['device']['volume_percent'] if current and current['device'] else 50
                self.sp.volume(min(volume + 15, 100))
            elif command == "Volume Down":
                volume = current['device']['volume_percent'] if current and current['device'] else 50
                self.sp.volume(max(volume - 15, 0))
            elif command == "Shuffle":
                self.sp.shuffle(True)
            elif command == "Like Song":
                if current and current['item']:
                    track_id = current['item']['id']
                    self.sp.current_user_saved_tracks_add([track_id])
        except Exception as e:
            print(f"Error executing command: {e}")

def main():
    # Initialize video capture
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    # Initialize detectors and Spotify controller
    hand_detector = HandGestureRecognizer()
    face_detector = FaceGestureRecognizer()
    spotify = SpotifyController()

    if not spotify.ready:
        print("❌ Failed to initialize Spotify controller. Check your authentication.")
        return

    last_gesture = None
    last_action_time = 0
    action_cooldown = 3  # seconds

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        current_time = time.time()

        # Detect gestures
        frame, hand_gesture = hand_detector.detect(frame)
        frame, face_gesture = face_detector.detect_face_motion(frame)

        # Determine current action
        current_action = None
        if face_gesture not in ["Unknown", "None"]:
            current_action = face_gesture
        elif hand_gesture not in ["No Hand", "Unknown"]:
            current_action = hand_gesture

        # Execute command if new action detected
        if (current_action and
            current_time - last_action_time > action_cooldown):
            print(f"🎵 Executing command: {current_action}")
            spotify.execute_command(current_action)
            last_gesture = current_action
            last_action_time = current_time

        # Display status
        status = f"Spotify: {'Ready' if spotify.ready else 'Error'}"
        cv2.putText(frame, status, (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        if current_action:
            cv2.putText(frame, f"Action: {current_action}", (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        cv2.imshow("Gesture Controlled Spotify", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
