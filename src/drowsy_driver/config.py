from dataclasses import dataclass, field

@dataclass
class CameraConfig:
    width: int = 640
    height: int = 480
    index: int = 0

@dataclass
class DetectConfig:
    max_faces: int = 1
    refine_landmarks: bool = True
    min_det_conf: float = 0.5
    min_track_conf: float = 0.5

@dataclass
class MetricsConfig:
    ear_smooth_window: int = 5
    window_seconds: int = 12
    perclos_threshold: float = 0.50
    persistence_seconds: int = 3

@dataclass
class CalibConfig:
    seconds: int = 10
    baseline_alpha: float = 0.85
    default_ear_threshold: float = 0.30

@dataclass
class AlertConfig:
    cooldown_seconds: int = 3

@dataclass
class AppConfig:
    camera: CameraConfig = field(default_factory=CameraConfig)
    detect: DetectConfig = field(default_factory=DetectConfig)
    metrics: MetricsConfig = field(default_factory=MetricsConfig)
    calib: CalibConfig = field(default_factory=CalibConfig)
    alert: AlertConfig = field(default_factory=AlertConfig)
