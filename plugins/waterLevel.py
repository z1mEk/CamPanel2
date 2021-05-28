import random
import asyncio

class data:
    whiteWaterLevel = 0
    tempWhiteWater = 0
    greyWaterLevel = 0
    tempGreyWater = 0

class plugin:

    @classmethod
    async def readData(cls, interval):
        while True:
            data.whiteWaterLevel = random.randint(0, 100)
            data.greyWaterLevel = random.randint(0, 100)
            await asyncio.sleep(interval)       

    @classmethod
    def initialize(cls, event_loop):
        event_loop.create_task(cls.readData(1))
