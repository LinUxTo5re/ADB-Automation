import time
import pyautogui

while True:
    pyautogui.write("ABCDE")  # Type 5 characters
    time.sleep(1)             # Pause for 1 second before removing
    for _ in range(5):        # Simulate backspace to delete the characters
        pyautogui.press("backspace")
    time.sleep(30)            # Wait for 30 seconds before the next cycle
