import os
import time
import asyncio

class StartMMMFarming:
    def __init__(self, device_id):
        self.device_id = device_id

    def handle_app_behavior(self, is_start):
        adb_command = "adb -s {0} shell ".format(self.device_id)
        if is_start:
            print("Running Telegram...")
            time.sleep(1)
            os.system(f"{adb_command}input tap 100 600")  # mmm shortcut on homescreen
            time.sleep(15)
        else:
            print("Stopping Telegram...")
            os.system(f"{adb_command}am force-stop org.telegram.messenger")
            time.sleep(5)

    def tap_farming(self):
        os.system(f'''adb -s {self.device_id} shell "for i in $(seq 1 5); do input tap 400 950; sleep 0.03; done"''')  # farming btn position
        time.sleep(5)

    async def start_MMM(self):
        self.handle_app_behavior(False)

        while True:
            print("\nstarting Mr. MEME .....")

            try:
                self.handle_app_behavior(True)
                print("Claiming or Farming (Mr. MEME).......")
                self.tap_farming()                    
                total_seconds = 1800 # 30 minutes
                wake_up_time = time.strftime("%H:%M:%S", time.localtime(time.time() + total_seconds))
                print(f'Farming (Mr. MEME) is in progress, Need to wait for {total_seconds} seconds (until {wake_up_time})....')
                self.handle_app_behavior(False)

            except Exception as e:
                print(f'Error: {e}')
                print("Whatever it is, let's start again\n")
            finally:
                await asyncio.sleep(total_seconds)

# if __name__ == "__main__":
#     telegram_mine = StartMMMFarming("emulator-5554")
#     asyncio.run(telegram_mine.start_MMM())