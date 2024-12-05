import os
import time
import asyncio
import random

class StartNardomGates:
    def __init__(self, device_id):
        self.device_id = device_id

    def handle_app_behavior(self, is_start):
        if is_start:
            print("Running Telegram...")
            os.system(f"adb -s {self.device_id} shell input tap 650 350")  # NardomG shortcut on homescreen
            time.sleep(30)
        else:
            print("Stopping Telegram...")
            os.system(f"adb -s {self.device_id} shell am force-stop org.telegram.messenger")
            time.sleep(5)

    def tap_farming(self):
        loc_pick = [200, 500, 900]
        for _ in range(10):
            x_random_pick = random.choice(loc_pick)
            os.system(f'''adb -s {self.device_id} shell input tap {x_random_pick} 1400''') # pick random gate
            time.sleep(3)
            os.system(f'''adb -s {self.device_id} shell input tap 550 2150''') # click on claim the prize
            time.sleep(2)

    async def start_NardomG(self):
        self.handle_app_behavior(False)

        while True:
            print("\nStarting NardomG .....")

            try: 
                self.handle_app_behavior(True)
                print("Claiming or Farming (NardomG).......")
                self.tap_farming()
                print("Successfully Claimed or Farmed, Ready to exit for now......")
                total_seconds =  6300 # 105 minutes in seconds (1 hour and 45 minutes)
                wake_up_time = time.strftime("%H:%M:%S", time.localtime(time.time() + total_seconds))
                print(f'Farming (NardomG) is in progress, Need to wait for {total_seconds} seconds (until {wake_up_time})....')
                self.handle_app_behavior(False)
            except Exception as e:
                print(f'Error: {e}')
                print("Whatever it is, let's start again\n")
            finally:
                await asyncio.sleep(total_seconds)

if __name__ == "__main__":
    telegram_mine = StartNardomGates("emulator-5554")
    asyncio.run(telegram_mine.start_NardomG())