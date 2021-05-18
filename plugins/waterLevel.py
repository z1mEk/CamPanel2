import random
import asyncio

class data:
    whiteWaterLevel = 0
    tempWhiteWater = 0
    greyWaterLevel = 0
    tempGreyWater = 0

class plugin:

    @classmethod
    async def readData(self, interval):
        while True:
            data.whiteWaterLevel = random.randint(0, 100)
            data.greyWaterLevel = random.randint(0, 100)
            await asyncio.sleep(interval)       

    @classmethod
    def initialize(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.readData(1))
        loop.run_forever
