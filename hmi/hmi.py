import asyncio
from config import config
from nextion import Nextion, EventType
from hmi import screen

### definition of call name for nextion's components. "call_name" procedure must by exists in hmi.events ###
components_touch_event = [
        #page0
        {"page_id": 0, "component_id": 9, "touch_event": 1, "call_name": "page0_b0_touch"},
        {"page_id": 0, "component_id": 5, "touch_event": 1, "call_name": "page0_t4_touch"},
        {"page_id": 0, "component_id": 6, "touch_event": 1, "call_name": "page0_t5_touch"},

        #page1
        {"page_id": 1, "component_id": 1, "touch_event": 1, "call_name": "page1_b0_touch"},
        {"page_id": 1, "component_id": 2, "touch_event": 0, "call_name": "page1_bt0_release"},
        {"page_id": 1, "component_id": 3, "touch_event": 0, "call_name": "page1_bt1_release"},
        {"page_id": 1, "component_id": 4, "touch_event": 0, "call_name": "page1_bt2_release"},
        {"page_id": 1, "component_id": 5, "touch_event": 0, "call_name": "page1_bt3_release"},
        {"page_id": 1, "component_id": 6, "touch_event": 0, "call_name": "page1_bt4_release"},
        {"page_id": 1, "component_id": 7, "touch_event": 0, "call_name": "page1_bt5_release"}
    ]

def CallProcName(data):
    comp = next((item for item in components_touch_event \
        if (item["page_id"], item["component_id"], item["touch_event"]) \
            == (data.page_id, data.component_id, data.touch_event)), None)
    
    if comp and (comp["call_name"] in dir(screen)):
        asyncio.ensure_future(getattr(screen, comp["call_name"])())

def eventHandler(type_, data):
    if type_ == EventType.TOUCH:
        CallProcName(data)
    elif type_ == EventType.TOUCH_COORDINATE:
        asyncio.ensure_future(screen.touch_coordinate(data))
    elif type_ == EventType.TOUCH_IN_SLEEP:
        asyncio.ensure_future(screen.touch_in_sleep(data))
    elif type_ == EventType.AUTO_SLEEP:
        asyncio.ensure_future(screen.auto_sleep())
    elif type_ == EventType.AUTO_WAKE:
        asyncio.ensure_future(screen.auto_wake())         
    elif type_ == EventType.STARTUP:
        asyncio.ensure_future(screen.startup())

async def startupCommands():
    for x in config.data.nextion.startup_commands:
        await client.command(x)

async def Create():
    global client
    client = Nextion(config.data.nextion.com, config.data.nextion.baudrate, eventHandler)
    await client.connect()
    await startupCommands()