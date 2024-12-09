import os
import time
import asyncio
from checkADB import is_emulator_working

class StartFrogFarmFarming:
    def __init__(self, device_id):
        self.device_id = device_id

    def handle_app_behavior(self, is_start):
        if is_start:
            print("Running Telegram...")
            os.system(f"adb -s {self.device_id} shell input tap 300 415")  # FrogFarm shortcut on homescreen
            time.sleep(20)
        else:
            print("Stopping Telegram...")
            os.system(f"adb -s {self.device_id} shell am force-stop org.telegram.messenger.web")
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
                if is_emulator_working():
                    self.handle_app_behavior(True)
                    is_daily_task = count % 48 == 0 # farming completes in 30 minutes and daily task in once in a day (24 hr=> 1440 min/30 min = 48 rounds)

                    print("Claiming or Farming (FrogFarm).......")
                    self.tap_farming(is_daily_task)

                    print("Successfully Claimed or Farmed, Ready to exit for now......")
                    total_seconds = 900 # 15 minutes in seconds
                    wake_up_time = time.strftime("%H:%M:%S", time.localtime(time.time() + total_seconds))
                    print(f'Farming (FrogFarm) is in progress, Need to wait for {total_seconds} seconds (until {wake_up_time})....')
                    self.handle_app_behavior(False)
                else:
                    raise ValueError("ADB NOT FOUND.....")
            except Exception as e:
                print(f'Error: {e}')
                print("Whatever it is, let's start after 2 minutes......\n")
                time.sleep(120)
            else:
                count = count + 1
                await asyncio.sleep(total_seconds)

# if __name__ == "__main__":
#     telegram_mine = StartFrogFarmFarming("127.0.0.1:6555")
#     asyncio.run(telegram_mine.start_FrogFarm())