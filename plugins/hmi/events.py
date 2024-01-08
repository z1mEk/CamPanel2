async def onStartUp():
    print("startup")

async def onAutoSleep():
    print("auto sleep")

async def onAutoWake():
    print("auto wake")

async def onSdCardUpgrade():
    print("sd card upgrade")
    
async def onTouchInSleep(data):
    print(data)

async def onTouchCoordinate(data):
    print(data)