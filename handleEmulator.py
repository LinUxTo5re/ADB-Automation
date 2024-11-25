import asyncio
import os

class GenymotionManager:
    def __init__(self, emulator_name, genymotion_path):
        self.genymotion_path = genymotion_path
        self.emulator_name = emulator_name

    async def run_command(self, command, cwd=None):
        try:
            process = await asyncio.create_subprocess_exec(
                *command,
                cwd=cwd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await process.communicate()
            if process.returncode == 0:
                return stdout.decode().strip()
            else:
                print(f"Command failed: {stderr.decode().strip()}")
                return None
        except Exception as e:
            print(f"Error while running command: {e}")
            return None

    # Get running emulator details
    async def get_running_emulator(self):
        output = await self.run_command(["./gmtool", "admin", "list"], cwd=self.genymotion_path)
        if output:
            lines = output.splitlines()
            for line in lines[2:]:  # Skip header lines
                cols = line.split("|")
                if len(cols) >= 4:
                    state = cols[0].strip()
                    name = cols[3].strip()
                    if state == "On":
                        return name
        return None

    # Stop running emulator
    async def stop_emulator(self, name):
        print(f"Stopping emulator: {name}")
        await self.run_command(["./gmtool", "admin", "stop", name], cwd=self.genymotion_path)

    # Restart ADB server
    async def restart_adb_server(self):
        print("Restarting ADB server...")
        await self.run_command(["adb", "kill-server"], cwd="/")
        await asyncio.sleep(5)
        await self.run_command(["adb", "start-server"], cwd="/")

    # Start emulator specially designed for telegram mining
    async def start_emulator(self, name):
        print(f"Starting emulator: {name}")
        await self.run_command(["./gmtool", "admin", "start", name], cwd=self.genymotion_path)

    async def manage_emulator(self):
        running_emulator = await self.get_running_emulator()
        if running_emulator:
            print(f"Found running emulator: {running_emulator}")
            await self.stop_emulator(running_emulator)
            await asyncio.sleep(5)
        else:
            print("No running emulator found.")

        await self.restart_adb_server()
        await self.start_emulator(self.emulator_name)

home_dir = os.path.expanduser("~")
genymotion_path = os.path.join(home_dir, "genymotion")

manager = GenymotionManager("CloneTMP - Samsung Galaxy S23", genymotion_path)
asyncio.run(manager.manage_emulator())