import os
import time
import asyncio

class StartTonKombat:
    def __init__(self, device_id):
        self.device_id = device_id

    def handle_app_behavior(self, is_start):
        if is_start:
            print("Running Telegram...")
            os.system(f"adb -s {self.device_id} shell input tap 159 280")  # TON shortcut on homescreen
            time.sleep(15)
        else:
            print("Stopping Telegram...")
            os.system(f"adb -s {self.device_id} shell am force-stop org.telegram.messenger")
            time.sleep(5)

    def tap_farming(self):
        os.system(f'''adb -s {self.device_id} shell "for i in $(seq 1 3); do input tap 600 1950; sleep 5; done"''')  # Farming button position
        time.sleep(5)

        os.system(f'''adb -s {self.device_id} shell input tap 150 2200''')  # Menu button position
        time.sleep(3)

        os.system(f'''adb -s {self.device_id} shell input tap 500 600''')  # Daily bonus button position
        time.sleep(3)

        os.system(f'''adb -s {self.device_id} shell input tap 500 2150''')  # Daily bonus button position
        time.sleep(3)

    async def start_TON(self):
        self.handle_app_behavior(False)

        while True:
            print("\nStarting TON .....")

            try: 
                self.handle_app_behavior(True)
                print("Claiming or Farming (TON).......")
                self.tap_farming()
                print("Successfully Claimed or Farmed, Ready to exit for now......")
                total_seconds = 3300 # 55 minutes in seconds
                wake_up_time = time.strftime("%H:%M:%S", time.localtime(time.time() + total_seconds))
                print(f'Farming (TON) is in progress, Need to wait for {total_seconds} seconds (until {wake_up_time})....')
                self.handle_app_behavior(False)
            except Exception as e:
                print(f'Error: {e}')
                print("Whatever it is, let's start again\n")
            finally:
                await asyncio.sleep(total_seconds)

if __name__ == "__main__":
    telegram_mine = StartTonKombat("emulator-5554")
    asyncio.run(telegram_mine.start_TON())