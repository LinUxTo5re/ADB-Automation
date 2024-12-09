import subprocess

def is_emulator_working():
    try:
        result = subprocess.run("adb devices", shell=True, text=True, capture_output=True)
        stdout = result.stdout.strip()
        stderr = result.stderr.strip()

        if result.returncode != 0:
            return False
        
        devices_output = stdout.splitlines()
        if len(devices_output) > 1: 
            for line in devices_output[1:]:
                device_info = line.split()
                if len(device_info) == 2:
                    device_id, status = device_info
                    if status == "device":
                        return True
                    elif status == "offline":
                        print(f"Device {device_id} is offline.")
                        return False
        else:
            return False
    except Exception as e:
        return False
