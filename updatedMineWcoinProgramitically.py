import cv2
import numpy as np
from PIL import Image
import pytesseract
import re
import os
import time
import random
import subprocess

device_id = "127.0.0.1:6555"

class updatedMineWcoinProgramitically:
    def __init__(self):
        pass

    def take_screenshot(self):
        """
        Capture a screenshot using adb and return it as a NumPy array.
        """
        try:
            result = subprocess.check_output(f"adb -s {device_id} exec-out screencap -p", shell=True)
            image_array = np.frombuffer(result, dtype=np.uint8)
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
            return image
        except Exception as e:
            print(f"Error capturing screenshot: {e}")
            return None

    def process_screenshot(self, image, current_strike_value=3500):
        """
        Process the screenshot and extract the numeric values using OCR.
        """
        try:
            image_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            text = pytesseract.image_to_string(image_pil)
            pattern = rf"(\d+)/{current_strike_value}"
            match = re.search(pattern, text)
            if match:
                number_before_slash, number_after_slash = map(int, match.group(0).split('/'))
                return {
                    'status': number_before_slash == number_after_slash,
                    'number_before_slash': number_before_slash,
                    'number_after_slash': number_after_slash
                }
            else:
                print("No match found in OCR text.")
                return None
        except Exception as e:
            print(f"Error processing screenshot: {e}")
            return None

    def determine_sleep_time(self, number_before_slash):
        """
        Determine the sleep time based on the value of number_before_slash.
        """
        if number_before_slash < 500:
            return 600
        elif number_before_slash < 1000:
            return 450
        elif number_before_slash < 2000:
            return 270
        elif number_before_slash < 3000:
            return 90
        elif number_before_slash < 3500:
            return 60
        else:
            return 610

    def tap_center(self):
        """
        Simulate taps on the screen using adb.
        """
        total_clicks = 0
        while total_clicks < 600:
            os.system(f"adb -s {device_id} shell input tap 500 1250")
            total_clicks += 1
            if total_clicks % 100 == 0:
                print(f"Total clicks so far: {total_clicks}")
                time.sleep(random.randint(1, 5))
            time.sleep(random.uniform(0.05, 0.2))  # Minimize time between taps

    def handle_app_behavior(self):
        """
        Handle app-specific behavior: restart and navigate to the required state.
        """
        print("Stopping Telegram...")
        os.system(f"adb -s {device_id} shell am force-stop org.telegram.messenger")  # Close Telegram
        time.sleep(5)
        os.system(f"adb -s {device_id} shell input swipe 900 500 100 500 300")  # Scroll right
        time.sleep(1)
        print("Running Telegram...")
        os.system(f"adb -s {device_id} shell input tap 125 649")  # Tap on the shortcut
        time.sleep(random.randint(7, 10))

    def start_Wcoin(self):
        """
        Main script logic to automate tasks using ADB.
        """
        os.system('clear')
        while True:
            print("\nStarting mining W-coin...")
            time.sleep(3)

            # Capture screenshot
            image = self.take_screenshot()
            if image is None:
                print("Error capturing screenshot. Retrying...")
                continue

            # Process screenshot
            return_obj = self.process_screenshot(image)
            if not return_obj:
                print("OCR processing failed. Restarting app...")
                self.handle_app_behavior()
                continue

            if return_obj['status']:
                print("Values are identical. Starting tap center action...")
                self.tap_center()
                self.handle_app_behavior()
            else:
                sleep_val = self.determine_sleep_time(return_obj['number_before_slash'])
                current_time = time.strftime("%H:%M:%S", time.localtime(time.time()))
                sleep_time = time.strftime("%H:%M:%S", time.localtime(time.time() + sleep_val))
                print(f"{current_time}: {return_obj['number_before_slash']}/{return_obj['number_after_slash']} "
                      f"not identical, sleeping for {sleep_val} seconds (until {sleep_time}).")
                time.sleep(sleep_val)

    # Start the app and run the main loop
    handle_app_behavior()
    start_Wcoin()
