import os
import time
import asyncio

class StartTonKombat:
    def __init__(self, device_id):
        self.device_id = device_id

    def handle_app_behavior(self, is_start):
        if is_start:
            print("Running Telegram...")
            os.system(f"adb -s {self.device_id} shell input swipe 700 640 100 640 300") # swipe towards right
            time.sleep(3)
            os.system(f"adb -s {self.device_id} shell input tap 475 175")  # TON shortcut on homescreen
            time.sleep(15)
        else:
            print("Stopping Telegram...")
            os.system(f"adb -s {self.device_id} shell am force-stop org.telegram.messenger.web")
            time.sleep(5)
            os.system(f"adb -s {self.device_id} shell input swipe 100 640 700 640 300") #swipe towards left
            time.sleep(5)

    def tap_farming(self, is_fight_required):
        sequence = " ".join(str(i) for i in range(1, 3))        
        os.system(f'''adb -s {self.device_id} shell "for i in {sequence}; do input tap 450 950; sleep 5; done"''')  # Farming button position
        time.sleep(5)

        if is_fight_required:
            print("Playing fights..... wait for 5 fights (max. 5 min)")
            for _ in range(5):
                os.system(f'''adb -s {self.device_id} shell input tap 400 1115''')  # Kombat btn position
                time.sleep(3)
                os.system(f'''adb -s {self.device_id} shell input tap 500 950''')  # Fight btn position
                time.sleep(45) # wating to fight get complete
                os.system(f'''adb -s {self.device_id} shell input tap 550 1130''')  # Next fight btn position
                time.sleep(3)
                if _ == 4:
                    os.system(f'''adb -s {self.device_id} shell input tap 100 1120''')  # Home btn position
                    time.sleep(3)
                    continue
                os.system(f'''adb -s {self.device_id} shell input tap 500 1100''')  # Play again btn position
        
        os.system(f'''adb -s {self.device_id} shell input tap 100 1115''')  # Menu button position
        time.sleep(3)

        os.system(f'''adb -s {self.device_id} shell input tap 350 350''')  # Earn button position
        time.sleep(3)

        os.system(f'''adb -s {self.device_id} shell input tap 350 1100''')  # Daily bonus button position
        time.sleep(3)

    async def start_TON(self):
        self.handle_app_behavior(False)
        is_fight_required = True
        count = 1
        while True:
            print("\nStarting TON .....")

            try:
                if count % 2 == 0:
                    is_fight_required = False

                self.handle_app_behavior(True)
                print("Claiming or Farming (TON).......")
                self.tap_farming(is_fight_required)
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
                count = count + 1

# if __name__ == "__main__":
#     telegram_mine = StartTonKombat("127.0.0.1:6555")
#     asyncio.run(telegram_mine.start_TON())