import os

while True:    
    os.system(f'''adb -s 127.0.0.1:6555 shell input tap 400 700''') # Farming button position
