import random
import nest_asyncio
nest_asyncio.apply()

class data:
    currentMiliAmper = 0
    currentAmper = 0
    totalMiliVoltage = 0
    totalVoltage = 0
    remainingCapacity = 0
    temperature = 0
    RSOC = 0

class plugin:

    @classmethod
    async def readData(cls, interval):
        while True:
            data.currentMiliAmper = random.randint(-50000, 50000)
            data.currentAmper = data.currentMiliAmper / 1000
            data.totalMiliVoltage = random.randint(12000, 15000)
            data.totalVoltage = data.totalMiliVoltage / 1000
            data.remainingCapacity = random.randint(0, 120000)
            data.temperature = random.randint(10, 30)
            data.RSOC = random.randint(0, 100)
            await nest_asyncio.asyncio.sleep(interval)       

    @classmethod
    def initialize(cls, event_loop):     
        event_loop.create_task(cls.readData(1))
