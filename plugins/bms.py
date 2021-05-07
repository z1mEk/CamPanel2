import random
import asyncio

class data:
    current = 0
    totalVoltage = 0
    remainingCapacity = 0
    temperature = 0
    RSOC = 0

class plugin:
    name = 'Daly BMS'

    @classmethod
    async def readData(self, interval):
        while True:
            data.current = random.randint(0, 50000)
            data.totalVoltage = random.randint(12000, 15000)
            data.remainingCapacity = random.randint(0, 120000)
            data.temperature = random.randint(10, 30)
            data.RSOC = random.randint(0, 100)
            await asyncio.sleep(interval)
       

    @classmethod
    def initialize(self):
        loop = asyncio.get_event_loop()      
        loop.create_task(self.readData(10))
        loop.run_forever
