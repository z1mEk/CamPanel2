import nest_asyncio
nest_asyncio.apply()
from plugins.hmi import hmi, helper
from plugins.hmi.pages import page0
from plugins.hmi.pages import page1
from plugins import dalyBms, waterLevel, relays

class plugin:

    @classmethod
    async def updateBMS(cls, interval):
        while True:
            page0.t4.txt = '{}'.format(dalyBms.data.totalVoltage)
            page0.t5.txt = '{}'.format(dalyBms.data.RSOC)
            await nest_asyncio.asyncio.sleep(interval)

    @classmethod
    async def updateWaterLevel(cls, interval):
        while True:
            page0.j0.val = waterLevel.data.whiteWaterLevel if waterLevel.data.whiteWaterLevel >= 0 else 0 
            page0.j0.pco = helper.RGB2NextionColour(0, 255, 255) if waterLevel.data.whiteWaterLevel > 20 else helper.RGB2NextionColour(255, 0, 0)
            page0.j1.val = waterLevel.data.greyWaterLevel if waterLevel.data.greyWaterLevel >= 0 else 0
            page0.j1.pco = helper.RGB2NextionColour(0, 255, 255) if waterLevel.data.greyWaterLevel < 80 else helper.RGB2NextionColour(255, 0, 0)
            page0.t2.txt = '{}%'.format(waterLevel.data.whiteWaterLevel)
            page0.t3.txt = '{}%'.format(waterLevel.data.greyWaterLevel)
            await nest_asyncio.asyncio.sleep(interval)      

    @classmethod
    async def updateDualStateButtonValue(cls, interval):
        while True:
            page1.bt0.val = relays.data.relay0.val
            page1.bt1.val = relays.data.relay1.val
            page1.bt2.val = relays.data.relay2.val
            page1.bt3.val = relays.data.relay3.val
            page1.bt4.val = relays.data.relay4.val
            page1.bt5.val = relays.data.relay5.val
            await nest_asyncio.asyncio.sleep(interval) 
        
    @classmethod
    async def initialize(cls, event_loop): 
        event_loop.create_task(hmi.create(event_loop))
        event_loop.create_task(cls.updateBMS(1))
        event_loop.create_task(cls.updateWaterLevel(10))
        event_loop.create_task(cls.updateDualStateButtonValue(1))
