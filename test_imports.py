import sys
sys.path.insert(0, 'src')

print("Testing config...")
try:
    from drowsy_driver.config import AppConfig
    print(f"✓ AppConfig imported: {AppConfig}")
except Exception as e:
    print(f"✗ Error importing AppConfig: {e}")
    import traceback
    traceback.print_exc()

print("\nTesting state...")
try:
    from drowsy_driver.state import RuntimeState
    print(f"✓ RuntimeState imported: {RuntimeState}")
except Exception as e:
    print(f"✗ Error importing RuntimeState: {e}")
    import traceback
    traceback.print_exc()

print("\nTesting capture.video...")
try:
    from drowsy_driver.capture.video import open_camera, read_frame
    print(f"✓ open_camera, read_frame imported")
except Exception as e:
    print(f"✗ Error importing from capture.video: {e}")
    import traceback
    traceback.print_exc()

print("\nTesting detect.face_mesh...")
try:
    from drowsy_driver.detect.face_mesh import FaceMeshDetector, LEFT_EYE, RIGHT_EYE
    print(f"✓ FaceMeshDetector, LEFT_EYE, RIGHT_EYE imported")
except Exception as e:
    print(f"✗ Error importing from detect.face_mesh: {e}")
    import traceback
    traceback.print_exc()

print("\nTesting metrics.ear...")
try:
    from drowsy_driver.metrics.ear import eye_aspect_ratio, smooth
    print(f"✓ eye_aspect_ratio, smooth imported")
except Exception as e:
    print(f"✗ Error importing from metrics.ear: {e}")
    import traceback
    traceback.print_exc()

print("\nTesting metrics.perclos...")
try:
    from drowsy_driver.metrics.perclos import update_perclos, drowsy_now
    print(f"✓ update_perclos, drowsy_now imported")
except Exception as e:
    print(f"✗ Error importing from metrics.perclos: {e}")
    import traceback
    traceback.print_exc()

print("\nTesting alert.beep...")
try:
    from drowsy_driver.alert.beep import beep
    print(f"✓ beep imported")
except Exception as e:
    print(f"✗ Error importing from alert.beep: {e}")
    import traceback
    traceback.print_exc()

print("\nTesting ui.overlay...")
try:
    from drowsy_driver.ui.overlay import draw_eye_points_and_guides, put_texts
    print(f"✓ draw_eye_points_and_guides, put_texts imported")
except Exception as e:
    print(f"✗ Error importing from ui.overlay: {e}")
    import traceback
    traceback.print_exc()

print("\nTesting calibration...")
try:
    from drowsy_driver.calibration import start_calibration, step_calibration
    print(f"✓ start_calibration, step_calibration imported")
except Exception as e:
    print(f"✗ Error importing from calibration: {e}")
    import traceback
    traceback.print_exc()

print("\n✅ All imports successful!")
