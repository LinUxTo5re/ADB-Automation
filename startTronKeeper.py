import os
import time
import asyncio

class StartTronKeeper:
    def __init__(self, device_id):
        self.device_id = device_id

    def handle_app_behavior(self, is_start):
        adb_command = "adb -s {0} shell ".format(self.device_id)
        if is_start:
            print("Running Telegram...")
            time.sleep(1)
            os.system(f"{adb_command}input tap 550 450")  # TronKeeper shortcut on homescreen
            time.sleep(15)
        else:
            print("Stopping Telegram...")
            os.system(f"{adb_command}am force-stop org.telegram.messenger")
            time.sleep(5)

    def tap_farming(self, tap_x, tap_y):
        for _ in range(3): # daily 3 free hold actions
            os.system(f'''adb -s {self.device_id} shell  input tap 400 400''')  # closing pop-up (optional)
            time.sleep(2)
            os.system(f'''adb -s {self.device_id} shell "input swipe {tap_x} {tap_y} {tap_x} {tap_y} 35000"''')  # Hold button for 35 seconds (extra 5 sec added)
            time.sleep(5)
            os.system(f'''adb -s {self.device_id} shell  input tap 400 400''')  # closing pop-up (optional)
            time.sleep(2)
      
        os.system(f"adb -s {self.device_id} shell input tap 186 1100") # clicking earn open league coins for next iter

    async def start_Tron(self):
        self.handle_app_behavior(False)

        while True:
            print("\nstarting TronKeeper .....")

            try:
                self.handle_app_behavior(True)
                print("Claiming or Farming (TronKeeper).......")
                tap_x = tap_y = 0
                for i in range(2): # usdt and earn open league coins
                    if i == 0:
                        tap_x, tap_y = 400, 900
                    else: 
                        print('earned usdt, now earning open league coins')
                        tap_x, tap_y = 400, 950
                    self.tap_farming(tap_x, tap_y)   

                total_seconds = 3600 # 1 hours
                wake_up_time = time.strftime("%H:%M:%S", time.localtime(time.time() + total_seconds))
                print(f'Farming is in progress, Need to wait for {total_seconds} seconds (until {wake_up_time})....')
                self.handle_app_behavior(False)

            except Exception as e:
                print(f'Error: {e}')
                print("Whatever it is, let's start again\n")
            finally:
                await asyncio.sleep(total_seconds)

# if __name__ == "__main__":
#     telegram_mine = StartTronKeeper("emulator-5554")
#     asyncio.run(telegram_mine.start_Tron())