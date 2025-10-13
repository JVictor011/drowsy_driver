import cv2
import mediapipe as mp

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

LEFT_EYE  = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

def to_px(lm, w, h, idxs):
    return [(int(lm[i].x*w), int(lm[i].y*h)) for i in idxs]

show_mode = "points"

while True:
    ok, frame = cam.read()
    if not ok:
        print("Cannot read frame")
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(rgb)

    if result.multi_face_landmarks:
        face = result.multi_face_landmarks[0]
        h, w = frame.shape[:2]
        lm = face.landmark

        left_pts  = to_px(lm, w, h, LEFT_EYE)
        right_pts = to_px(lm, w, h, RIGHT_EYE)

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

    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    if key == ord('t'):
        show_mode = "contour" if show_mode == "points" else "points"

cam.release()
cv2.destroyAllWindows()