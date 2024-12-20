import os
import time
import asyncio
from checkADB import is_emulator_working

class StartSwitchClaiming:
    def __init__(self, device_id):
        self.device_id = device_id

    def handle_app_behavior(self, is_start, x_tap = 0, y_tap = 0, iter = 0):
        if is_start:
            print("Running Telegram...")
            if iter == 1:
                os.system(f"adb -s {self.device_id} shell input swipe 700 640 100 640 300") # swipe towards right
                time.sleep(3)
            os.system(f"adb -s {self.device_id} shell input tap {x_tap} {y_tap}")  # Switch shortcut on homescreen
            time.sleep(20)
        else:
            print("Stopping Telegram...")
            os.system(f"adb -s {self.device_id} shell am force-stop org.telegram.messenger.web")
            time.sleep(5)
            os.system(f"adb -s {self.device_id} shell am force-stop org.telegram.messenger")
            time.sleep(3)
            os.system(f"adb -s {self.device_id} shell input swipe 100 640 700 640 300") #swipe towards left
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
                for _ in range(2): # for 2 diff devices
                    if is_emulator_working():
                        x_tap, y_tap = (480, 900) if _ == 0 else (475, 650)
                        self.handle_app_behavior(True, x_tap, y_tap, _)
                        is_daily_task = count % 4 == 0
                        print("Claiming or Farming (Switch).......")
                        self.tap_farming(is_daily_task)
                        print(f"Successfully Claimed or Farmed, Ready to exit for now for device: {_ + 1}......")
                        self.handle_app_behavior(False)
                    else:
                        raise ValueError("ADB NOT FOUND.....")
                total_seconds = 10800 # 3 hours in seconds
                wake_up_time = time.strftime("%H:%M:%S", time.localtime(time.time() + total_seconds))
                print(f'Farming (Switch) is in progress, Need to wait for {total_seconds} seconds (until {wake_up_time})....')
                    
            except Exception as e:
                print(f'Error: {e}')
                print("Whatever it is, let's start after 2 minutes......\n")
                time.sleep(120)
            else:
                count = count + 1
                await asyncio.sleep(total_seconds)

# if __name__ == "__main__":
#     telegram_mine = StartSwitchClaiming("127.0.0.1:6555")
#     asyncio.run(telegram_mine.start_Switch())