import nest_asyncio
nest_asyncio.apply()
from plugins.hmi import hmi, helper
from plugins.hmi.pages.MainPage import MainPage
from plugins import dalyBms, waterLevel, relays
from datetime import datetime

class plugin:

    @classmethod
    async def updateTime(cls, interval):
        while True:
            MainPage.tTime.txt = datetime.now().strftime("%H:%M")
            await nest_asyncio.asyncio.sleep(interval)

    @classmethod
    async def updateTemperatures(cls, interval):
        while True:
            MainPage.tInTemp.txt = '{:.0f}°C'.format(21)
            MainPage.tOutTemp.txt = '{:.0f}°C'.format(5)
            await nest_asyncio.asyncio.sleep(interval)

    @classmethod
    async def updateBMS(cls, interval):
        while True:
            MainPage.jRSOC.val = dalyBms.data.RSOC
            MainPage.tRSOC.txt = '{:.0f}'.format(dalyBms.data.RSOC)
            MainPage.tVoltage.txt = dalyBms.data.totalVoltageDisplay
            MainPage.tCurrent.txt = dalyBms.data.currentDisplay
            MainPage.tPvPower.txt = '{:.0f}W'.format(88)
            await nest_asyncio.asyncio.sleep(interval)

    @classmethod
    async def updateWaterLevel(cls, interval):
        while True:
            MainPage.jWhiteWater.val = waterLevel.data.whiteWaterLevel if waterLevel.data.whiteWaterLevel >= 0 else 0 
            MainPage.jWhiteWater.pco = 1055 if waterLevel.data.whiteWaterLevel > 20 else helper.RGB2NextionColour(255, 0, 0)
            MainPage.jGrayWater.val = waterLevel.data.greyWaterLevel if waterLevel.data.greyWaterLevel >= 0 else 0
            MainPage.jGrayWater.pco = 40179 if waterLevel.data.greyWaterLevel < 80 else helper.RGB2NextionColour(255, 0, 0)
            MainPage.tWhiteWater.txt = waterLevel.data.whiteWaterLevelDisplay
            MainPage.tGrayWater.txt = waterLevel.data.greyWaterLevelDisplay
            await nest_asyncio.asyncio.sleep(interval)      

    @classmethod
    async def updateDualStateButtonValue(cls, interval):
        while True:
            MainPage.btWaterPump.val = relays.data.relay0.val
            MainPage.btACInverter.val = relays.data.relay1.val
            MainPage.btHeater.val = relays.data.relay2.val
            MainPage.btBoiler.val = relays.data.relay3.val
            await nest_asyncio.asyncio.sleep(interval) 
        
    @classmethod
    async def initialize(cls, event_loop): 
        event_loop.create_task(hmi.create(event_loop))
        event_loop.create_task(cls.updateTime(1))
        event_loop.create_task(cls.updateTemperatures(60))   
        event_loop.create_task(cls.updateBMS(2))
        event_loop.create_task(cls.updateWaterLevel(60))
        event_loop.create_task(cls.updateDualStateButtonValue(1))
