import cv2
from PIL import Image
import pytesseract
import re
import os
import time
import random

def main():
    os.system('clear')
    while True:
        print("\nstarting mining W-coin.......")
        time.sleep(1)
        # take screenshot
        os.system("adb exec-out screencap -p > screen.png")
        time.sleep(5)
        return_obj = handle_png()
        if return_obj == 'restart':
            handle_app_behaviour()
            continue
        if return_obj.get('status'):
            tap_center()
        else:
            current_time = time.strftime("%H:%M:%S", time.localtime(time.time()))
            sleep_time = time.strftime("%H:%M:%S", time.localtime(time.time() + int(return_obj['sleep_val'])))
            print(f'{current_time}: {return_obj['number_before_slash']}/{return_obj['number_after_slash']} not identical,'
                   f'sleeping for {return_obj['sleep_val']} seconds: {sleep_time}')
            time.sleep(int(return_obj['sleep_val']))


def handle_png():
    try:
        screenshot_path = "screen.png"
        image = cv2.imread(screenshot_path)
        image_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        text = pytesseract.image_to_string(image_pil)
        current_strike_value = 3500
        pattern = r"(\d+)/"+str(current_strike_value)
        match = re.search(pattern, text)
        extracted_value = match.group(0) 
        number_before_slash, number_after_slash =str(extracted_value).split('/')

        # Convert the numbers to integers
        number_before_slash = int(number_before_slash)
        number_after_slash = int(number_after_slash)
        return_obj = {'status': True, 'number_after_slash': number_after_slash, 'number_before_slash': number_before_slash}

        if number_before_slash == number_after_slash:
            return return_obj
        else:
            return_obj['status'] = False
            if number_before_slash < 500:
                return_obj['sleep_val'] = 600
            elif number_before_slash < 1000:
                return_obj['sleep_val'] = 450
            elif number_before_slash < 2000:
                return_obj['sleep_val'] = 270
            elif number_before_slash < 3000:
                return_obj['sleep_val'] = 90
            else:
                return_obj['sleep_val'] = 610
            return return_obj
    except Exception as e:
        print('Exception: ', e)
        print('restarting..........')
        return 'restart'
    

def tap_center():
    total_clicks = 0
    while total_clicks < 600:
        os.system("adb shell input tap 500 1250")
        total_clicks = total_clicks + 1
        if total_clicks % 100 == 0:
            print(f"total clicks yet: {total_clicks}")
            time.sleep(random.randint(1, 5))
        time.sleep(random.uniform(0.05, 0.2)) #minimizing the time between taps
    handle_app_behaviour()
    
def handle_app_behaviour():
    print("Stopping Telegram.......")
    os.system("adb shell am force-stop org.telegram.messenger") # close telegram
    time.sleep(5)
    os.system("adb shell input swipe 900 500 100 500 300") # scroll right
    time.sleep(1)
    print('Running Telegram.....')
    os.system("adb shell input tap 125 649") # click on w-coin shortcut
    time.sleep(random.randint(7,10))

handle_app_behaviour()
# starting app
main()
