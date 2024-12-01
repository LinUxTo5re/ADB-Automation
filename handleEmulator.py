import asyncio
import os
import time

class StartEmulators:
    def __init__(self) :
        self.emulator_path = r"C:\Program Files (x86)\Android\android-sdk\emulator"
        self.adb_path = r"C:\Program Files (x86)\Android\android-sdk\platform-tools"

    async def start_emulator(self, emulator_name):
        command = ["emulator", "-avd", emulator_name]
        current_time = time.strftime("%H:%M:%S", time.localtime(time.time()))
        print(f"Emulator '{emulator_name}' is not running or has a different IP. Starting it... (at: {current_time})")
        stdout, stderr = await execute_command(self.emulator_path, command)
        if stderr:
            print(f"Error: {stderr}")
        else:
            print(f"Emulator '{emulator_name}' started...") 

    async def execute_command(self, path, command):
        os.chdir(path)
        try:
            process = await asyncio.create_subprocess_exec(
                *command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            return stdout.decode().strip(), stderr.decode().strip()
        except Exception as e:
            return None, str(e)
        
emulator_path = r"C:\Program Files (x86)\Android\android-sdk\emulator"
adb_path = r"C:\Program Files (x86)\Android\android-sdk\platform-tools"

async def execute_command(path, command):
    os.chdir(path)
    try:
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        return stdout.decode().strip(), stderr.decode().strip()
    except Exception as e:
        return None, str(e)

async def list_emulators():
    command = ["emulator", "-list-avds"]
    stdout, stderr = await execute_command(emulator_path, command)
    if stderr:
        print(f"Error: {stderr}")
    else:
        emulators = stdout.splitlines()[1:]
        if emulators:
            return emulators
        else:
            print("No emulators found.")
            return []

async def get_emulator_status():
    command = ["adb", "devices"]
    stdout, stderr = await execute_command(adb_path, command)
    if stderr:
        print(f"Error: {stderr}")
    else:
        devices = stdout.splitlines()[1:]
        running_devices = []
        if devices:
            for device in devices:
                if device:
                    device_name, _ = device.split("\t")
                    running_devices.append(device_name)
        return running_devices

async def main():
    os.system('cls')
    emulators_ip = {
        'clone-1_nexus_4_-_api_35': 'emulator-5554',
    }

    while True:
        emulators_list = await list_emulators()
        running_devices = await get_emulator_status()

        print(f"Available emulators: {emulators_list}")
        for emulator in emulators_list:
                if emulator in emulators_ip:
                    if emulators_ip[emulator] not in running_devices:
                        start_device = StartEmulators()
                        await start_device.start_emulator(emulator)

        print("Will check after 30 seconds...")
        await asyncio.sleep(30)

if __name__ == "__main__":
    asyncio.run(main())
