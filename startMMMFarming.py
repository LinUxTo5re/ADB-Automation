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
            os.system(f"{adb_command}input tap 300 650")  # mmm shortcut on homescreen
            time.sleep(20)
        else:
            print("Stopping Telegram...")
            os.system(f"{adb_command}am force-stop org.telegram.messenger.web")
            time.sleep(5)

    def tap_farming(self, is_daily_reward):
        sequence = " ".join(str(i) for i in range(1, 6))
        os.system(f'''adb -s {self.device_id} shell "for i in {sequence}; do input tap 400 1000; sleep 5; done"''') # Farming button position
        time.sleep(5)

        if is_daily_reward:
            os.system(f"adb -s {self.device_id} shell input tap 530 1100") # Airdrop btn
            time.sleep(5)
            os.system(f"adb -s {self.device_id} shell input tap 650 520") # Daily reward btn
            time.sleep(5)
 
    async def start_MMM(self):
        self.handle_app_behavior(False)
        count, is_daily_reward = 0, False
        while True:
            print("\nstarting Mr. MEME .....")
            is_daily_reward = count % 3 == 0

            try:
                self.handle_app_behavior(True)
                print("Claiming or Farming (Mr. MEME).......")
                self.tap_farming(is_daily_reward)                    
                total_seconds = 7200 # 2 hours in seconds
                wake_up_time = time.strftime("%H:%M:%S", time.localtime(time.time() + total_seconds))
                print(f'Farming (Mr. MEME) is in progress, Need to wait for {total_seconds} seconds (until {wake_up_time})....')
                self.handle_app_behavior(False)

            except Exception as e:
                print(f'Error: {e}')
                print("Whatever it is, let's start again\n")
            finally:
                count = count + 1
                await asyncio.sleep(total_seconds)

# if __name__ == "__main__":
#     telegram_mine = StartMMMFarming("emulator-5554")
#     asyncio.run(telegram_mine.start_MMM())