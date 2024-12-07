import os
import time
import asyncio

class StartCGX:
    def __init__(self, device_id):
        self.device_id = device_id

    def handle_app_behavior(self, is_start):
        if is_start:
            print("Running Telegram...")
            os.system(f"adb -s {self.device_id} shell input swipe 700 640 100 640 300") # swipe towards right
            time.sleep(3)
            os.system(f"adb -s {self.device_id} shell input tap 475 400")  # CGX shortcut on homescreen
            time.sleep(30)
        else:
            print("Stopping Telegram...")
            os.system(f"adb -s {self.device_id} shell am force-stop org.telegram.messenger.web")
            time.sleep(3)
            os.system(f"adb -s {self.device_id} shell input swipe 100 640 700 640 300") #swipe towards left
            time.sleep(5)

    def tap_farming(self):
        os.system(f'''adb -s {self.device_id} shell input tap 375 1130''')  # for safety - home btn
        time.sleep(3)

        os.system(f'''adb -s {self.device_id} shell input swipe 384 1000 384 400 300''')  # Scroll down
        time.sleep(3)

        sequence = " ".join(str(i) for i in range(1, 3))        
        os.system(f'''adb -s {self.device_id} shell "for i in {sequence}; do input tap 400 975; sleep 5; done"''')  # Claiming btn position
        time.sleep(5)

        os.system(f'''adb -s {self.device_id} shell input tap 100 255''')  # Daily Bonus btn
        time.sleep(5)

        os.system(f'''adb -s {self.device_id} shell input tap 675 670''')  # claim daily bonus
        time.sleep(5)

    async def start_CGX(self):
        self.handle_app_behavior(False)

        while True:
            print("\nStarting CGX .....")

            try: 
                self.handle_app_behavior(True)
                print("Claiming or Farming (CGX).......")
                self.tap_farming()
                print("Successfully Claimed or Farmed, Ready to exit for now......")
                total_seconds = 2700 # 45 minutes in seconds
                wake_up_time = time.strftime("%H:%M:%S", time.localtime(time.time() + total_seconds))
                print(f'Farming (CGX) is in progress, Need to wait for {total_seconds} seconds (until {wake_up_time})....')
                self.handle_app_behavior(False)
            except Exception as e:
                print(f'Error: {e}')
                print("Whatever it is, let's start again\n")
            finally:
                await asyncio.sleep(total_seconds)

# if __name__ == "__main__":
#     telegram_mine = StartCGX("127.0.0.1:6555")
#     asyncio.run(telegram_mine.start_CGX())