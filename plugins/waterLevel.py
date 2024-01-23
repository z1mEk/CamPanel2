'''
pip install EasyMCP2221
permissions: https://github.com/electronicayciencia/EasyMCP2221/issues/5
'''
import nest_asyncio
from nest_asyncio import asyncio
nest_asyncio.apply()
import EasyMCP2221
from datetime import datetime
from general.logger import logging

class data:
    whiteWaterLevel = 0
    greyWaterLevel = 0
    lastUpdate = datetime.now()

class helper:
    @classmethod
    def map_value(cls, value, in_min, in_max, out_min, out_max):
        return int((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

class plugin:
    
    mcp = None

    @classmethod
    def reconnect(cls):
        try:
            cls.mcp = EasyMCP2221.Device()
        except Exception as e:
            logging.error(f"MCP2221_connect: {e}") 

    @classmethod
    async def readData(cls, interval):
        while True:
            try:
                if cls.mcp == None:
                    cls.reconnect()
                cls.mcp.set_pin_function(gp1='ADC', gp2="ADC")
                cls.mcp.ADC_config(ref="VDD")                
                values = cls.mcp.ADC_read()
                logging.info(f"values={values}")
                data.whiteWaterLevel = helper.map_value(158, 0, 190, 0, 100)
                data.greyWaterLevel = helper.map_value(15, 0, 190, 0, 100)
                data.lastUpdate = datetime.now()
            except Exception as e:
                logging.error(f"MCP2221_get: {e}")
                data.whiteWaterLevel = 0
                data.greyWaterLevel = 0

            await asyncio.sleep(interval)       

    @classmethod
    async def initialize(cls, event_loop):
        event_loop.create_task(cls.readData(5))
