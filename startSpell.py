import os
import time
import asyncio

class StartSpellBoosting:
    def __init__(self, device_id):
        self.device_id = device_id

    def handle_app_behavior(self, is_start):
        if is_start:
            print("Running Telegram...")
            os.system(f"adb -s {self.device_id} shell input tap 655 655")  # Spell shortcut on homescreen
            time.sleep(15)
        else:
            print("Stopping Telegram...")
            os.system(f"adb -s {self.device_id} shell am force-stop org.telegram.messenger.web")
            time.sleep(5)

    def tap_farming(self):      
        sequence = " ".join(str(i) for i in range(1, 6))
        os.system(f'''adb -s {self.device_id} shell "for i in {sequence}; do input tap 350 650; sleep 0.3; done"''') # Farming button position
        time.sleep(5)

    async def start_Spell(self):
        self.handle_app_behavior(False)

        while True:
            print("\nStarting Spell .....")

            try: 
                self.handle_app_behavior(True)
                print("Claiming or Farming (Spell).......")
                self.tap_farming()
                print("Successfully Claimed or Farmed, Ready to exit for now......")
                total_seconds = 5400 # 90 minutes in seconds
                wake_up_time = time.strftime("%H:%M:%S", time.localtime(time.time() + total_seconds))
                print(f'Farming (Spell) is in progress, Need to wait for {total_seconds} seconds (until {wake_up_time})....')
                self.handle_app_behavior(False)
            except Exception as e:
                print(f'Error: {e}')
                print("Whatever it is, let's start again\n")
            finally:
                await asyncio.sleep(total_seconds)

# if __name__ == "__main__":
#     telegram_mine = StartSpellBoosting("127.0.0.1:6555")
#     asyncio.run(telegram_mine.start_Spell())