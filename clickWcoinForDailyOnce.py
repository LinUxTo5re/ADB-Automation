import os
import time
import random

device_id = '127.0.0.1:6555'
def tap_center():
    os.system(f"adb -s {device_id} shell input tap 500 1250")

end_time = time.time() + 5 * 60
total_clicks = 0
while time.time() < end_time:
    tap_center()
    total_clicks = total_clicks + 1
    print(f"total clicks yet: {total_clicks}")
