import os

device_id = '127.0.0.1:6555'
sequence = " ".join(str(i) for i in range(1, 600))

while True:
    os.system(f'''adb -s {device_id} shell "for i in {sequence}; do input tap 400 700; done"''') # Farming button position
        
