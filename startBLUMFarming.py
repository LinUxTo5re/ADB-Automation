import cv2
import numpy as np
import os
import time
import asyncio
from paddleocr import PaddleOCR
from mysqlDBqueries import mysqlDBqueries

class StartBLUMFarming:
    def __init__(self, device_id):
        self.device_id = device_id
        self.ocr = PaddleOCR(use_angle_cls = True, lang = 'en')

    async def capture_screenshot(self):
        try:
            await asyncio.sleep(3)
            process = await asyncio.create_subprocess_shell(
                f"adb -s {self.device_id} exec-out screencap -p",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                print(f"Error capturing screenshot: {stderr.decode().strip()}")
                return None

            image_array = np.frombuffer(stdout, dtype=np.uint8)
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
            # remove this line
            # image = cv2.imread("tmp/blumclaim.png", cv2.IMREAD_COLOR)
            return image
        except Exception as e:
            print(f"Error capturing screenshot: {e}")
            return None

    async def process_screenshot(self, image, region_coordinates=(45, 1840, 1055, 2005)):
        try:
            x1, y1, x2, y2 = region_coordinates
            cropped_img_np = image[y1:y2, x1:x2]
            cropped_img_rgb = cv2.cvtColor(cropped_img_np, cv2.COLOR_BGR2RGB)
            result = self.ocr.ocr(cropped_img_rgb, cls=True)
            print('\n', result)
            extracted_text = [line[1][0] for line in result[0]]
            if extracted_text:
                print(f'\nText extraction completed: {extracted_text}')
                return extracted_text
            else:
                print('No text detected.')
                return None
        except Exception as e:
            print(f"Error processing screenshot: {e}")
            return None

    async def handle_app_behavior(self, is_start):
        if is_start:
            print("\nRunning Telegram...")
            os.system(f"adb -s {self.device_id} shell input swipe 900 500 100 500 300")
            await asyncio.sleep(1)
            os.system(f"adb -s {self.device_id} shell input tap 550 1000") # blum shortcut on homescreen
            await asyncio.sleep(10)
        else:
            print("Stopping Telegram...")
            os.system(f"adb -s {self.device_id} shell am force-stop org.telegram.messenger")
            await asyncio.sleep(5)

    def time_to_seconds(self, time_str):
        try:
            time_str = next((item for item in time_str if "h" in item and "m" in item), None)

            if time_str:
                time_str = time_str.replace("h", ":").replace("m", "").strip()
                hours, minutes = map(int, time_str.split(":"))
                total_seconds = hours * 3600 + minutes * 60 + 30  # extra 30 seconds
                return total_seconds
            return None
        except Exception as e:
            print(f"Error converting time to seconds: {e}")
            return None

    async def tap_farming(self):
        for _ in range(3):
            os.system(f"adb -s {self.device_id} shell input tap 520 1935") # farming btn position
            await asyncio.sleep(3)
        await asyncio.sleep(5)
        print('Claimed or Farming successfully, Ready to exit for now......')
        
        try:
            dbContext = mysqlDBqueries()
            dbContext.insert_process_data('mmm', False, 999)
        except Exception as e:
            print(f"DB exception: {e}")


    async def start_blum(self):
        await self.handle_app_behavior(False)

        while True:
            print("starting BLUM .....")
            try:
                dbContext = mysqlDBqueries()
                dbContext.insert_process_data('blum', True, 999)
            except Exception as e:
                print(f"DB exception: {e}")

            try:
                await self.handle_app_behavior(True)
                screenshot = await self.capture_screenshot()

                if screenshot is not None:
                    print('Screenshot taken and stored in array successfully')
                    text = await self.process_screenshot(screenshot)

                    if len(text) == 2:
                        if text[0].isalpha() and text[0].upper() == 'claim'.upper():
                            print("Claiming or Farming.......")
                            await self.tap_farming()
                            await self.handle_app_behavior(False)
                        
                        if not text[1].isalpha():
                            total_seconds = self.time_to_seconds(text) if text else None
                            if total_seconds is None or total_seconds > 28800:
                                total_seconds = 6000  # check after one hour
                            wake_up_time = time.strftime("%H:%M:%S", time.localtime(time.time() + total_seconds))
                            print(f'Farming is in progress, Need to wait for {total_seconds} seconds (until {wake_up_time})....')
                            await self.handle_app_behavior(False)
                            await asyncio.sleep(total_seconds)
                    else: # hope it'll not execute in future
                        if text[0].upper() == 'Start farming'.upper():
                            print("Claiming or Farming (else block).......")
                            await self.tap_farming()
                            await self.handle_app_behavior(False)
                else:
                    print("Failed to capture screenshot.")
                    await self.handle_app_behavior(False)
            except Exception as e:
                print(f'Error: {e} \n')
                print("Whatever it is, let's start again\n")
                await self.handle_app_behavior(False)