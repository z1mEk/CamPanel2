import asyncio
from hmi.pages import page0
from general import plugins
from hmi import methods, helper

class plugin:

    @classmethod
    async def updateBMS(cls, interval):
        while True:
            page0.t4.txt = '{}'.format(plugins.bms.data.totalVoltage)
            page0.t5.txt = '{}'.format(plugins.bms.data.RSOC)
            await asyncio.sleep(interval)

    @classmethod
    async def updateWaterLevel(cls, interval):
        while True:
            page0.j0.val = plugins.waterLevel.data.whiteWaterLevel
            page0.j1.val = plugins.waterLevel.data.greyWaterLevel
            page0.t2.txt = '{}%'.format(plugins.waterLevel.data.whiteWaterLevel)
            page0.t3.txt = '{}%'.format(plugins.waterLevel.data.greyWaterLevel)
            await asyncio.sleep(interval)            
        
    @classmethod
    def onStart(cls):
        page0.t6.txt = "V"
        page0.t7.txt = "%"

    @classmethod
    def initialize(cls,  event_loop):  
        #cls.onStart()
        event_loop.create_task(cls.updateBMS(1))
        event_loop.create_task(cls.updateWaterLevel(1))
