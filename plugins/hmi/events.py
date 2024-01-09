from general.logger import logging

async def onStartUp():
    logging.debug("events.onStartUp()")

async def onAutoSleep():
    logging.debug("events.onAutoSleep()")

async def onAutoWake():
    logging.debug("events.onAutoWake()")

async def onSdCardUpgrade():
    logging.debug("events.onSdCardUpgrade()")
    
async def onTouchInSleep(data):
    logging.debug(f"events.onTouchInSleep({data})")

async def onTouchCoordinate(data):
    logging.debug(f"events.onTouchCoordinate({data})")