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

async def isSleeping():
    return await hmi.client.is_sleeping()