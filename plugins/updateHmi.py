import asyncio
from hmi.pages import page0
from general import plugins

class plugin:
    name = 'Update HMI'

    @classmethod
    async def updateBMS(self, interval):
        while True:
            await page0.t4.setTxt('{:.2f}'.format(plugins.bms.data.totalVoltage / 1000))
            await page0.t5.setTxt('{}'.format(plugins.bms.data.RSOC))
            await page0.t6.setTxt('V')
            await page0.t7.setTxt('%')
            await asyncio.sleep(interval)

    @classmethod
    async def updateWaterLevel(self, interval):
        while True:
            await page0.j0.setVal(plugins.waterLevel.data.whiteWater)
            await page0.j1.setVal(plugins.waterLevel.data.greyWater)
            await page0.t2.setTxt('{}%'.format(plugins.waterLevel.data.whiteWaterLevel))
            await page0.t3.setTxt('{}%'.format(plugins.waterLevel.data.greyWaterLevel))
            await asyncio.sleep(interval)            
        

    @classmethod
    def initialize(self):
        loop = asyncio.get_event_loop()      
        loop.create_task(self.updateBMS(5))
        loop.create_task(self.updateWaterLevel(5))
        loop.run_forever
