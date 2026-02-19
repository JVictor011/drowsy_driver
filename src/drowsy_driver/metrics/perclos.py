import time
from collections import deque

def update_perclos(perclos_window: deque, is_closed: bool, window_seconds: int) -> float:
    now = time.time()
    while perclos_window and (now - perclos_window[0][0] > window_seconds):
        perclos_window.popleft()
    perclos_window.append((now, int(is_closed)))
    return sum(v for _, v in perclos_window)/len(perclos_window) if perclos_window else 0.0

def drowsy_now(perclos_window: deque, perclos: float, persistence_seconds: int, perclos_threshold: float) -> bool:
    if not perclos_window: return False
    duration = perclos_window[-1][0] - perclos_window[0][0]
    return duration >= persistence_seconds and perclos >= perclos_threshold
