from hmi import methods

async def onStartUp():
    print("startup")

async def onAutoSleep():
    print("auto sleep")

async def onAutoWake():
    print("auto wake")
    
async def onTouchInSleep(data):
    print(data)

async def onTouchCoordinate(data):
    print(data)