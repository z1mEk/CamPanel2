from hmi import hmi

async def onRun():
    await hmi.create() 

async def onEvery1Second():
    return
 