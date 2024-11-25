import cv2
import numpy as np
from PIL import Image
import pytesseract
import re
import os
import time
import random
import subprocess
import asyncio
from mysqlDBqueries import mysqlDBqueries
from handleEmulator import GenymotionManager

class UpdatedMineWcoinProgramAsync:
    def __init__(self, device_id, emulator_name, genymotion_path):
        self.device_id = device_id
        self.count_error = 0
        self.emulator_name = emulator_name
        self.genymotion_path = genymotion_path

    async def take_screenshot(self):
        try:
            result = await asyncio.to_thread(
                subprocess.check_output,
                f"adb -s {self.device_id} exec-out screencap -p",
                shell=True
            )
            image_array = np.frombuffer(result, dtype=np.uint8)
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
            return image
        except Exception as e:
            print(f"Error capturing screenshot: {e}")
            try:
                dbContext = mysqlDBqueries()
                dbContext.insert_process_data('Error', False, 999)
                await asyncio.sleep(300)
            except Exception as e:
                print(f"DB exception: {e}")

            return None

    async def process_screenshot(self, image, current_strike_value=3500):
        try:
            image_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            text = await asyncio.to_thread(pytesseract.image_to_string, image_pil)
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
        if number_before_slash < 500:
            return 650
        elif number_before_slash < 1000:
            return 550
        elif number_before_slash < 2000:
            return 350
        elif number_before_slash < 3000:
            return 280
        elif number_before_slash < 3500:
            return 90
        else:
            return 610

    async def tap_center(self):
        total_clicks = 0
        while total_clicks < 600:
            os.system(f"adb -s {self.device_id} shell input tap 500 1250") # w-coin tap pointer
            total_clicks += 1
            if total_clicks % 100 == 0:
                print(f"Total clicks so far: {total_clicks}")
                await asyncio.sleep(random.randint(1, 5))
            await asyncio.sleep(random.uniform(0.05, 0.2))  # Minimize time between taps
        
        try:
            dbContext = mysqlDBqueries()
            dbContext.insert_process_data('wcoin', False, 999)
        except Exception as e:
            print(f"DB exception: {e}")

    async def handle_app_behavior(self, is_start):
        if not is_start:
            print("Stopping Telegram...")
            os.system(f"adb -s {self.device_id} shell am force-stop org.telegram.messenger")  # Close Telegram
            await asyncio.sleep(5)
        else:
            os.system(f"adb -s {self.device_id} shell input swipe 900 500 100 500 300")  # Scroll right
            await asyncio.sleep(1)
            print("Running Telegram...")
            os.system(f"adb -s {self.device_id} shell input tap 125 649")  # Tap on the shortcut
            await asyncio.sleep(random.randint(7, 10))

    async def start_Wcoin(self):
        await self.handle_app_behavior(False)
        while True:
            try:
                dbContext = mysqlDBqueries()
                dbContext.insert_process_data('wcoin', True, 999)
            except Exception as e:
                print(f"DB exception: {e}")

            try:
                await self.handle_app_behavior(True)
                print("\nStarting mining W-coin...")
                await asyncio.sleep(3)

                # Capture screenshot
                image = await self.take_screenshot()
                if image is None:
                    print("Error capturing screenshot. Retrying...")
                    self.count_error = self.count_error + 1
                    if self.count_error > 5:
                        manager = GenymotionManager(self.emulator_name, self.genymotion_path)
                        await manager.manage_emulator()
                        await asyncio.sleep(10)
                        self.count_error = 0
                    continue

                print('Screenshot taken and stored in array successfully')

                # Process screenshot
                return_obj = await self.process_screenshot(image)
                if not return_obj:
                    print("OCR processing failed. Restarting app...")
                    await self.handle_app_behavior(False)
                    continue
                
                print(f'text extracted: {return_obj}')

                if return_obj['status']:
                    print("Values are identical. Starting tap center action...")
                    await self.tap_center()
                    await self.handle_app_behavior(False)
                else:
                    sleep_val = self.determine_sleep_time(return_obj['number_before_slash'])
                    current_time = time.strftime("%H:%M:%S", time.localtime(time.time()))
                    sleep_time = time.strftime("%H:%M:%S", time.localtime(time.time() + sleep_val))
                    print(f"{current_time}: {return_obj['number_before_slash']}/{return_obj['number_after_slash']} "
                        f"not identical, sleeping for {sleep_val} seconds (until {sleep_time}).")
                    await self.handle_app_behavior(False)
                    await asyncio.sleep(sleep_val)
            except Exception as e:
                print(f"Exception: {e}")
                await self.handle_app_behavior(False)