import asyncio
from hmi.pages import page0, page1
from plugins import dalyBms, waterLevel
from hmi import methods, helper

class plugin:

    @classmethod
    async def updateBMS(cls, interval):
        while True:
            page0.t4.txt = '{}'.format(dalyBms.data.totalVoltage)
            page0.t5.txt = '{}'.format(dalyBms.data.RSOC)
            await asyncio.sleep(interval)

    @classmethod
    async def updateWaterLevel(cls, interval):
        while True:
            page0.j0.val = waterLevel.data.whiteWaterLevel
            page0.j0.pco = helper.RGB2NextionColour(0, 255, 255) if waterLevel.data.whiteWaterLevel > 20 else helper.RGB2NextionColour(255, 0, 0)
            page0.j1.val = waterLevel.data.greyWaterLevel
            page0.j1.pco = helper.RGB2NextionColour(0, 255, 255) if waterLevel.data.greyWaterLevel < 80 else helper.RGB2NextionColour(255, 0, 0)
            page0.t2.txt = '{}%'.format(waterLevel.data.whiteWaterLevel)
            page0.t3.txt = '{}%'.format(waterLevel.data.greyWaterLevel)
            await asyncio.sleep(interval)      

    @classmethod
    async def updateDualStateButtonValue(cls, interval):
        while True:
            # page1.bt0.val = plugins.relays.data.currentStates[0]
            # page1.bt1.val = plugins.relays.data.currentStates[1]
            # page1.bt2.val = plugins.relays.data.currentStates[2]
            # page1.bt3.val = plugins.relays.data.currentStates[3]
            # page1.bt4.val = plugins.relays.data.currentStates[4]
            # page1.bt5.val = plugins.relays.data.currentStates[5]
            await asyncio.sleep(interval) 
        
    @classmethod
    def initialize(cls, event_loop):  
        event_loop.create_task(cls.updateBMS(1))
        event_loop.create_task(cls.updateWaterLevel(1))
        #event_loop.create_task(cls.updateDualStateButtonValue(1))
