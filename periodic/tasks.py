import asyncio
from events import events

async def run():
    await events.onRun()

async def periodic_001s():
    while True:
        await events.onEvery1Second()
        await asyncio.sleep(1)    

async def periodic_005s():
    while True:
        await events.onEvery5Seconds()
        await asyncio.sleep(5) 

async def periodic_015s():
    while True:
        await events.onEvery15Seconds()
        await asyncio.sleep(15)

async def periodic_030s():
    while True:
        await events.onEvery30Seconds()
        await asyncio.sleep(30)

async def periodic_060s():
    while True:
        await events.onEvery60Seconds()
        await asyncio.sleep(60)        

async def periodic_300s():
    while True:
        await events.onEvery300Seconds()
        await asyncio.sleep(300)        