import os
import time
import asyncio
from checkADB import is_emulator_working

class startWcoin:
    def __init__(self, device_id):
        self.device_id = device_id
        self.sleep_val = 900

    def tap_center(self, is_WAI):
        sequence = " ".join(str(i) for i in range(1, 600))
        os.system(f'''adb -s {self.device_id} shell "for i in {sequence}; do input tap 400 700; sleep 0.3; done"''') # Farming button position
        print("Finished all taps.")

        if is_WAI:
            time.sleep(5)
            os.system(f"adb -s {self.device_id} shell input tap 520 415")  # Tap on the W-AI
            time.sleep(10)

            sequence = " ".join(str(i) for i in range(1, 4))
            os.system(f'''adb -s {self.device_id} shell "for i in {sequence}; do input tap 400 1100; sleep 2; done;"''')  # Claim W-AI
            time.sleep(2)

    def handle_app_behavior(self, is_start):
        try:
            if not is_start:
                print("Stopping Telegram...")
                os.system(f"adb -s {self.device_id} shell am force-stop org.telegram.messenger.web")  # Close Telegram
                time.sleep(5)
            else:
                print("Running Telegram...")
                os.system(f"adb -s {self.device_id} shell input tap 650 400")  # Tap on the shortcut
                time.sleep(20)
        except Exception as e:
            print(f"Exception(W-Coin): {e}")

    async def start_Wcoin(self):
        count, is_WAI = 0, False
        self.handle_app_behavior(False)
        while True:
            try:
                if is_emulator_working():
                    is_WAI = count % 45 == 0 # Do check W-AI after every 3 hours or 45 counts
                    print("\nStarting mining W-coin...")
                    self.handle_app_behavior(True)
                    self.tap_center(is_WAI)                
                    sleep_time = time.strftime("%H:%M:%S", time.localtime(time.time() + self.sleep_val))
                    print(f"sleeping for {self.sleep_val} seconds (until {sleep_time}).")
                    self.handle_app_behavior(False)
                else:
                    raise ValueError("ADB NOT FOUND.....")
            except Exception as e:
                print(f'Error: {e}')
                print("Whatever it is, let's start after 2 minutes......\n")
                time.sleep(120)
            else:
                count = count + 1
                await asyncio.sleep(self.sleep_val)

# if __name__ == "__main__":
#     telegram_mine = startWcoin("127.0.0.1:6555")
#     asyncio.run(telegram_mine.start_Wcoin())