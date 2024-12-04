import os
import time

class GenymotionManager:
    def __init__(self, emulator_name):
        self.emulator_name = emulator_name

    # Get running emulator details
    def get_running_emulator(self):
        output = os.popen("""./gmtool admin list""").read()

        if output:
            lines = output.splitlines()
            for line in lines[2:]: 
                cols = line.split("|")
                if len(cols) >= 4:
                    state = cols[0].strip()
                    name = cols[3].strip()
                    if state == "On":
                        return name
        return None

    # Stop running emulator
    def stop_emulator(self, name):
        print(f"Stopping emulator: {name}\n")
        os.system(f"""./gmtool admin stop '{name}'""")

    # Restart ADB server
    def restart_adb_server(self):
        print("Restarting ADB server...")
        os.system("""adb kill-server""")
        os.system("""adb start-server""")

    # Start emulator specially designed for telegram mining
    def start_emulator(self, name):
        print(f"Starting emulator: {name}")
        os.system(f"""./gmtool admin start '{name}'""")

    def manage_emulator(self):
        os.chdir(os.path.expanduser('/opt/genymobile/genymotion'))
        self.stop_emulator(self.emulator_name)
        while True:
            print(f"\nHandling genymotion emulator: {self.emulator_name}")
            sleep_time = time.strftime("%H:%M:%S", time.localtime(time.time()))

            running_emulator = self.get_running_emulator()
            if not running_emulator == self.emulator_name or not running_emulator:
                print("No running emulator found.")  
                self.restart_adb_server()
                self.start_emulator(self.emulator_name)
                print(f"Started Emulator: {self.emulator_name}")         
            elif running_emulator and running_emulator == self.emulator_name:
                print(f"Found running emulator: {running_emulator}")

            print(f"Will be back after 10 minutes (until {sleep_time})")
            time.sleep(600)   

if __name__ == '__main__':
    genyManager = GenymotionManager("TelegramBot")
    genyManager.manage_emulator()