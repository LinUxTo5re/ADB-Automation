import os
import time
import asyncio
from checkADB import is_emulator_working

class StartHeadCoin:
    def __init__(self, device_id):
        self.device_id = device_id

    def handle_app_behavior(self, is_start, x_tap = 0, y_tap = 0, iter = 0):
        if is_start:
            print("Running Telegram...")
            if iter == 1:
                os.system(f"adb -s {self.device_id} shell input swipe 700 640 100 640 300") # swipe towards right
                time.sleep(3)
            os.system(f"adb -s {self.device_id} shell input tap {x_tap} {y_tap}")  # Head shortcut on homescreen
            time.sleep(45)
        else:
            print("Stopping Telegram...")
            os.system(f"adb -s {self.device_id} shell am force-stop org.telegram.messenger.web")
            time.sleep(5)
            os.system(f"adb -s {self.device_id} shell am force-stop org.telegram.messenger")
            time.sleep(3)
            os.system(f"adb -s {self.device_id} shell input swipe 100 640 700 640 300") #swipe towards left
            time.sleep(5)

    def tap_farming(self, is_daily_task):      
            os.system(f"adb -s {self.device_id} shell input tap 400 1030")  # Claim coins
            print("Claimed Head coins....")
            time.sleep(5)
            os.system(f"adb -s {self.device_id} shell input tap 650 930")  # NFT box
            time.sleep(5)
            os.system(f"adb -s {self.device_id} shell input swipe 384 1000 384 640 500") # scroll down to claim key
            time.sleep(3)
            os.system(f"adb -s {self.device_id} shell input tap 550 800")  # Claim key
            print("Claimed NFT key")
            time.sleep(3)

            sequence = " ".join(str(i) for i in range(1, 500))
            os.system(f'''adb -s {self.device_id} shell "for i in {sequence}; do input tap 400 400; sleep 0.3; done"''') # Farming button position (diamond)
            time.sleep(5)
            print("Claimed Diamond.....")

            if is_daily_task:
                os.system(f"adb -s {self.device_id} shell input tap 400 1130")  # Earn btn position
                time.sleep(3)
                os.system(f"adb -s {self.device_id} shell input tap 350 470")  # Daily reward btn position
                time.sleep(3)
                os.system(f"adb -s {self.device_id} shell input tap 400 1100")  # Claim daily reward
                print('Claimed Daily reward')
            time.sleep(5)

    async def start_Head(self):
        self.handle_app_behavior(False)
        count, is_daily_task = 0 , False
        while True:
            print("\nStarting Head .....")
            is_daily_task = count % 6 == 0 # check after 24 hours

            try: 
                for _ in range(2): # for 2 diff devices
                    if is_emulator_working():
                        x_tap, y_tap = (110, 650) if _ == 0 else (300, 650)
                        self.handle_app_behavior(True, x_tap, y_tap, _)
                        print("Claiming or Farming (Head).......")
                        self.tap_farming(is_daily_task)
                        print(f"Successfully Claimed or Farmed, Ready to exit for now for device: {_ + 1}......")
                        self.handle_app_behavior(False)
                    else:
                        raise ValueError("ADB NOT FOUND.....")
                total_seconds = 14400 # 4 hours
                wake_up_time = time.strftime("%H:%M:%S", time.localtime(time.time() + total_seconds))
                print(f'Farming (Head) is in progress, Need to wait for {total_seconds} seconds (until {wake_up_time})....')
                    
            except Exception as e:
                print(f'Error: {e}')
                print("Whatever it is, let's start after 2 minutes......\n")
                time.sleep(120)
            else:
                count = count + 1
                await asyncio.sleep(total_seconds)

# if __name__ == "__main__":
#     telegram_mine = StartHeadCoin("127.0.0.1:6555")
#     asyncio.run(telegram_mine.start_Head())