import os
import time
import asyncio
import random
from checkADB import is_emulator_working

class StartNordomGates:
    def __init__(self, device_id):
        self.device_id = device_id

    def handle_app_behavior(self, is_start, x_tap = 0, y_tap = 0, iter = 0):
        if is_start:
            print("Running Telegram...")
            os.system(f"adb -s {self.device_id} shell input swipe 700 640 100 640 300") # swipe towards right
            time.sleep(3)
            os.system(f"adb -s {self.device_id} shell input tap {x_tap} {y_tap}")  # NordomG shortcut on homescreen
            time.sleep(30)
        else:
            print("Stopping Telegram...")
            os.system(f"adb -s {self.device_id} shell am force-stop org.telegram.messenger.web")
            time.sleep(5)
            os.system(f"adb -s {self.device_id} shell am force-stop org.telegram.messenger")
            time.sleep(3)
            os.system(f"adb -s {self.device_id} shell input swipe 100 640 700 640 300") #swipe towards left
            time.sleep(5)

    def tap_farming(self, is_Knock_Knock):
        if is_Knock_Knock:
            print('Playing Knock-Knock.....')
            os.system(f"adb -s {self.device_id} shell input tap 400 1000") # Knock Knock, Who's There?
            time.sleep(2)
            sequence = " ".join(str(i) for i in range(1, 350))
            os.system(f'''adb -s {self.device_id} shell "for i in {sequence}; do input tap 425 700; done"''')  # Knock on the door
        
        loc_pick = [200, 400, 600]
        for _ in range(10):
            time.sleep(2)
            x_random_pick = random.choice(loc_pick)
            os.system(f'''adb -s {self.device_id} shell input tap {x_random_pick} 750''') # pick random gate
            time.sleep(3)
            os.system(f'''adb -s {self.device_id} shell input tap 400 1075''') # click on claim the prize
        time.sleep(5)

    async def start_NordomG(self):
        self.handle_app_behavior(False)
        count, is_Knock_Knock = 0, False
        while True:
            print("\nStarting NardomG .....")

            is_Knock_Knock = count % 3 == 0

            try: 
                for _ in range(2): # for 2 diff devices
                    if is_emulator_working():
                        x_tap, y_tap = (660, 165) if _ == 0 else (650, 900)
                        self.handle_app_behavior(True, x_tap, y_tap, _)
                        print("Claiming or Farming (NardomG).......")
                        self.tap_farming(is_Knock_Knock)
                        print(f"Successfully Claimed or Farmed, Ready to exit for now for device: {_ + 1}.....")
                        self.handle_app_behavior(False)
                    else:
                        raise ValueError("ADB NOT FOUND.....")
                total_seconds =  6300 # 105 minutes in seconds (1 hour and 45 minutes)
                wake_up_time = time.strftime("%H:%M:%S", time.localtime(time.time() + total_seconds))
                print(f'Farming (NordomG) is in progress, Need to wait for {total_seconds} seconds (until {wake_up_time})....')
                    
            except Exception as e:
                print(f'Error: {e}')
                print("Whatever it is, let's start after 2 minutes......\n")
                time.sleep(120)
            else:
                count = count + 1
                await asyncio.sleep(total_seconds)

# if __name__ == "__main__":
#     telegram_mine = StartNordomGates("127.0.0.1:6555")
#     asyncio.run(telegram_mine.start_NordomG())