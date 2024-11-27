import os
import time
import random

device_id = '127.0.0.1:6555'

def tap_random():
    start_time = time.time() 
    while time.time() - start_time < 58:  
        x = random.randint(30, 1030)
        y = random.randint(250, 1790)
        os.system(f"adb -s {device_id} shell input tap {x} {y}")

if __name__ == '__main__':
    os.system(f'adb -s {device_id} shell input tap 908 1615')
    tap_random()
