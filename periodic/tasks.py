import asyncio
from periodic.methods import on15Seconds, on1Second, on300Seconds, on30Seconds, on5Seconds, on60Seconds, onRun

async def run():
    await onRun()

async def periodic_001s():
    while True:
        await on1Second()
        await asyncio.sleep(1)    

async def periodic_005s():
    while True:
        await on5Seconds()
        await asyncio.sleep(5) 

async def periodic_015s():
    while True:
        await on15Seconds()
        await asyncio.sleep(15)

async def periodic_030s():
    while True:
        await on30Seconds()
        await asyncio.sleep(30)

async def periodic_060s():
    while True:
        await on60Seconds()
        await asyncio.sleep(60)        

async def periodic_300s():
    while True:
        await on300Seconds()
        await asyncio.sleep(300)        