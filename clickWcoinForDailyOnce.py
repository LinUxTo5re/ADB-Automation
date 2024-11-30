import os

device_id = 'emulator-5554'

while True:
    os.system(f'''adb -s {device_id} shell "for i in $(seq 1 600); do input tap 400 725; done"''')

