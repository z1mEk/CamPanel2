'''
pip3 install EasyMCP2221
'''
import nest_asyncio
import EasyMCP2221
nest_asyncio.apply()

class data:
    mcp = None
    whiteWaterLevel = -1
    greyWaterLevel = -1

class plugin:

    @classmethod
    async def readData(cls, interval):
        while True:
            if data.mcp != None:
                values = data.mcp.ADC_read()
                data.whiteWaterLevel = values[0] / 1024 * 100
                data.greyWaterLevel = values[1] / 1024 * 100

            await nest_asyncio.asyncio.sleep(interval)       

    @classmethod
    def initialize(cls, event_loop):
        if data.mcp == None:
            try:
                data.mcp = EasyMCP2221.Device()
                data.mcp.set_pin_function(gp1='ADC', gp2="ADC")
                data.mcp.ADC_config(ref="VDD")
            except Exception as e:
                print(f"Wystąpił problem z połączeniem z modułem MCP2221: {e}")    

        event_loop.create_task(cls.readData(5))
