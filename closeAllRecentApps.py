import subprocess
import time

def clear_all_recent_apps():
    try:
        subprocess.run(["adb", "shell", "input", "keyevent", "KEYCODE_APP_SWITCH"], check=True)
        time.sleep(1)
        for _ in range(5):
            subprocess.run(["adb", "shell", "input", "swipe", "100", "500", "900", "500", "300"], check=True)
            time.sleep(0.5)
        time.sleep(3)
        subprocess.run(["adb", "shell", "input", "tap", "150", "570"], check=True)
        time.sleep(5)
    except Exception as e:
        print(f"Error (clear all recent taps): {e}")