import asyncio
import random

class data:
    class pv:
        voltage = 0
        current = 0
        power = 0
        status = 0

    class battery:
        voltage = 0
        current = 0
        temperature = 0
        status = 0
        chargingStatus = 0

    class load:
        voltage = 0
        current = 0
        power = 0
        status = 0

class plugin:

    @classmethod
    async def readData(cls, interval):
        while True:
            data.pv.voltage = random.randint(12, 40)
            data.pv.current = random.randint(0, 20)
            await asyncio.sleep(interval)  

    @classmethod
    def initialize(cls):
        loop = asyncio.get_event_loop()    
        loop.create_task(cls.readData(1))  
