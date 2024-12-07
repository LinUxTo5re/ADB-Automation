import os
import time
import asyncio

class StartTONxDAO:
    def __init__(self, device_id):
        self.device_id = device_id

    def handle_app_behavior(self, is_start):
        if is_start:
            print("Running Telegram...")
            os.system(f"adb -s {self.device_id} shell input swipe 700 640 100 640 300") # swipe towards right
            time.sleep(3)
            os.system(f"adb -s {self.device_id} shell input tap 650 400")  # TONxDAO shortcut on homescreen
            time.sleep(20)
        else:
            print("Stopping Telegram...")
            os.system(f"adb -s {self.device_id} shell am force-stop org.telegram.messenger.web")
            time.sleep(5)
            os.system(f"adb -s {self.device_id} shell input swipe 100 640 700 640 300") #swipe towards left
            time.sleep(5)

    def tap_farming(self):
        print('Holding (touch) for next 01 minute.....')
        os.system(f"adb -s {self.device_id} shell input swipe 400 700 400 700 60000") # hold for 01 minutes
        time.sleep(5)
        os.system(f"adb -s {self.device_id} shell input tap 675 1150") # Click on tasks
        time.sleep(3)
        print("Claiming daily task......")
        sequence = " ".join(str(i) for i in range(1, 3))
        os.system(f'''adb -s {self.device_id} shell "for i in {sequence}; do input tap 250 530; sleep 5; done"''')  # Click on emoji task
        time.sleep(5)

    async def start_TONxDAO(self):
        self.handle_app_behavior(False)

        while True:
            print("\nStarting TONxDAO .....")

            try: 
                self.handle_app_behavior(True)
                print("Claiming or Farming (TONxDAO).......")
                self.tap_farming()

                print("Successfully Claimed or Farmed, Ready to exit for now......")
                total_seconds = 10800 # 180 minutes in seconds (3 hours)
                wake_up_time = time.strftime("%H:%M:%S", time.localtime(time.time() + total_seconds))
                print(f'Farming (TONxDAO) is in progress, Need to wait for {total_seconds} seconds (until {wake_up_time})....')
                self.handle_app_behavior(False)
            except Exception as e:
                print(f'Error: {e}')
                print("Whatever it is, let's start again\n")
            finally:
                await asyncio.sleep(total_seconds)

# if __name__ == "__main__":
#     telegram_mine = StartTONxDAO("127.0.0.1:6555")
#     asyncio.run(telegram_mine.start_TONxDAO())