from __future__ import annotations
import cv2
import mediapipe as mp
from ..config import DetectConfig

LEFT_EYE  = [33,160,158,133,153,144]
RIGHT_EYE = [362,385,387,263,373,380]

class FaceMeshDetector:
    def __init__(self, cfg: DetectConfig):
        self.mp_face = mp.solutions.face_mesh
        self.mp_draw = mp.solutions.drawing_utils
        self.mesh = self.mp_face.FaceMesh(
            max_num_faces=cfg.max_faces,
            refine_landmarks=cfg.refine_landmarks,
            min_detection_confidence=cfg.min_det_conf,
            min_tracking_confidence=cfg.min_track_conf,
        )

    def process(self, frame_bgr):
        rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        return self.mesh.process(rgb)

    def landmarks_to_pixels(self, face, w, h, idxs):
        lm = face.landmark
        return [(int(lm[i].x*w), int(lm[i].y*h)) for i in idxs]

    def draw_contours(self, frame, face):
        self.mp_draw.draw_landmarks(
            image=frame,
            landmark_list=face,
            connections=self.mp_face.FACEMESH_CONTOURS,
            landmark_drawing_spec=None,
            connection_drawing_spec=self.mp_draw.DrawingSpec(color=(0,255,0), thickness=1, circle_radius=1)
        )
