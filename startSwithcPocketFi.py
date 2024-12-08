import os
import time
import asyncio

class StartSwitchClaiming:
    def __init__(self, device_id):
        self.device_id = device_id

    def handle_app_behavior(self, is_start):
        if is_start:
            print("Running Telegram...")
            os.system(f"adb -s {self.device_id} shell input tap 480 900")  # Switch shortcut on homescreen
            time.sleep(20)
        else:
            print("Stopping Telegram...")
            os.system(f"adb -s {self.device_id} shell am force-stop org.telegram.messenger.web")
            time.sleep(5)

    def tap_farming(self, is_daily_task):      
        sequence = " ".join(str(i) for i in range(1, 3))
        os.system(f'''adb -s {self.device_id} shell "for i in {sequence}; do input tap 400 700; sleep 0.3; done"''') # Farming button position
        print("Claimed SWITCH....")
        time.sleep(5)

        if is_daily_task:
            os.system(f"adb -s {self.device_id} shell input tap 260 1100")  # Tasks btn position
            time.sleep(10)
            os.system(f"adb -s {self.device_id} shell input tap 300 515")  # PocketFi btn position
            time.sleep(10)
            os.system(f"adb -s {self.device_id} shell input tap 400 720")  # PocketFi btn position
            time.sleep(3)
            os.system(f"adb -s {self.device_id} shell input tap 350 1150")  # Claim daily boost
            print("Claimed daily boost....")
            time.sleep(3)

    async def start_Switch(self):
        self.handle_app_behavior(False)
        count, is_daily_task = 0, False
        while True:
            print("\nStarting Switch .....")

            try: 
                self.handle_app_behavior(True)
                is_daily_task = count % 8 == 0
                print("Claiming or Farming (Switch).......")
                self.tap_farming(is_daily_task)
                print("Successfully Claimed or Farmed, Ready to exit for now......")
                total_seconds = 10800 # 3 hours in seconds
                wake_up_time = time.strftime("%H:%M:%S", time.localtime(time.time() + total_seconds))
                print(f'Farming (Switch) is in progress, Need to wait for {total_seconds} seconds (until {wake_up_time})....')
                self.handle_app_behavior(False)
            except Exception as e:
                print(f'Error: {e}')
                print("Whatever it is, let's start again\n")
            finally:
                count = count + 1
                await asyncio.sleep(total_seconds)

# if __name__ == "__main__":
#     telegram_mine = StartSwitchClaiming("127.0.0.1:6555")
#     asyncio.run(telegram_mine.start_Switch())