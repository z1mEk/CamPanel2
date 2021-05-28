from hmi import hmi

async def onRun(event_loop):
    await hmi.create(event_loop)

 