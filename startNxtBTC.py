import os
import time
import asyncio

class StartNxtBTC:
    def __init__(self, device_id):
        self.device_id = device_id

    def handle_app_behavior(self, is_start):
        if is_start:
            print("Running Telegram...")
            os.system(f"adb -s {self.device_id} shell input tap 415 350")  # NxtBTC shortcut on homescreen
            time.sleep(30)
        else:
            print("Stopping Telegram...")
            os.system(f"adb -s {self.device_id} shell am force-stop org.telegram.messenger")
            time.sleep(5)

    def tap_farming(self):
        os.system(f'''adb -s {self.device_id} shell input tap 400 2200''')  #Mine btn position
        time.sleep(3)

        os.system(f'''adb -s {self.device_id} shell "for i in $(seq 1 3); do input tap 759 1450; sleep 5; done"''')  # Claiming btn position
        time.sleep(5)

        os.system(f'''adb -s {self.device_id} shell "for i in $(seq 1 3); do input tap 300 1450; sleep 5; done"''')  # Mining btn position
        time.sleep(5)

        os.system(f'''adb -s {self.device_id} shell input tap 150 2175''')  # Home btn position
        os.system(f'''adb -s {self.device_id} shell input tap 150 1575''')  # Daily bonus position
        time.sleep(3)

    async def start_NxtBTC(self):
        self.handle_app_behavior(False)

        while True:
            print("\nStarting NxtBTC .....")

            try: 
                self.handle_app_behavior(True)
                print("Claiming or Farming (NxtBTC).......")
                self.tap_farming()
                print("Successfully Claimed or Farmed, Ready to exit for now......")
                total_seconds = 2700 # 45 minutes in seconds
                wake_up_time = time.strftime("%H:%M:%S", time.localtime(time.time() + total_seconds))
                print(f'Farming (NxtBTC) is in progress, Need to wait for {total_seconds} seconds (until {wake_up_time})....')
                self.handle_app_behavior(False)
            except Exception as e:
                print(f'Error: {e}')
                print("Whatever it is, let's start again\n")
            finally:
                await asyncio.sleep(total_seconds)

if __name__ == "__main__":
    telegram_mine = StartNxtBTC("emulator-5554")
    asyncio.run(telegram_mine.start_NxtBTC())