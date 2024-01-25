from plugins.hmi import hmi
from general.logger import logging
import nest_asyncio
from nest_asyncio import asyncio
nest_asyncio.apply()

async def command(command):
    try:
        logging.debug(f"methods.command({command})")
        return await hmi.client.command(command)
    except Exception as e:
        logging.error(f"Nextion: {e}")

async def wakeUp():
    try:
        logging.debug(f"methods.wakeUp()")
        await hmi.client.wakeup()
    except Exception as e:
        logging.error(f"Nextion: {e}")

async def sleep():
    try:
        logging.debug(f"methods.sleep()")
        await hmi.client.sleep()
    except Exception as e:
        logging.error(f"Nextion: {e}")
    
async def reset():
    await command('rest')

async def reconnect():
    try:
        logging.debug(f"methods.reconnect()")
        await hmi.client.reconnect()
    except Exception as e:
        logging.error(f"Nextion: {e}")

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
    try:
        ret = await hmi.client.is_sleeping() 
        logging.debug(f"methods.isSleeping() -> {ret}")
        return ret
    except Exception as e:
        logging.error(f"Nextion: {e}")

async def getProperty(component:str, property:str):
    try:
        ret = await hmi.client.get(f"{component}.{property}")
        logging.debug(f"methods.getProperty({component}, {property}) -> {ret}")
        return ret
    except Exception as e:
        logging.error(f"Nextion: {e}")

async def setProperty(component:str, property:str, val):
    try:
        logging.debug(f"methods.setProperty({component}, {property}, {val})")
        await hmi.client.set(f"{component}.{property}", val)
    except Exception as e:
        logging.error(f"Nextion: {e}")

async def showPageId(page_id:int):
    logging.debug(f"methods.show({page_id})")
    await command(f"page {page_id}")

async def showPageName(page_name:str):
    logging.debug(f"methods.show({page_name})")
    await command(f"page {page_name}")    

async def getCurrentPageId() -> int:
    logging.debug(f"methods.sendme()")
    try:
        ret = await command(f"sendme")
    except Exception as e:
        logging.error(f"sendme:{e}")
        ret -1
    return ret
