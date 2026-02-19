import cv2
import mediapipe as mp
import math
import time
import sys
from collections import deque

cam = cv2.VideoCapture(0)
if not cam.isOpened():
    print("Cannot open camera")
    exit()

mp_face = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
face_mesh = mp_face.FaceMesh(
    max_num_faces=1, 
    refine_landmarks=True,
    min_detection_confidence=0.5, 
    min_tracking_confidence=0.5)

WINDOW_SECONDS = 12
PERCLOS_THRESHOLD = 0.70
PERSISTENCE_SECONDS = 8

CALIB_SECONDS = 10
BASELINE_ALPHA = 0.78

perclos_window = deque()
baseline_ear = None
ear_threshold = 0.20
calibrating = False
calib_data = []
calib_t0 = None
last_alert_ts = 0
ALERT_COOLDOWN = 6 

LEFT_EYE  = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

EAR_SMOOTH_WINDOW = 5
ear_window = deque(maxlen=EAR_SMOOTH_WINDOW)

def to_px(lm, w, h, idxs):
    return [(int(lm[i].x*w), int(lm[i].y*h)) for i in idxs]

def euclid(p1, p2):
    return math.hypot(p1[0]-p2[0], p1[1]-p2[1])

def eye_aspect_ratio(pts):
    A = euclid(pts[1], pts[4])
    B = euclid(pts[2], pts[5])
    C = euclid(pts[0], pts[3]) + 1e-8
    return (A + B) / (2.0 * C)

def beep_alert():
    if sys.platform.startswith("win"):
        import winsound
        winsound.Beep(880, 300)
        winsound.Beep(660, 300)
        winsound.Beep(880, 300)
    else:
        print("\a", end="", flush=True)

def beep_alert():
    if sys.platform.startswith("win"):
        import winsound
        winsound.PlaySound("SystemHand", winsound.SND_ALIAS | winsound.SND_ASYNC)
    else:
        print("\a", end="", flush=True)



show_mode = "points"

while True:
    ok, frame = cam.read()
    if not ok:
        print("Cannot read frame")
        break

    face_detected = False

    if result.multi_face_landmarks:
        face_detected = True

    if not face_detected:
        cv2.putText(frame, "SEM ROSTO", (10, 144),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)


    cam.set(cv2.CAP_PROP_FRAME_WIDTH,  640)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(rgb)


    if result.multi_face_landmarks:
        face = result.multi_face_landmarks[0]
        h, w = frame.shape[:2]
        lm = face.landmark

        left_pts  = to_px(lm, w, h, LEFT_EYE)
        right_pts = to_px(lm, w, h, RIGHT_EYE)

        ear_left  = eye_aspect_ratio(left_pts)
        ear_right = eye_aspect_ratio(right_pts)
        ear = (ear_left + ear_right) / 2.0

        ear_window.append(ear)
        ear_smooth = sum(ear_window) / len(ear_window)

        now = time.time()

        eye_closed = ear_smooth < ear_threshold

        while perclos_window and (now - perclos_window[0][0] > WINDOW_SECONDS):
            perclos_window.popleft()

        perclos_window.append((now, int(eye_closed)))

        if perclos_window:
            perclos = sum(v for _, v in perclos_window) / len(perclos_window)
        else:
            perclos = 0.0

        state = "OK"
        drowsy = False

        if perclos_window:
            window_duration = perclos_window[-1][0] - perclos_window[0][0]
            if window_duration >= PERSISTENCE_SECONDS and perclos >= PERCLOS_THRESHOLD:
                drowsy = True

        if drowsy:
            state = "DROWSY"
            if (time.time() - last_alert_ts) > ALERT_COOLDOWN:
                beep_alert()
                last_alert_ts = time.time()

        _last_ts = time.time()
        fps = 0.0

        now = time.time()
        dt = now - _last_ts
        if dt > 0:
            fps = 0.9*fps + 0.1*(1.0/dt)
        _last_ts = now

        cv2.putText(frame, f"FPS: {fps:.1f}", (10, 168),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)

        cooldown_left = max(0, int(ALERT_COOLDOWN - (time.time() - last_alert_ts)))
        cv2.putText(frame, f"Cooldown: {cooldown_left}s", (10, 192),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)


        color = (0,255,0) if state=="OK" else (0,0,255)
        cv2.putText(frame, f"STATE: {state}", (10, 144),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)


        cv2.putText(frame, f"PERCLOS({WINDOW_SECONDS}s): {perclos:.2f}",
                    (10, 72), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)

        cv2.putText(frame, f"EAR(L/R/avg): {ear_left:.3f}/{ear_right:.3f}/{ear_smooth:.3f}",
                    (10, 48), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
        
        if calibrating:
            calib_data.append(ear_smooth)
            cv2.putText(frame, "CALIBRANDO... mantenha olhos abertos",
                        (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255), 2)

            if time.time() - calib_t0 >= CALIB_SECONDS:
                calibrating = False
                if len(calib_data) > 10:
                    baseline_ear = float(sum(calib_data) / len(calib_data))
                    ear_threshold = baseline_ear * BASELINE_ALPHA
                    calib_data = []
                    cv2.putText(frame, f"Calibrado! baseline={baseline_ear:.3f} thr={ear_threshold:.3f}",
                                (10, 124), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
                else:
                    cv2.putText(frame, "Calibracao insuficiente. Tente novamente (c).",
                                (10, 124), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)



        if show_mode == "contour":
            mp_drawing.draw_landmarks(
                image=frame,
                landmark_list=face,
                connections=mp_face.FACEMESH_CONTOURS,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing.DrawingSpec(color=(0,255,0), thickness=1, circle_radius=1)
            )
        else:
            for p in left_pts + right_pts:
                cv2.circle(frame, p, 2, (0,255,0), -1)

            def draw_ear_guides(pts):
                cv2.line(frame, pts[1], pts[4], (255,255,255), 1)
                cv2.line(frame, pts[2], pts[5], (255,255,255), 1)
                cv2.line(frame, pts[0], pts[3], (255,255,255), 1)
            draw_ear_guides(left_pts)
            draw_ear_guides(right_pts)

    cv2.putText(frame, f"Mode: {show_mode}  (press 't' to toggle, 'q' to quit)",
                (10, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
    thr_msg = f"EAR_thr: {ear_threshold:.3f}" if baseline_ear else "EAR_thr: default (calibre com 'c')"
    cv2.putText(frame, thr_msg, (10, 96), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)


    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    if key == ord('t'):
        show_mode = "contour" if show_mode == "points" else "points"
    if key == ord('c') and not calibrating:
        calibrating = True
        calib_data = []
        calib_t0 = time.time()


cam.release()
cv2.destroyAllWindows()