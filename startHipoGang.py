import os
import time
import asyncio
import random
from checkADB import is_emulator_working

class StartHipoGangFarming:
    def __init__(self, device_id):
        self.device_id = device_id

    def handle_app_behavior(self, is_start):
        if is_start:
            print("Running Telegram...")
            os.system(f"adb -s {self.device_id} shell input tap 300 900")  # HipoGang shortcut on homescreen
            time.sleep(15)
        else:
            print("Stopping Telegram...")
            os.system(f"adb -s {self.device_id} shell am force-stop org.telegram.messenger.web")
            time.sleep(5)

    def tap_farming(self):      
        sequence = " ".join(str(i) for i in range(1, 550))
        random_x = random.randint(100, 650)
        random_y = random.randint(600, 1000)
        os.system(f'''adb -s {self.device_id} shell "for i in {sequence}; do input tap {random_x} {random_y}; sleep 0.1; done"''') # Farming button position
        time.sleep(5)

        # os.system(f'''adb -s {self.device_id} shell input tap 350 300''') # click on daily reward btn
        # time.sleep(5)
        # os.system(f'''adb -s {self.device_id} shell input tap 400 1100''') # claim daily reward
        # time.sleep(5)

    async def start_HipoGang(self):
        self.handle_app_behavior(False)

        while True:
            print("\nStarting HipoGang .....")

            try: 
                if is_emulator_working():
                    self.handle_app_behavior(True)
                    print("Claiming or Farming (HipoGang).......")
                    self.tap_farming()
                    print("Successfully Claimed or Farmed, Ready to exit for now......")
                    total_seconds = 1200 # 20 minutes in seconds
                    wake_up_time = time.strftime("%H:%M:%S", time.localtime(time.time() + total_seconds))
                    print(f'Farming (HipoGang) is in progress, Need to wait for {total_seconds} seconds (until {wake_up_time})....')
                    self.handle_app_behavior(False)
                else:
                    raise ValueError("ADB NOT FOUND.....")
            except Exception as e:
                print(f'Error: {e}')
                print("Whatever it is, let's start after 2 minutes......\n")
                time.sleep(120)
            else:
                await asyncio.sleep(total_seconds)

# if __name__ == "__main__":
#     telegram_mine = StartHipoGangFarming("127.0.0.1:6555")
#     asyncio.run(telegram_mine.start_HipoGang())