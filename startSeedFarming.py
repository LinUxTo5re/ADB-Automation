import os
import time
import asyncio
from checkADB import is_emulator_working

class StartSeedFarming:
    def __init__(self, device_id):
        self.device_id = device_id

    def handle_app_behavior(self, is_start, x_tap = 0, y_tap = 0, iter = 0):
        if is_start:
            print("Running Telegram...")
            if iter == 1:
                os.system(f"adb -s {self.device_id} shell input swipe 700 640 100 640 300") # swipe towards right
                time.sleep(3)
            os.system(f"adb -s {self.device_id} shell input tap {x_tap} {y_tap}")  # Seed shortcut on homescreen
            time.sleep(20)
        else:
            print("Stopping Telegram...")
            os.system(f"adb -s {self.device_id} shell am force-stop org.telegram.messenger.web")
            time.sleep(5)
            os.system(f"adb -s {self.device_id} shell am force-stop org.telegram.messenger")
            time.sleep(3)
            os.system(f"adb -s {self.device_id} shell input swipe 100 640 700 640 300") #swipe towards left
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
            os.system(f"adb -s {self.device_id} shell input tap 250 750")  # Christmas gift --> remove later

        time.sleep(2)
        os.system(f"adb -s {self.device_id} shell input tap 400 125")  # closing pop-up (optional)
        time.sleep(2)

    async def start_Seed(self):
        self.handle_app_behavior(False)

        while True:
            print("\nStarting Seed .....")

            try: 
                for _ in range(2): # for 2 diff devices
                    if is_emulator_working():
                        x_tap, y_tap = (470, 650) if _ == 0 else (300, 900)
                        self.handle_app_behavior(True, x_tap, y_tap, _)
                        print("Claiming or Farming (Seed).......")
                        tap_x = tap_y = 0

                        for i in range(2):
                            if i == 0:
                                tap_x, tap_y = 400, 950 # Claim button position
                            else:
                                tap_x, tap_y = 400, 705 # Worm button position
                            self.tap_farming(tap_x, tap_y, i)

                        print(f"Successfully Claimed or Farmed, Ready to exit for now for device: {_ + 1}......")
                        self.handle_app_behavior(False)
                    else:
                        raise ValueError("ADB NOT FOUND.....")   
                total_seconds = 5400 # 1.5 hours in seconds
                wake_up_time = time.strftime("%H:%M:%S", time.localtime(time.time() + total_seconds))
                print(f'Farming (Seed) is in progress, Need to wait for {total_seconds} seconds (until {wake_up_time})....')
                                                       
            except Exception as e:
                print(f'Error: {e}')
                print("Whatever it is, let's start after 2 minutes......\n")
                time.sleep(120)
            else:
                await asyncio.sleep(total_seconds)

# if __name__ == "__main__":
#     telegram_mine = StartSeedFarming("127.0.0.1:6555")
#     asyncio.run(telegram_mine.start_Seed())