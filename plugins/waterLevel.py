'''
pip3 install EasyMCP2221
'''
import nest_asyncio
from MCP2221 import MCP2221
nest_asyncio.apply()
import random

class data:
    mcp = None
    whiteWaterLevel = 56
    greyWaterLevel = 23

class plugin:

    @classmethod
    async def readData(cls, interval):
        try:
            #04D8:00DD
            data.mcp = MCP2221.MCP2221(1240, 221, 0)
            print(f"data.mcp: {data.mcp}")
            # data.mcp.set_pin_function(gp1='ADC', gp2="ADC")
            # data.mcp.ADC_config(ref="VDD")
        except Exception as e:
            print(f"Wystąpił problem z modułem MCP2221: {e}")  

        while True:
            if data.mcp != None:
                values = data.mcp.ADC_read()
                data.whiteWaterLevel = values[0] / 1024 * 100
                data.greyWaterLevel = values[1] / 1024 * 100
            else:
                data.whiteWaterLevel = random.randint(1, 100)
                data.greyWaterLevel = random.randint(1, 100)

            await nest_asyncio.asyncio.sleep(interval)       

    @classmethod
    async def initialize(cls, event_loop):
        event_loop.create_task(cls.readData(5))
