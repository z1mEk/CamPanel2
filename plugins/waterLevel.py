'''
pip install EasyMCP2221
'''
import nest_asyncio
import EasyMCP2221
nest_asyncio.apply()
from datetime import datetime

class data:
    mcp = None
    whiteWaterLevel = -1
    greyWaterLevel = -1
    whiteWaterLevelDisplay = ""
    greyWaterLevelDisplay = ""
    lastUpdate = None

class helper:
    @classmethod
    def map_value(value, in_min, in_max, out_min, out_max):
        return int((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

class plugin:

    @classmethod
    def reconnect(cls):
        try:
            data.mcp = EasyMCP2221.Device()
        except Exception as e:
            print(f"Wystąpił problem z modułem MCP2221: {e}") 

    @classmethod
    async def readData(cls, interval):
        while True:
            # if data.mcp == None:
            #     cls.reconnect()
            # data.mcp.set_pin_function(gp1='ADC', gp2="ADC")
            # data.mcp.ADC_config(ref="VDD")                
            # values = data.mcp.ADC_read()
            data.whiteWaterLevel = 88 #helper.map_value(158, 0, 190, 0, 100)
            data.greyWaterLevel = 12 #helper.map_value(15, 0, 190, 0, 100)
            data.whiteWaterLevelDisplay = '{}%'.format(data.whiteWaterLevel)
            data.greyWaterLevelDisplay = '{}%'.format(data.greyWaterLevel)
            data.lastUpdate = datetime.now()
            await nest_asyncio.asyncio.sleep(interval)       

    @classmethod
    async def initialize(cls, event_loop):
        event_loop.create_task(cls.readData(5))
