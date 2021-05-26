import random
import asyncio

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
            data.currentMiliAmper = random.randint(0, 50000)
            data.currentAmper = data.currentMiliAmper / 1000
            data.totalMiliVoltage = random.randint(12000, 15000)
            data.totalVoltage = data.totalMiliVoltage / 1000
            data.remainingCapacity = random.randint(0, 120000)
            data.temperature = random.randint(10, 30)
            data.RSOC = random.randint(0, 100)
            await asyncio.sleep(interval)       

    @classmethod
    def initialize(cls):
        loop = asyncio.get_event_loop()      
        loop.create_task(cls.readData(1))
