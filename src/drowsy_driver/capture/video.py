from __future__ import annotations
import cv2
from ..config import CameraConfig

def open_camera(cfg: CameraConfig):
    cam = cv2.VideoCapture(cfg.index)
    if not cam.isOpened():
        raise RuntimeError("Cannot open camera")
    cam.set(cv2.CAP_PROP_FRAME_WIDTH,  cfg.width)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, cfg.height)
    return cam

def read_frame(cam):
    ok, frame = cam.read()
    if not ok:
        raise RuntimeError("Cannot read frame")
    return frame
