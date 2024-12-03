import os
import time
import asyncio

class StartSeedFarming:
    def __init__(self, device_id):
        self.device_id = device_id

    def handle_app_behavior(self, is_start):
        if is_start:
            print("\nRunning Telegram...")
            os.system(f"adb -s {self.device_id} shell input tap 470 650")  # Seed shortcut on homescreen
            time.sleep(15)
        else:
            print("Stopping Telegram...")
            os.system(f"adb -s {self.device_id} shell am force-stop org.telegram.messenger.web")
            time.sleep(5)

    def tap_farming(self, tap_x, tap_y, iter):
        os.system(f"adb -s {self.device_id} shell input tap 400 155")  # closing pop-up (optional)
        time.sleep(2)

        if iter == 0:
            sequence = " ".join(str(i) for i in range(1, 4))
            os.system(f'''adb -s {self.device_id} shell "for i in {sequence}; do input tap {tap_x} {tap_y}; sleep 5; done"''') # Farming button position
            print("Seeding completed, processing worm ...")
        else: 
            os.system(f"adb -s {self.device_id} shell input tap {tap_x} {tap_y}")  # Farming worm button position

        time.sleep(2)
        os.system(f"adb -s {self.device_id} shell input tap 400 125")  # closing pop-up (optional)
        time.sleep(2)

    async def start_Seed(self):
        self.handle_app_behavior(False)

        while True:
            print("\nStarting Seed .....")

            try: 
                self.handle_app_behavior(True)
                print("Claiming or Farming (Seed).......")
                tap_x = tap_y = 0

                for i in range(2):
                    if i == 0:
                        tap_x, tap_y = 400, 950 # Claim button position
                    else:
                        tap_x, tap_y = 400, 705 # Worm button position
                    self.tap_farming(tap_x, tap_y, i)

                print("Successfully Claimed or Farmed, Ready to exit for now......")
                total_seconds = 5400 # 1.5 hours in seconds
                wake_up_time = time.strftime("%H:%M:%S", time.localtime(time.time() + total_seconds))
                print(f'Farming (Seed) is in progress, Need to wait for {total_seconds} seconds (until {wake_up_time})....')
                self.handle_app_behavior(False)
            except Exception as e:
                print(f'Error: {e}')
                print("Whatever it is, let's start again\n")
            finally:
                await asyncio.sleep(total_seconds)

# if __name__ == "__main__":
#     telegram_mine = StartSeedFarming("emulator-5556")
#     asyncio.run(telegram_mine.start_Seed())