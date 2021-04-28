from hmi import hmi
from hmi.pages import page0, page1
from hmi import screen

async def onRun():
    print("run")
    await hmi.Create()  

async def onEvery1Second():
    return

async def onEvery5Seconds():
    return

async def onEvery15Seconds():
    print("connected")
    return

async def onEvery30Seconds():
    return

async def onEvery60Seconds():
    return  

async def onEvery300Seconds():
    return 