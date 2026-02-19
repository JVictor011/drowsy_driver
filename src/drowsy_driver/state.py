from __future__ import annotations
from dataclasses import dataclass, field
from collections import deque
import time

@dataclass
class RuntimeState:
    ear_window: deque = field(default_factory=lambda: deque(maxlen=5))
    perclos_window: deque = field(default_factory=deque)
    baseline_ear: float | None = None
    ear_threshold: float = 0.20
    calibrating: bool = False
    calib_data: list[float] = field(default_factory=list)
    calib_t0: float | None = None
    last_alert_ts: float = 0.0
    fps: float = 0.0
    _last_ts: float = field(default_factory=time.time)
    show_mode: str = "points"
