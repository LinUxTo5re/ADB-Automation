from updatedMineWcoinProgramitically import UpdatedMineWcoinProgramAsync
from startMMMFarming import StartMMMFarming
import asyncio
import os
from startBLUMFarming import StartBLUMFarming

class StartMiningMemeCoinsOnTelegram:
    def __init__(self):
        self.device_id = "127.0.0.1:6555"
        self.emulator_name = "CloneTMP - Samsung Galaxy S23" 
        
    async def start_all(self):
        os.system('clear')
        # Run mining tasks concurrently
        await asyncio.gather(
            self.start_w_coin(),
            self.start_mmm_coin(),
            self.start_blum_coin()
        )

    async def start_w_coin(self):
        wcoin = UpdatedMineWcoinProgramAsync(self.device_id, self.emulator_name)
        await asyncio.sleep(120) # giving room to MR.MEME for starting
        await wcoin.start_Wcoin()

    async def start_mmm_coin(self):
        mmmcoin = StartMMMFarming(self.device_id)
        await asyncio.sleep(45) # giving room to blum for starting
        await mmmcoin.start_MMM()
    
    async def start_blum_coin(self):
        blumcoin = StartBLUMFarming(self.device_id)
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
