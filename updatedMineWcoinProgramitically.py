import os
import time
import random
import asyncio

class UpdatedMineWcoinProgram:
    def __init__(self, device_id):
        self.device_id = device_id
        self.sleep_val = 660

    def tap_center(self):
        os.system(f'''adb -s {self.device_id} shell "for i in $(seq 1 600); do input tap 400 750; sleep 0.2; done"''')
        print("Finished all taps.")

    def handle_app_behavior(self, is_start):
        try:
            if not is_start:
                print("Stopping Telegram...")
                os.system(f"adb -s {self.device_id} shell am force-stop org.telegram.messenger")  # Close Telegram
                time.sleep(5)
            else:
                print("Running Telegram...")
                os.system(f"adb -s {self.device_id} shell input tap 240 260")  # Tap on the shortcut
                time.sleep(15)
        except Exception as e:
            print(f"Exception(W-Coin): {e}")

    async def start_Wcoin(self):
        self.handle_app_behavior(False)
        while True:
            try:
                print("\nStarting mining W-coin...")
                self.handle_app_behavior(True)
                self.tap_center()                
                sleep_time = time.strftime("%H:%M:%S", time.localtime(time.time() + self.sleep_val))
                print(f"sleeping for {self.sleep_val} seconds (until {sleep_time}).")
                self.handle_app_behavior(False)
            except Exception as e:
                print(f"Exception: {e}")
            finally:
                await asyncio.sleep(self.sleep_val)
