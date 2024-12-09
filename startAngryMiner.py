import os
import time
import asyncio
from checkADB import is_emulator_working

class StartAngryMiner:
    def __init__(self, device_id):
        self.device_id = device_id

    def handle_app_behavior(self, is_start):
        if is_start:
            print("Running Telegram...")
            os.system(f"adb -s {self.device_id} shell input tap 115 900")  # AngryMiner shortcut on homescreen
            time.sleep(30)
        else:
            print("Stopping Telegram...")
            os.system(f"adb -s {self.device_id} shell am force-stop org.telegram.messenger.web")
            time.sleep(5)

    def tap_farming(self):      
        sequence = " ".join(str(i) for i in range(1, 3))
        os.system(f'''adb -s {self.device_id} shell "for i in {sequence}; do input tap 375 950; sleep 5; done"''') # Farming button position
        time.sleep(5)

    async def start_AngryMiner(self):
        self.handle_app_behavior(False)

        while True:
            print("\nStarting AngryMiner .....")

            try: 
                if is_emulator_working():
                    self.handle_app_behavior(True)
                    print("Claiming or Farming (AngryMiner).......")
                    self.tap_farming()
                    print("Successfully mined, Ready to exit for now......")
                    total_seconds = 7200 # 2 hours in seconds
                    wake_up_time = time.strftime("%H:%M:%S", time.localtime(time.time() + total_seconds))
                    print(f'Mining (AngryMiner) is in progress, Need to wait for {total_seconds} seconds (until {wake_up_time})....')
                    self.handle_app_behavior(False)
                else:
                    raise ValueError("ADB NOT FOUND.....")
            except Exception as e:
                print(f'Warning: {e}')
                print("Whatever it is, let's start after 2 minutes......\n")
                time.sleep(120)
            else:
                await asyncio.sleep(total_seconds)

if __name__ == "__main__":
    telegram_mine = StartAngryMiner("127.0.0.1:6555")
    asyncio.run(telegram_mine.start_AngryMiner())