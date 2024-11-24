import cv2
import numpy as np
import os
import time
import subprocess
from paddleocr import PaddleOCR

device_id = "127.0.0.1:6555"
ocr = PaddleOCR(use_angle_cls=True, lang='en')

def capture_screenshot():
    try:
        time.sleep(3)
        result = subprocess.check_output(f"adb -s {device_id} exec-out screencap -p", shell=True)
        image_array = np.frombuffer(result, dtype=np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        return image
    except Exception as e:
        print(f"Error capturing screenshot: {e}")
        return None

def process_screenshot(image, region_coordinates=(170, 1812, 942, 1980)):
    try:
        x1, y1, x2, y2 = region_coordinates
        cropped_img_np = image[y1:y2, x1:x2]
        cropped_img_rgb = cv2.cvtColor(cropped_img_np, cv2.COLOR_BGR2RGB)
        result = ocr.ocr(cropped_img_rgb, cls=True)
        extracted_text = [line[1][0] for line in result[0]]
        if extracted_text:
            print(f'Text extraction completed: {extracted_text[0]}')
            return extracted_text[0]
        else:
            print('No text detected.')
            return None
    except Exception as e:
        print(f"Error processing screenshot: {e}")
        return None

def time_to_seconds(time_str):
    try:
        hours, minutes, seconds = map(int, time_str.split(":"))
        total_seconds = hours * 3600 + minutes * 60 + seconds + 30 # extra 30 seconds
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

def tap_farming():
    for i in range(3):
        os.system(f"adb -s {device_id} shell input tap 515 1890")
        time.sleep(3)
    time.sleep(5)
    print('Claimed or Farming successfully, Ready to exist for now......')

def start_MMM():
    os.system('clear')
    handle_app_behavior(False)

    while True:
        try:
            handle_app_behavior(True)
            screenshot = capture_screenshot()

            if screenshot is not None:
                print('Screenshot taken and stored in array successfully')
                text = process_screenshot(screenshot)
                print(f'text extracted: {text}')
                
                if text.replace(" ", "").isalpha():
                    print("Claiming or Farming.......")
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

start_MMM()