import os
import time
import asyncio

class StartFrogFarmFarming:
    def __init__(self, device_id):
        self.device_id = device_id

    def handle_app_behavior(self, is_start):
        if is_start:
            print("\nRunning Telegram...")
            os.system(f"adb -s {self.device_id} shell input tap 300 415")  # FrogFarm shortcut on homescreen
            time.sleep(15)
        else:
            print("Stopping Telegram...")
            os.system(f"adb -s {self.device_id} shell am force-stop org.telegram.messenger.web")
            time.sleep(5)

    def tap_farming(self, tap_x, tap_y, iter):
        if iter == 1:
            os.system(f"adb -s {self.device_id} shell input tap 500 1130") # click on tasks
            time.sleep(3)
            os.system(f"adb -s {self.device_id} shell input tap 400 350") # click on daily reward

        sequence = " ".join(str(i) for i in range(1, 6))
        os.system(f'''adb -s {self.device_id} shell "for i in {sequence}; do input tap {tap_x} {tap_y}; sleep 5; done"''') # Farming/daily reward button position
        time.sleep(5)

    async def start_FrogFarm(self):
        self.handle_app_behavior(False)

        while True:
            print("\nStarting FrogFarm .....")

            try: 
                self.handle_app_behavior(True)
                print("Claiming or Farming (FrogFarm).......")
                tap_x = tap_y = 0
                for i in range(2): # 2 times for farming and claiming daily task
                    if i == 0:
                        tap_x, tap_y = 350, 1000 # Farming btn position
                    else:
                        print("Farming completed, now claiming daily reward...")
                        tap_x, tap_y = 400, 370 # Daily task
                    self.tap_farming(tap_x, tap_y, i)

                print("Successfully Claimed or Farmed, Ready to exit for now......")
                total_seconds = 2700 # 45 minutes in seconds
                wake_up_time = time.strftime("%H:%M:%S", time.localtime(time.time() + total_seconds))
                print(f'Farming (FrogFarm) is in progress, Need to wait for {total_seconds} seconds (until {wake_up_time})....')
                self.handle_app_behavior(False)
            except Exception as e:
                print(f'Error: {e}')
                print("Whatever it is, let's start again\n")
            finally:
                await asyncio.sleep(total_seconds)

# if __name__ == "__main__":
#     telegram_mine = StartFrogFarmFarming("emulator-5556")
#     asyncio.run(telegram_mine.start_FrogFarm())