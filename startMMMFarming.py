import cv2
import numpy as np
import os
import time
import asyncio
from paddleocr import PaddleOCR
from mysqlDBqueries import mysqlDBqueries

class StartMMMFarming:
    def __init__(self, device_id):
        self.device_id = device_id
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en')

    async def capture_screenshot(self):
        try:
            await asyncio.sleep(3)
            process = await asyncio.create_subprocess_shell(
                f"adb -s {self.device_id} exec-out screencap -p",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await asyncio.sleep(1)
            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                print(f"Error capturing screenshot: {stderr.decode().strip()}")
                return None

            image_array = np.frombuffer(stdout, dtype=np.uint8)
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
            return image
        except Exception as e:
            print(f"Error capturing screenshot: {e}")
            return None

    async def process_screenshot(self, image, region_coordinates=(170, 1812, 942, 1980)):
        try:
            await asyncio.sleep(3)
            x1, y1, x2, y2 = region_coordinates
            cropped_img_np = image[y1:y2, x1:x2]
            cropped_img_rgb = cv2.cvtColor(cropped_img_np, cv2.COLOR_BGR2RGB)
            result = self.ocr.ocr(cropped_img_rgb, cls=True)
            extracted_text = [line[1][0] for line in result[0]]
            if extracted_text:
                return extracted_text[0]
            else:
                print('No text detected.')
                return None
        except Exception as e:
            print(f"Error processing screenshot: {e}")
            return None

    def time_to_seconds(self, time_str):
        try:
            hours, minutes, seconds = map(int, time_str.split(":"))
            total_seconds = hours * 3600 + minutes * 60 + seconds + 30  # extra 30 seconds
            return total_seconds
        except Exception as e:
            print(f"Error converting time to seconds: {e}")
            return None

    async def handle_app_behavior(self, is_start):
        if is_start:
            print("Running Telegram...")
            os.system(f"adb -s {self.device_id} shell input swipe 900 500 100 500 300") # swipe left
            await asyncio.sleep(1)
            os.system(f"adb -s {self.device_id} shell input tap 955 635") #mmm shortcut on homescreen
            await asyncio.sleep(15)
        else:
            print("Stopping Telegram...")
            os.system(f"adb -s {self.device_id} shell am force-stop org.telegram.messenger")
            await asyncio.sleep(5)

    async def tap_farming(self):
        for _ in range(3):
            os.system(f"adb -s {self.device_id} shell input tap 515 1890") # farming btn position
            await asyncio.sleep(3)
        await asyncio.sleep(5)
        print('Claimed or Farming successfully, Ready to exit for now......')
        
        try:
            dbContext = mysqlDBqueries()
            dbContext.insert_process_data('mmm', False)
        except Exception as e:
            print(f"DB exception: {e}")

    async def start_MMM(self):
        await self.handle_app_behavior(False)

        while True:
            print("\nstarting Mr. MEME .....")
            try:
                dbContext = mysqlDBqueries()
                dbContext.insert_process_data('mmm', True)
            except Exception as e:
                print(f"DB exception: {e}")

            try:
                await self.handle_app_behavior(True)
                
                screenshot = await self.capture_screenshot()

                if screenshot is not None:
                    print('Screenshot taken and stored in array successfully')
                    text = await self.process_screenshot(screenshot)
                    print(f'text extracted: {text}')

                    if text and text.replace(" ", "").isalpha():
                        print("Claiming or Farming.......")
                        await self.tap_farming()
                        await self.handle_app_behavior(False)
                    else:
                        total_seconds = self.time_to_seconds(text) if text else None
                        if total_seconds is None or total_seconds > 28800: # 8 hours
                            total_seconds = 3000  # check after half hour
                        wake_up_time = time.strftime("%H:%M:%S", time.localtime(time.time() + total_seconds))
                        print(f'Farming is in progress, Need to wait for {total_seconds} seconds (until {wake_up_time})....')
                        await self.handle_app_behavior(False)
                        await asyncio.sleep(total_seconds)
                else:
                    print("Failed to capture screenshot.")
                    await self.handle_app_behavior(False)
            except Exception as e:
                print(f'Error: {e}')
                print("Whatever it is, let's start again\n")
                await self.handle_app_behavior(False)
