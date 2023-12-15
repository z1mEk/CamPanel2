'''
pip3 install EasyMCP2221
'''
import nest_asyncio
import EasyMCP2221
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
            data.mcp = EasyMCP2221.Device()
            data.mcp.set_pin_function(gp1='ADC', gp2="ADC")
            data.mcp.ADC_config(ref="VDD")
        except Exception as e:
            print(f"Wystąpił problem z modułem MCP2221: {e}")  

        while True:
            if data.mcp != None:
                values = data.mcp.ADC_read()
                data.whiteWaterLevel = round(values[0] / 1024 * 100, 0)
                data.greyWaterLevel = round(values[1] / 1024 * 100, 0)

            await nest_asyncio.asyncio.sleep(interval)       

    @classmethod
    async def initialize(cls, event_loop):
        event_loop.create_task(cls.readData(5))
