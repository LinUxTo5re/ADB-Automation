from updatedMineWcoinProgramitically import UpdatedMineWcoinProgram
from startMMMFarming import StartMMMFarming
import asyncio
import os
from startBLUMFarming import StartBLUMFarming
from startTronKeeper import StartTronKeeper

class StartMiningMemeCoinsOnTelegram:
    def __init__(self):
        self.device_id = "emulator-5554"
        
    async def start_all(self):
        os.system('cls')
        # Run mining tasks concurrently
        await asyncio.gather(
            self.start_tron_coin(),
            self.start_blum_coin(),
            self.start_mmm_coin(),
            self.start_w_coin()
        )

    async def start_w_coin(self):
        wcoin = UpdatedMineWcoinProgram(self.device_id)
        await wcoin.start_Wcoin()

    async def start_mmm_coin(self):
        mmmcoin = StartMMMFarming(self.device_id)
        await mmmcoin.start_MMM()
    
    async def start_blum_coin(self):
        blumcoin = StartBLUMFarming(self.device_id)
        await blumcoin.start_blum()
    
    async def start_tron_coin(self):
        troncoin = StartTronKeeper(self.device_id)
        await troncoin.start_tron()

if __name__ == "__main__":
    telegram_mine = StartMiningMemeCoinsOnTelegram()
    asyncio.run(telegram_mine.start_all())

"""
Order of starting bot:
1) blum
2) mmm
3) w coin
"""
