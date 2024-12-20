import os
import time
import asyncio
from checkADB import is_emulator_working
from closeAllRecentApps import clear_all_recent_apps

class StartSpellBoosting:
    def __init__(self, device_id):
        self.device_id = device_id

    def handle_app_behavior(self, is_start, x_tap = 0, y_tap = 0, iter = 0):
        if is_start:
            print("Running Telegram...")
            if iter == 1:
                os.system(f"adb -s {self.device_id} shell input swipe 700 640 100 640 300") # swipe towards right
                time.sleep(3)
            os.system(f"adb -s {self.device_id} shell input tap {x_tap} {y_tap}")  # Spell shortcut on homescreen
            time.sleep(20)
        else:
            print("Stopping Telegram...")
            os.system(f"adb -s {self.device_id} shell am force-stop org.telegram.messenger.web")
            time.sleep(5)
            os.system(f"adb -s {self.device_id} shell am force-stop org.telegram.messenger")
            time.sleep(3)
            os.system(f"adb -s {self.device_id} shell input swipe 100 640 700 640 300") #swipe towards left
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
                for _ in range(2): # for 2 diff devices
                    if is_emulator_working():
                        x_tap, y_tap = (655, 655) if _ == 0 else (115, 900)
                        self.handle_app_behavior(True, x_tap, y_tap, _)
                        print("Claiming or Farming (Spell).......")
                        self.tap_farming()
                        print(f"Successfully Claimed or Farmed, Ready to exit for now for device: {_ + 1}......")
                        self.handle_app_behavior(False)
                    else:
                        raise ValueError("ADB NOT FOUND.....")
                total_seconds = 7200 # 2 hours in seconds
                wake_up_time = time.strftime("%H:%M:%S", time.localtime(time.time() + total_seconds))
                print(f'Farming (Spell) is in progress, Need to wait for {total_seconds} seconds (until {wake_up_time})....')
                    
            except Exception as e:
                print(f'Error: {e}')
                print("Whatever it is, let's start after 2 minutes......\n")
                time.sleep(120)
            else:
                clear_all_recent_apps()
                await asyncio.sleep(total_seconds)
# if __name__ == "__main__":
#     telegram_mine = StartSpellBoosting("127.0.0.1:6555")
#     asyncio.run(telegram_mine.start_Spell())