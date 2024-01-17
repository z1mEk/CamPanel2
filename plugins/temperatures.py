'''
sudo pip install w1thermsensor
https://github.com/timofurrer/w1thermsensor
https://bigl.es/ds18b20-temperature-sensor-with-python-raspberry-pi/
'''
import nest_asyncio
nest_asyncio.apply()
import random
from general.logger import logging

class data:
    inTemp = 0
    outTemp = 0

class plugin:

    @classmethod
    async def readData(cls, interval):
        while True:

            await nest_asyncio.asyncio.sleep(interval)  

    @classmethod
    async def initialize(cls, event_loop):
        event_loop.create_task(cls.readData(1))  
