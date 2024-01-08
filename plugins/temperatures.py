'''
sudo pip install w1thermsensor
https://github.com/timofurrer/w1thermsensor
https://bigl.es/ds18b20-temperature-sensor-with-python-raspberry-pi/
'''
import nest_asyncio
nest_asyncio.apply()
import random

class data:
    temp1 = 0
    temp2 = 0

class plugin:

    @classmethod
    async def readData(cls, interval):
        while True:
            data.temp1 = random.randint(-30, 30)
            data.temp2 = random.randint(-30, 30)
            await nest_asyncio.asyncio.sleep(interval)  

    @classmethod
    async def initialize(cls, event_loop):
        event_loop.create_task(cls.readData(1))  
