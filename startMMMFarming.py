import cv2
import numpy as np
import os
import time
import subprocess
import easyocr

device_id = "127.0.0.1:6555"

def capture_screenshot():
    try:
        time.sleep(3)
        result = subprocess.check_output(f"adb -s {device_id} exec-out screencap -p", shell=True)
        image_array = np.frombuffer(result, dtype=np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        print('Image captured successfully')
        return image
    except Exception as e:
        print(f"Error capturing screenshot: {e}")
        return None

def process_screenshot(image, region_coordinates=(170, 1812, 942, 1980)):
    try:
        x1, y1, x2, y2 = region_coordinates
        cropped_img_np = image[y1:y2, x1:x2]
        reader = easyocr.Reader(['en'])
        result = reader.readtext(cropped_img_np)
        extracted_text = [text for _, text, _ in result]
        print(f'Text extraction completed: {extracted_text[0]}')
        return extracted_text
    except Exception as e:
        print(f"Error processing screenshot: {e}")
        return None

def time_to_seconds(time_str):
    try:
        time_str = time_str.replace(".", ":")
        hours, minutes, seconds = map(int, time_str.split(":"))
        total_seconds = hours * 3600 + minutes * 60 + seconds
        return total_seconds
    except Exception as e:
        print(f"Error converting time to seconds: {e}")
        return None

def handle_app_behavior(is_start):
    if is_start:
        print("\nRunning Telegram...")
        os.system(f"adb -s {device_id} shell input swipe 900 500 100 500 300")  # Scroll right
        time.sleep(1)
        os.system(f"adb -s {device_id} shell input tap 955 635")  # Tap on the shortcut
        time.sleep(10)
    else:
        print("Stopping Telegram...")
        os.system(f"adb -s {device_id} shell am force-stop org.telegram.messenger")  # Close Telegram
        time.sleep(5)

def main():
    os.system('clear')
    while True:
        try:
            handle_app_behavior(True)
            screenshot = capture_screenshot()

            if screenshot is not None:
                text = process_screenshot(screenshot)[0]
                if text == 'START FARMING':
                    print("Starting Farming.......")
                    tap_farming()
                    handle_app_behavior(False)
                else:
                    total_seconds = time_to_seconds(text)
                    if total_seconds is None or total_seconds > 28500:
                        total_seconds = 6000 # check after one hour
                    wake_up_time = time.strftime("%H:%M:%S", time.localtime(time.time() + total_seconds))
                    print(f'Farming is in progress, Need to wait for {total_seconds} seconds (until {wake_up_time})....')
                    handle_app_behavior(False)
                    time.sleep(total_seconds)
            else:
                print("Failed to capture screenshot.")
                handle_app_behavior(False)
        except Exception as e:
            print(f'Error: {e} \n')
            print("WhatEver it is, let's start again\n")
            handle_app_behavior(False)

def tap_farming():
    os.system(f"adb -s {device_id} shell input tap 515 1890")
    time.sleep(5)
    print('Farming Started, Ready to exist for now......')

handle_app_behavior(False)
main()