import time

def start_calibration(state, seconds: int):
    state.calibrating = True
    state.calib_data.clear()
    state.calib_t0 = time.time()
    state._calib_seconds = seconds

def step_calibration(state, ear_smooth, baseline_alpha: float, default_threshold: float):
    state.calib_data.append(ear_smooth)
    if (time.time() - state.calib_t0) >= state._calib_seconds:
        state.calibrating = False
        if len(state.calib_data) > 10:
            baseline = sum(state.calib_data) / len(state.calib_data)
            state.baseline_ear = baseline
            state.ear_threshold = baseline * baseline_alpha
        else:
            state.baseline_ear = None
            state.ear_threshold = default_threshold
        state.calib_data.clear()
        state.calib_t0 = None
        return True
    return False
