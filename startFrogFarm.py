import os
import time
import asyncio

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

    def tap_farming(self, tap_x, tap_y, is_daily_task):
        if is_daily_task:
            os.system(f"adb -s {self.device_id} shell input tap 500 1130") # click on tasks
            time.sleep(3)
            os.system(f"adb -s {self.device_id} shell input tap 400 375") # click on daily reward
            time.sleep(3)

        sequence = " ".join(str(i) for i in range(1, 3))
        os.system(f'''adb -s {self.device_id} shell "for i in {sequence}; do input tap {tap_x} {tap_y}; sleep 5; done"''') # Farming/daily reward button position
        time.sleep(5)

    async def start_FrogFarm(self):
        self.handle_app_behavior(False)
        count, is_daily_task = 0, False
        while True:
            print("\nStarting FrogFarm .....")

            try: 
                self.handle_app_behavior(True)
                is_daily_task = count % 48 == 0 # farming completes in 30 minutes and daily task in once in a day (24 hr=> 1440 min/30 min = 48 rounds)

                print("Claiming or Farming (FrogFarm).......")
                tap_x = tap_y = 0
                for _ in range(2): # 2 times for farming and claiming daily task
                    tap_x, tap_y = 350, 1000 # Farming btn position
                    
                    if is_daily_task:
                        print("Farming completed, now claiming daily reward...")
                        tap_x, tap_y = 400, 1100 # Daily task

                    self.tap_farming(tap_x, tap_y, is_daily_task)

                print("Successfully Claimed or Farmed, Ready to exit for now......")
                total_seconds = 900 # 15 minutes in seconds
                wake_up_time = time.strftime("%H:%M:%S", time.localtime(time.time() + total_seconds))
                print(f'Farming (FrogFarm) is in progress, Need to wait for {total_seconds} seconds (until {wake_up_time})....')
                self.handle_app_behavior(False)
            except Exception as e:
                print(f'Error: {e}')
                print("Whatever it is, let's start again\n")
            finally:
                count = count + 1
                await asyncio.sleep(total_seconds)

if __name__ == "__main__":
    telegram_mine = StartFrogFarmFarming("127.0.0.1:6555")
    asyncio.run(telegram_mine.start_FrogFarm())