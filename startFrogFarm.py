import os
import time
import asyncio
from checkADB import is_emulator_working
from closeAllRecentApps import clear_all_recent_apps

class StartFrogFarmFarming:
    def __init__(self, device_id):
        self.device_id = device_id

    def handle_app_behavior(self, is_start, x_tap = 0, y_tap = 0, iter = 0):
        if is_start:
            print("Running Telegram...")
            if iter == 1:
                os.system(f"adb -s {self.device_id} shell input swipe 700 640 100 640 300") # swipe towards right
                time.sleep(3)
            os.system(f"adb -s {self.device_id} shell input tap {x_tap} {y_tap}")  # FrogFarm shortcut on homescreen
            time.sleep(20)
        else:
            print("Stopping Telegram...")
            os.system(f"adb -s {self.device_id} shell am force-stop org.telegram.messenger.web")
            time.sleep(5)
            os.system(f"adb -s {self.device_id} shell am force-stop org.telegram.messenger")
            time.sleep(3)
            os.system(f"adb -s {self.device_id} shell input swipe 100 640 700 640 300") #swipe towards left
            time.sleep(5)

    def tap_farming(self,is_daily_task):
        sequence = " ".join(str(i) for i in range(1, 4))
        os.system(f'''adb -s {self.device_id} shell "for i in {sequence}; do input tap 350 975; sleep 5; done"''') # Farming/daily reward button position
        time.sleep(5)

        if is_daily_task:
            print("Farming completed, now claiming daily reward...")
            os.system(f"adb -s {self.device_id} shell input tap 500 1130") # click on tasks
            time.sleep(3)
            os.system(f"adb -s {self.device_id} shell input tap 400 375") # click on daily reward
            time.sleep(3)
            os.system(f'''adb -s {self.device_id} shell "for i in {sequence}; do input tap 400 1100; sleep 5; done"''') # Farming/daily reward button position
            time.sleep(5)

    async def start_FrogFarm(self):
        self.handle_app_behavior(False)
        count, is_daily_task = 0, False
        while True:
            print("\nStarting FrogFarm .....")

            try: 
                for _ in range(2): # for 2 diff devices
                    if is_emulator_working():
                        x_tap, y_tap = (300, 415) if _ == 0 else (475, 900)
                        self.handle_app_behavior(True, x_tap, y_tap, _)
                        is_daily_task = count % 48 == 0 # farming completes in 30 minutes and daily task in once in a day (24 hr=> 1440 min/30 min = 48 rounds)

                        print("Claiming or Farming (FrogFarm).......")
                        self.tap_farming(is_daily_task)

                        print(f"Successfully Claimed or Farmed, Ready to exit for now for device: {_ + 1}......")
                        self.handle_app_behavior(False)
                    else:
                        raise ValueError("ADB NOT FOUND.....")
                total_seconds = 900 # 15 minutes in seconds
                wake_up_time = time.strftime("%H:%M:%S", time.localtime(time.time() + total_seconds))
                print(f'Farming (FrogFarm) is in progress, Need to wait for {total_seconds} seconds (until {wake_up_time})....')
                    
            except Exception as e:
                print(f'Error: {e}')
                print("Whatever it is, let's start after 2 minutes......\n")
                time.sleep(120)
            else:
                count = count + 1
                if count % 12 == 0:
                    clear_all_recent_apps()
                await asyncio.sleep(total_seconds)

# if __name__ == "__main__":
#     telegram_mine = StartFrogFarmFarming("127.0.0.1:6555")
#     asyncio.run(telegram_mine.start_FrogFarm())