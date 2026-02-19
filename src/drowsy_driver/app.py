import time, cv2
from .config import AppConfig
from .state import RuntimeState
from .capture.video import open_camera, read_frame
from .detect.face_mesh import FaceMeshDetector, LEFT_EYE, RIGHT_EYE
from .metrics.ear import eye_aspect_ratio, smooth
from .metrics.perclos import update_perclos, drowsy_now
from .alert.beep import beep
from .ui.overlay import draw_eye_points_and_guides, put_texts
from .calibration import start_calibration, step_calibration

def run():
    cfg = AppConfig()
    st = RuntimeState()
    st.ear_threshold = cfg.calib.default_ear_threshold
    st.ear_window = type(st.ear_window)(maxlen=cfg.metrics.ear_smooth_window)

    cam = open_camera(cfg.camera)
    detector = FaceMeshDetector(cfg.detect)

    try:
        while True:
            frame = read_frame(cam)

            now = time.time()
            dt = now - st._last_ts
            if dt > 0:
                st.fps = 0.9*st.fps + 0.1*(1.0/dt)
            st._last_ts = now

            result = detector.process(frame)
            face_detected = False
            perclos = 0.0
            state_text = "NO FACE"
            state_color = (0,255,255)

            if result.multi_face_landmarks:
                face_detected = True
                face = result.multi_face_landmarks[0]
                h, w = frame.shape[:2]
                left_pts  = detector.landmarks_to_pixels(face, w, h, LEFT_EYE)
                right_pts = detector.landmarks_to_pixels(face, w, h, RIGHT_EYE)

                ear_left  = eye_aspect_ratio(left_pts)
                ear_right = eye_aspect_ratio(right_pts)
                ear = (ear_left + ear_right) / 2.0

                st.ear_window.append(ear)
                ear_smooth = smooth(st.ear_window, cfg.metrics.ear_smooth_window)
                
                eyes_closed = ear_smooth < st.ear_threshold

                if st.calibrating:
                    finished = step_calibration(
                        st, ear_smooth,
                        cfg.calib.baseline_alpha,
                        cfg.calib.default_ear_threshold
                    )
                    if finished:
                        pass

                is_closed = ear_smooth < st.ear_threshold
                perclos = update_perclos(st.perclos_window, is_closed, cfg.metrics.window_seconds)
                
                if is_closed:
                    print(f"👁️ Olhos FECHADOS - EAR: {ear_smooth:.3f} < {st.ear_threshold:.3f}")

                drowsy = drowsy_now(st.perclos_window, perclos, cfg.metrics.persistence_seconds, cfg.metrics.perclos_threshold)
                if drowsy:
                    state_text, state_color = "DROWSY", (0,0,255)
                    if (time.time() - st.last_alert_ts) > cfg.alert.cooldown_seconds:
                        print(f"🚨 ALERTA! PERCLOS={perclos:.2f} >= {cfg.metrics.perclos_threshold}")
                        beep()
                        st.last_alert_ts = time.time()
                else:
                    state_text, state_color = "OK", (0,255,0)

                if st.show_mode == "contour":
                    detector.draw_contours(frame, face)
                else:
                    draw_eye_points_and_guides(frame, left_pts, right_pts)

                thr_msg = f"EAR_thr: {st.ear_threshold:.3f}" if st.baseline_ear else "EAR_thr: default (c p/ calibrar)"
                
                if st.perclos_window:
                    duration = st.perclos_window[-1][0] - st.perclos_window[0][0]
                else:
                    duration = 0
                
                perclos_color = (255,255,255)
                if perclos >= cfg.metrics.perclos_threshold:
                    perclos_color = (0,0,255) if duration >= cfg.metrics.persistence_seconds else (0,165,255)
                elif perclos >= cfg.metrics.perclos_threshold * 0.7:
                    perclos_color = (0,255,255)
                
                eye_status = "FECHADOS" if eyes_closed else "ABERTOS"
                eye_color = (0, 0, 255) if eyes_closed else (0, 255, 0)
                
                put_texts(frame, [
                    (f"Mode: {st.show_mode}  (t: toggle, c: calibrate, q: quit)", (255,255,255)),
                    (f"EAR(L/R/avg): {ear_left:.3f}/{ear_right:.3f}/{ear_smooth:.3f} - Olhos: {eye_status}", eye_color),
                    (f"PERCLOS({cfg.metrics.window_seconds}s): {perclos:.2f} / {cfg.metrics.perclos_threshold:.2f} [{duration:.1f}s]", perclos_color),
                    (thr_msg, (255,255,255)),
                    (f"STATE: {state_text}", state_color),
                    (f"FPS: {st.fps:.1f}", (255,255,255)),
                    (f"Cooldown: {max(0, int(cfg.alert.cooldown_seconds - (time.time()-st.last_alert_ts)))}s", (255,255,255)),
                ])

            else:
                put_texts(frame, [
                    ("Mode: points  (t: toggle, c: calibrate, q: quit)", (255,255,255)),
                    (f"PERCLOS({cfg.metrics.window_seconds}s): {perclos:.2f}", (255,255,255)),
                    ("STATE: NO FACE", (0,255,255)),
                    (f"FPS: {st.fps:.1f}", (255,255,255)),
                ])
                cv2.putText(frame, "SEM ROSTO", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)

            cv2.imshow("Drowsy Driver MVP", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            if key == ord('t'):
                st.show_mode = "contour" if st.show_mode == "points" else "points"
            if key == ord('c') and not st.calibrating:
                start_calibration(st, cfg.calib.seconds)

    finally:
        cam.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    run()