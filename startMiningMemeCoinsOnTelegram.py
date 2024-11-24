from updatedMineWcoinProgramitically import UpdatedMineWcoinProgramAsync
from startMMMFarming import StartMMMFarming
import asyncio
import os

class StartMiningMemeCoinsOnTelegram:
    def __init__(self):
        self.device_id = "127.0.0.1:6555"

    async def start_all(self):
        os.system('clear')
        # Run both mining tasks concurrently
        await asyncio.gather(
            self.start_w_coin(),
            self.start_mmm_coin()
        )

    async def start_w_coin(self):
        wcoin = UpdatedMineWcoinProgramAsync(self.device_id)
        await asyncio.sleep(60) # giving room to MR.MEME for starting
        await wcoin.start_Wcoin()

    async def start_mmm_coin(self):
        mmmcoin = StartMMMFarming(self.device_id)
        await mmmcoin.start_MMM()

if __name__ == "__main__":
    telegram_mine = StartMiningMemeCoinsOnTelegram()
    asyncio.run(telegram_mine.start_all())
