import cv2

def draw_eye_points_and_guides(frame, left_pts, right_pts):
    for p in left_pts + right_pts:
        cv2.circle(frame, p, 2, (0,255,0), -1)
    for pts in (left_pts, right_pts):
        cv2.line(frame, pts[1], pts[4], (255,255,255), 1)
        cv2.line(frame, pts[2], pts[5], (255,255,255), 1)
        cv2.line(frame, pts[0], pts[3], (255,255,255), 1)

def put_texts(frame, rows, start=(10,24), dy=24):
    x, y = start
    for text, color in rows:
        cv2.putText(frame, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        y += dy
