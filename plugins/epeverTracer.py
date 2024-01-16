import random
import nest_asyncio
nest_asyncio.apply()
from general.logger import logging

class pv:
    status = ""
    voltage = 35
    current = 6
    power = 280

class battery:
    status = ""
    voltage = 0
    current = 0
    temp = 0
    soc = 0

class load:
    status = ""
    voltage = 0
    current = 0

class data:
    pv = pv
    battery = battery
    load = load
    
class plugin:

    @classmethod
    async def readData(cls, interval):
        while True:

            await nest_asyncio.asyncio.sleep(interval)       

    @classmethod
    async def initialize(cls, event_loop):
        event_loop.create_task(cls.readData(5))