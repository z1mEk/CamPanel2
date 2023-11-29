from hmi import hmi

async def wakeUp():
    await hmi.client.wakeup()

async def sleep():
    await hmi.client.sleep()
    
async def reset():
    await command('rest')

async def command(command):
    await hmi.client.command(command)

async def reconnect():
    await hmi.client.reconnect()

async def dimmer(value:int, save:bool = False):
    await command('dim{}={}'.format('s' if save else '', value))

async def setTimeToSleep(value:int):
    await command('thsp={}'.format(value))

async def setWakeUpSerial(value:bool = False):
    await command('thup={}'.format(0 if value else 1))

async def isSleeping() -> bool:
    return await hmi.client.is_sleeping()

async def getProperty(component:str, property:str):
    return await hmi.client.get(f"{component}.{property}")

async def setProperty(component:str, property:str, val):
    await hmi.client.set(f"{component}.{property}", val)

async def getPageId(page_name:str):
    return await hmi.client.get_page_id(page_name)

async def getComponentId(page_name:str, component_name:str):
    return await hmi.client.get_component_id(page_name, component_name)

async def show(page_id:int):
    await command(f"page {page_id}")