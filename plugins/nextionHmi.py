import nest_asyncio
nest_asyncio.apply()
from plugins.hmi import hmi
    
class plugin:

    @classmethod
    async def initialize(cls, event_loop):
        event_loop.create_task(hmi.create(event_loop))