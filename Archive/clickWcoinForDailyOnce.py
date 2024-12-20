import os

device_id = '127.0.0.1:6555'
sequence = " ".join(str(i) for i in range(1, 600))

while True:
    for _ in range(600):
        os.system(f'''adb -s {device_id} shell input tap 400 700''') # Farming button position
        
