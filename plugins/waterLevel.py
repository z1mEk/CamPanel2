'''
pip3 install EasyMCP2221
'''
import nest_asyncio
import EasyMCP2221
nest_asyncio.apply()

class data:
    mcp = None
    whiteWaterLevel = 0
    greyWaterLevel = 0

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
            if data.mcp == None:
                cls.reconnect()
            data.mcp.set_pin_function(gp1='ADC', gp2="ADC")
            data.mcp.ADC_config(ref="VDD")                
            values = data.mcp.ADC_read()
            data.whiteWaterLevel = int((values[0] / 1023) * 100)
            data.greyWaterLevel = int((values[1] / 1023) * 100)
            await nest_asyncio.asyncio.sleep(interval)       

    @classmethod
    async def initialize(cls, event_loop):
        event_loop.create_task(cls.readData(5))
