from plugins.hmi import hmi
from general.logger import logging
import nest_asyncio
nest_asyncio.apply()
from general.queueManager import QueueManager

async def command(command):
    async def commandQueue():
        try:
            logging.debug(f"methods.command({command})")
            return await hmi.client.command(command)
        except Exception as e:
            logging.error(f"Nextion: {e}")
    return QueueManager.enqueue(commandQueue)

async def wakeUp():
    async def wakeUpQueue():
        try:
            logging.debug(f"methods.wakeUp()")
            await hmi.client.wakeup()
        except Exception as e:
            logging.error(f"Nextion: {e}")
    QueueManager.enqueue(wakeUpQueue)

async def sleep():
    async def sleepQueue():
        try:
            logging.debug(f"methods.sleep()")
            await hmi.client.sleep()
        except Exception as e:
            logging.error(f"Nextion: {e}")
    QueueManager.enqueue(sleepQueue)
    
async def reset():
    await command('rest')

async def reconnect():
    async def reconnectQueue():
        try:
            logging.debug(f"methods.reconnect()")
            await hmi.client.reconnect()
        except Exception as e:
            logging.error(f"Nextion: {e}")
    QueueManager.enqueue(reconnectQueue)

async def dimmer(value:int, save:bool = False):
    logging.debug(f"methods.dimmer({value}, {save})")
    await command('dim{}={}'.format('s' if save else '', value))

async def setTimeToSleep(value:int):
    logging.debug(f"methods.setTimeToSleep({value})")
    await command('thsp={}'.format(value))

async def setWakeUpSerial(value:bool = False):
    logging.debug(f"methods.setWakeUpSerial({value})")
    await command('thup={}'.format(0 if value else 1))

async def isSleeping() -> bool:
    async def isSleepingQueue():
        try:
            ret = await hmi.client.is_sleeping() 
            logging.debug(f"methods.isSleeping() -> {ret}")
            return ret
        except Exception as e:
            logging.error(f"Nextion: {e}")
    return QueueManager.enqueue(isSleepingQueue)

async def getProperty(component:str, property:str):
    async def getPropertyQueue():
        try:
            ret = await hmi.client.get(f"{component}.{property}")
            logging.info(f"methods.getProperty({component}, {property}) -> {ret}")
            return ret
        except Exception as e:
            logging.error(f"Nextion: {e}")
    return QueueManager.enqueue(getPropertyQueue)

async def setProperty(component:str, property:str, val):
    async def setPropertyQueue():
        try:
            logging.info(f"methods.setProperty({component}, {property}, {val})")
            await hmi.client.set(f"{component}.{property}", val)
        except Exception as e:
            logging.error(f"Nextion: {e}")
    QueueManager.enqueue(setPropertyQueue)

async def show(page_id:int):
    logging.debug(f"methods.show({page_id})")
    await command(f"page {page_id}")

async def sendme() -> int:
    logging.debug(f"methods.sendme()")
    return await command(f"sendme")