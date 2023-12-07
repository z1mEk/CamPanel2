'''
https://pypi.org/project/nextion/
pip3 install nextion
'''
import nest_asyncio
nest_asyncio.apply()
from general.config_loader import config
from nextion import Nextion, EventType, client
from hmi import methods as hmiMethods, events as hmiEvents, triggers
 
def callbackExecute(data):
    func = next((item for item in triggers.components_touch_event \
        if (item["page_id"], item["component_id"], item["touch_event"]) \
            == (data.page_id, data.component_id, data.touch_event)), None)
    nest_asyncio.asyncio.ensure_future(func["call_back"]())

def eventHandler(type_, data):
    if type_ == EventType.TOUCH:
        callbackExecute(data)
    elif type_ == EventType.TOUCH_COORDINATE:
        nest_asyncio.asyncio.ensure_future(hmiEvents.onTouchCoordinate(data))
    elif type_ == EventType.TOUCH_IN_SLEEP:
        nest_asyncio.asyncio.ensure_future(hmiEvents.onTouchInSleep(data))
    elif type_ == EventType.AUTO_SLEEP:
        nest_asyncio.asyncio.ensure_future(hmiEvents.onAutoSleep())
    elif type_ == EventType.AUTO_WAKE:
        nest_asyncio.asyncio.ensure_future(hmiEvents.onAutoWake())         
    elif type_ == EventType.STARTUP:
        nest_asyncio.asyncio.ensure_future(hmiEvents.onStartUp())

async def startupCommands():
    print("Startup commands")
    await hmiMethods.wakeUp()
    for comm in config.nextion.startup_commands:
        print(comm)
        await hmiMethods.command(comm)

async def create(event_loop):
    global client
    print(f"Nextion create()")
    print(f"Nextion port: {config.nextion.com}")
    print(f"Nextion baudrate: {config.nextion.baudrate}")

    try:
        client = Nextion(config.nextion.com, config.nextion.baudrate, eventHandler, event_loop, reconnect_attempts=5, encoding="utf-8")
        await client.connect()
        await startupCommands()
    except Exception as e:
        print(f"Wystąpił problem z połączeniem z ekranem Nextion: {e}")