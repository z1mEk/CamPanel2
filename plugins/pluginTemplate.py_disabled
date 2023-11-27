import random
import asyncio

class data:
    val1 = None
    val2 = None
    
class plugin:

    @classmethod
    async def readData(cls, interval):
        while True:

            await asyncio.sleep(interval)       

    @classmethod
    def initialize(cls, event_loop):
        event_loop.create_task(cls.readData(1))
