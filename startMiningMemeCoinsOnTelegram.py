from updatedMineWcoinProgramitically import UpdatedMineWcoinProgramAsync
from startMMMFarming import StartMMMFarming
import asyncio
import os
from startBLUMFarming import StartBLUMFarming
from handleEmulator import GenymotionManager

class StartMiningMemeCoinsOnTelegram:
    def __init__(self):
        self.device_id = "127.0.0.1:6555"
        self.emulator_name = "CloneTMP - Samsung Galaxy S23" 
        self.home_dir = os.path.expanduser("~")
        self.genymotion_path = os.path.join(self.home_dir, "genymotion")
        

    async def start_all(self):
        os.system('clear')
        # Run both mining tasks concurrently
        await asyncio.gather(
            self.start_w_coin(),
            self.start_mmm_coin(),
            self.start_blum_coin()
        )

    # async def start_genymotion_emulator(self):
    #     manager = GenymotionManager(self.emulator_name, self.genymotion_path)
    #     await manager.manage_emulator()

    async def start_w_coin(self):
        wcoin = UpdatedMineWcoinProgramAsync(self.device_id, self.emulator_name, self.genymotion_path)
        await asyncio.sleep(90) # giving room to MR.MEME for starting
        await wcoin.start_Wcoin()

    async def start_mmm_coin(self):
        mmmcoin = StartMMMFarming(self.device_id)
        await asyncio.sleep(45) # giving room to blum for starting
        await mmmcoin.start_MMM()
    
    async def start_blum_coin(self):
        blumcoin = StartBLUMFarming(self.device_id)
        await asyncio.sleep(60) # giving room to android emulator starting
        await blumcoin.start_blum()

if __name__ == "__main__":
    telegram_mine = StartMiningMemeCoinsOnTelegram()
    asyncio.run(telegram_mine.start_all())

"""
Order of starting bot:
1) blum
2) mmm
3) w coin
"""
