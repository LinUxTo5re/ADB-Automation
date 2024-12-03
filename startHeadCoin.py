import os
import time
import asyncio

class StartHeadCoin:
    def __init__(self, device_id):
        self.device_id = device_id

    def handle_app_behavior(self, is_start):
        if is_start:
            print("Running Telegram...")
            os.system(f"adb -s {self.device_id} shell input tap 110 650")  # Head shortcut on homescreen
            time.sleep(30)
        else:
            print("Stopping Telegram...")
            os.system(f"adb -s {self.device_id} shell am force-stop org.telegram.messenger.web")
            time.sleep(5)

    def tap_farming(self):      
            os.system(f"adb -s {self.device_id} shell input tap 400 1030")  # Claim coins
            print("Claimed Head coins....")
            time.sleep(5)
            os.system(f"adb -s {self.device_id} shell input tap 650 930")  # NFT box
            time.sleep(5)
            os.system(f"adb -s {self.device_id} shell input swipe 384 1000 384 640 500") # scroll down to claim key
            time.sleep(3)
            os.system(f"adb -s {self.device_id} shell input tap 550 800")  # Claim key
            time.sleep(3)
            print("Claimed NFT key")

            sequence = " ".join(str(i) for i in range(1, 500))
            os.system(f'''adb -s {self.device_id} shell "for i in {sequence}; do input tap 400 400; sleep 0.3; done"''') # Farming button position
            time.sleep(5)
            print("Claimed Diamond.....")

            os.system(f"adb -s {self.device_id} shell input tap 400 1130")  # Earn btn position
            time.sleep(3)
            os.system(f"adb -s {self.device_id} shell input tap 350 470")  # Daily reward btn position
            time.sleep(3)
            os.system(f"adb -s {self.device_id} shell input tap 400 1100")  # Claim daily reward
            print('Claimed Daily reward')

    async def start_Head(self):
        self.handle_app_behavior(False)

        while True:
            print("\nStarting Head .....")

            try: 
                self.handle_app_behavior(True)
                print("Claiming or Farming (Head).......")
                self.tap_farming()
                print("Successfully Claimed or Farmed, Ready to exit for now......")
                total_seconds = 7200 # 2 hours
                wake_up_time = time.strftime("%H:%M:%S", time.localtime(time.time() + total_seconds))
                print(f'Farming (Head) is in progress, Need to wait for {total_seconds} seconds (until {wake_up_time})....')
                self.handle_app_behavior(False)
            except Exception as e:
                print(f'Error: {e}')
                print("Whatever it is, let's start again\n")
            finally:
                await asyncio.sleep(total_seconds)

# if __name__ == "__main__":
#     telegram_mine = StartHeadCoin("127.0.0.1:6555")
#     asyncio.run(telegram_mine.start_Head())