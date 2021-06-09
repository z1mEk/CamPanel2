'''
https://pypi.org/project/nextion/
pip3 install nextion
'''
import asyncio
from config import config
from nextion import Nextion, EventType#, client
from hmi import methods, events, triggers
 
def callbackExecute(data):
    func = next((item for item in triggers.components_touch_event \
        if (item["page_id"], item["component_id"], item["touch_event"]) \
            == (data.page_id, data.component_id, data.touch_event)), None)
    asyncio.ensure_future(func["call_back"]())

def eventHandler(type_, data):
    if type_ == EventType.TOUCH:
        callbackExecute(data)
    elif type_ == EventType.TOUCH_COORDINATE:
        asyncio.ensure_future(events.onTouchCoordinate(data))
    elif type_ == EventType.TOUCH_IN_SLEEP:
        asyncio.ensure_future(events.onTouchInSleep(data))
    elif type_ == EventType.AUTO_SLEEP:
        asyncio.ensure_future(events.onAutoSleep())
    elif type_ == EventType.AUTO_WAKE:
        asyncio.ensure_future(events.onAutoWake())         
    elif type_ == EventType.STARTUP:
        asyncio.ensure_future(events.onStartUp())

async def startupCommands():
    await methods.wakeUp()
    for comm in config.data.nextion.startup_commands:
        await methods.command(comm)

async def create(event_loop):
    global client
    client = Nextion(config.data.nextion.com, config.data.nextion.baudrate, eventHandler, event_loop)
    await client.connect()
    await startupCommands()