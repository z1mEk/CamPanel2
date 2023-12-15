from hmi import hmi

async def wakeUp():
    try:
        await hmi.client.wakeup()
    except Exception as e:
        print(f"Wystąpił problem z połączeniem z ekranem Nextion: {e}")

async def sleep():
    try:
        await hmi.client.sleep()
    except Exception as e:
        print(f"Wystąpił problem z połączeniem z ekranem Nextion: {e}")
    
async def reset():
    await command('rest')

async def command(command):
    try:
        await hmi.client.command(command)
    except Exception as e:
        print(f"Wystąpił problem z połączeniem z ekranem Nextion: {e}")

async def reconnect():
    try:
        await hmi.client.reconnect()
    except Exception as e:
        print(f"Wystąpił problem z połączeniem z ekranem Nextion: {e}")

async def dimmer(value:int, save:bool = False):
    await command('dim{}={}'.format('s' if save else '', value))

async def setTimeToSleep(value:int):
    await command('thsp={}'.format(value))

async def setWakeUpSerial(value:bool = False):
    await command('thup={}'.format(0 if value else 1))

async def isSleeping() -> bool:
    try:
        return await hmi.client.is_sleeping()
    except Exception as e:
        print(f"Wystąpił problem z połączeniem z ekranem Nextion: {e}")

async def getProperty(component:str, property:str):
    try:
        return await hmi.client.get(f"{component}.{property}")
    except Exception as e:
        print(f"Wystąpił problem z połączeniem z ekranem Nextion: {e}")

async def setProperty(component:str, property:str, val):
    try:
        await hmi.client.set(f"{component}.{property}", val)
    except Exception as e:
        print(f"Wystąpił problem z połączeniem z ekranem Nextion: {e}")

async def show(page_id:int):
    await command(f"page {page_id}")