from updatedMineWcoinProgramitically import UpdatedMineWcoinProgram
from startMMMFarming import StartMMMFarming
import asyncio
import os
from startBLUMFarming import StartBLUMFarming
from startTronKeeper import StartTronKeeper
from startSeedFarming import StartSeedFarming
from startTimeFarm import StartTimeFarmFarming
from startFrogFarm import StartFrogFarmFarming
from startHeadCoin import StartHeadCoin

class StartMiningMemeCoinsOnTelegram:
    def __init__(self):
        self.device_id = "127.0.0.1:6555"
        
    async def start_all(self):
        os.system('clear')
        # Run mining tasks concurrently
        await asyncio.gather(
            self.start_head_coin(),
            self.start_seed_coin(),
            self.start_time_coin(),
            self.start_tron_coin(),
            self.start_frog_coin(),
            self.start_blum_coin(),
            self.start_mmm_coin(),
            self.start_w_coin()
        )

    async def start_w_coin(self):
        wcoin = UpdatedMineWcoinProgram(self.device_id)
        await wcoin.start_Wcoin()

    async def start_mmm_coin(self):
        mmmcoin = StartMMMFarming(self.device_id)
        await mmmcoin.start_MMM() # 30 min await in main()
    
    async def start_blum_coin(self):
        blumcoin = StartBLUMFarming(self.device_id)
        await blumcoin.start_blum()  # 45 min await in main()

    async def start_frog_coin(self):
        frogcoin = StartFrogFarmFarming(self.device_id)
        await frogcoin.start_FrogFarm()  # 45 min await in main()
    
    async def start_tron_coin(self):
        troncoin = StartTronKeeper(self.device_id)
        await troncoin.start_Tron()  # 60 min await in main()
    
    async def start_time_coin(self):
        secondcoin = StartTimeFarmFarming(self.device_id)
        await secondcoin.start_TimeFarm()  # 60 min await in main()

    async def start_seed_coin(self):
        seedcoin = StartSeedFarming(self.device_id)
        await seedcoin.start_Seed()  # 90 min await in main()

    async def start_head_coin(self):
        headcoin = StartHeadCoin(self.device_id)
        await headcoin.start_Head()  # 120 min await in main()

if __name__ == "__main__":
    telegram_mine = StartMiningMemeCoinsOnTelegram()
    asyncio.run(telegram_mine.start_all())

"""
Order of starting bot:
1) blum
2) mmm
3) w coin
"""
