'''
https://pypi.org/project/nextion/
pip3 install nextion
'''
import asyncio
from general import config_loader
from nextion import Nextion, EventType, client
from hmi import methods as hmiMethods, events as hmiEvents, triggers
 
def callbackExecute(data):
    print("callbackExecute()")
    func = next((item for item in triggers.components_touch_event \
        if (item["page_id"], item["component_id"], item["touch_event"]) \
            == (data.page_id, data.component_id, data.touch_event)), None)
    asyncio.ensure_future(func["call_back"]())

def eventHandler(type_, data):
    print("eventHandler()")
    if type_ == EventType.TOUCH:
        callbackExecute(data)
    elif type_ == EventType.TOUCH_COORDINATE:
        asyncio.ensure_future(hmiEvents.onTouchCoordinate(data))
    elif type_ == EventType.TOUCH_IN_SLEEP:
        asyncio.ensure_future(hmiEvents.onTouchInSleep(data))
    elif type_ == EventType.AUTO_SLEEP:
        asyncio.ensure_future(hmiEvents.onAutoSleep())
    elif type_ == EventType.AUTO_WAKE:
        asyncio.ensure_future(hmiEvents.onAutoWake())         
    elif type_ == EventType.STARTUP:
        asyncio.ensure_future(hmiEvents.onStartUp())

async def startupCommands():
    print("Startup commands")
    await hmiMethods.wakeUp()
    for comm in config_loader.data.nextion.startup_commands:
        print(comm)
        await hmiMethods.command(comm)

async def create(event_loop):
    global client
    print(f"Nextion create()")
    print(f"Nextion port: {config_loader.data.nextion.com}")
    print(f"Nextion baudrate: {config_loader.data.nextion.baudrate}")

    try:
        client = Nextion(config_loader.data.nextion.com, config_loader.data.nextion.baudrate, eventHandler, event_loop, reconnect_attempts=5, encoding="utf-8")
        await client.connect()
        await startupCommands()
    except Exception as e:
        print(f"Wystąpił problem z połączeniem z ekranem Nextion: {e}")