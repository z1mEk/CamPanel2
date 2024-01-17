import nest_asyncio
nest_asyncio.apply()
from general.logger import logging

class data:
    val1 = None
    val2 = None
    
class plugin:

    @classmethod
    async def readData(cls, interval):
        while True:
            data.val1 = 0
            data.val2 = 0
            await nest_asyncio.asyncio.sleep(interval)       

    @classmethod
    async def initialize(cls, event_loop):
        event_loop.create_task(cls.readData(1))
