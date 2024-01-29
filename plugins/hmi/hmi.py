'''
https://pypi.org/project/nextion/
pip install nextion
'''
import nest_asyncio
from nest_asyncio import asyncio
nest_asyncio.apply()
from general.configLoader import config
from general.deviceManager import device
from nextion import Nextion, EventType, client
from plugins.hmi import methods as hmiMethods, events as hmiEvents, triggers
from general.logger import logging

# async def updateNextion():
#     await client.upload_firmware()
 
def callbackExecute(data):
    func = next((item for item in triggers.components_touch_event \
        if (item["page_id"], item["component_id"], item["touch_event"]) \
            == (data.page_id, data.component_id, data.touch_event)), None)
    asyncio.create_task(func["call_back"]())

def eventHandler(type_, data):
    if type_ == EventType.TOUCH:
        callbackExecute(data)
    elif type_ == EventType.TOUCH_COORDINATE:
        asyncio.create_task(hmiEvents.onTouchCoordinate(data))
    elif type_ == EventType.TOUCH_IN_SLEEP:
        asyncio.create_task(hmiEvents.onTouchInSleep(data))
    elif type_ == EventType.AUTO_SLEEP:
        asyncio.create_task(hmiEvents.onAutoSleep())
    elif type_ == EventType.AUTO_WAKE:
        asyncio.create_task(hmiEvents.onAutoWake())         
    elif type_ == EventType.STARTUP:
        asyncio.create_task(hmiEvents.onStartUp())
    elif type_ == EventType.SD_CARD_UPGRADE:
        asyncio.create_task(hmiEvents.onSdCardUpgrade())

async def startupCommands():
    logging.debug(f"hmi.startupCommands()")
    await hmiMethods.wakeUp()
    for comm in config.nextion.startup_commands:
        await hmiMethods.command(comm)
        logging.debug(f"command({comm})")

async def create(event_loop):
    global client
    try:
        nextion_device = device.FindUsbDevice(config.nextion.device)
        logging.info(f"Create Nextion client")
        client = Nextion(nextion_device, config.nextion.baudrate, eventHandler, event_loop, reconnect_attempts=5)
        await client.connect()
        logging.info(f"Nextion device connected: {nextion_device}, {config.nextion.baudrate}")
        await startupCommands()
    except Exception as e:
        logging.error(f"Nextion: {e}")