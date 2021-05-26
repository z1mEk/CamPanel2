import asyncio
from hmi.pages import page0
from general.plugins import bms, waterLevel

class plugin:

    @classmethod
    async def updateBMS(cls, interval):
        while True:
            page0.t4.txt = '{}'.format(bms.data.totalVoltage)
            page0.t5.txt = '{}'.format(bms.data.RSOC)
            await asyncio.sleep(interval)

    @classmethod
    async def updateWaterLevel(cls, interval):
        while True:
            page0.j0.val = waterLevel.data.whiteWaterLevel

            # print(page0.j0.val)

            #if page0.j0.val < 50:
            #    page0.j0.pco = 63488
            #else:
            #    page0.j0.pco = 2047

            page0.j1.val = waterLevel.data.greyWaterLevel
            page0.t2.txt = '{}%'.format(waterLevel.data.whiteWaterLevel)
            page0.t3.txt = '{}%'.format(waterLevel.data.greyWaterLevel)
            page0.t6.txt = "V"
            page0.t7.txt = "%"
            await asyncio.sleep(interval)            
        

    @classmethod
    def initialize(cls):
        loop = asyncio.get_event_loop()      
        loop.create_task(cls.updateBMS(1))
        loop.create_task(cls.updateWaterLevel(1))
        #loop.run_forever
