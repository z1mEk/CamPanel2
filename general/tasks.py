import asyncio
from general import events

async def periodic_001s():
    while True:
        await events.onEvery1Second()
        await asyncio.sleep(1)    
       