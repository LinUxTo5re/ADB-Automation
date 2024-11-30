import os

if __name__ == '__main__':
    print('hello world')
    # os.system(f"adb -s emulator-5556 shell input tap 550 1000")
    os.system(f'''adb -s emulator-5554 shell "for i in $(seq 1 600); do input tap 400 750; sleep 0.05; done"''')

    