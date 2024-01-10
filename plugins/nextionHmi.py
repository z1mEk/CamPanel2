import nest_asyncio
nest_asyncio.apply()
from plugins.hmi import hmi, helper
from plugins.hmi.pages.MainPage import MainPage
from plugins import dalyBms, waterLevel, relays, temperatures, wifiStatus
from datetime import datetime
from general.logger import logging

class plugin:

    @classmethod
    async def updateTime(cls, interval):
        while True:
            MainPage.tTime.txt = datetime.now().strftime("%H:%M")
            await nest_asyncio.asyncio.sleep(interval)

    @classmethod
    async def updateTemperatures(cls, interval):
        while True:
            MainPage.tInTemp.txt = '{:.0f}'.format(temperatures.data.inTemp)
            MainPage.tOutTemp.txt = '{:.0f}'.format(temperatures.data.outTemp)
            await nest_asyncio.asyncio.sleep(interval)

    @classmethod
    async def updateBMS(cls, interval):
        while True:
            MainPage.jRSOC.val = dalyBms.data.RSOC
            MainPage.tRSOC.txt = '{:.0f}'.format(dalyBms.data.RSOC)
            MainPage.tVoltage.txt = '{:.2f}V'.format(dalyBms.data.totalVoltage)

            MainPage.tCurrent.txt = (
                '{:.0f}mA'.format(dalyBms.data.currentFlex) if abs(dalyBms.data.currentMiliAmper) < 1000 else
                '{:.2f}A'.format(dalyBms.data.currentFlex) if abs(dalyBms.data.currentMiliAmper) < 10000 else
                '{:.1f}A'.format(dalyBms.data.currentFlex) if abs(dalyBms.data.currentMiliAmper) < 100000 else
                '{:.0f}A'.format(dalyBms.data.currentFlex)
            )
            
            MainPage.tPvPower.txt = '{:.0f}W'.format(88)

            MainPage.jRSOC.pco = (
                helper.RGB2NextionColour(255, 0, 0) if dalyBms.data.RSOC <= 15 else
                helper.RGB2NextionColour(255, 255, 0) if dalyBms.data.RSOC <= 30 else
                helper.RGB2NextionColour(0, 255, 0)
            )
            
            await nest_asyncio.asyncio.sleep(interval)

    @classmethod
    async def updateWaterLevel(cls, interval):
        while True:
            MainPage.jWhiteWater.val = waterLevel.data.whiteWaterLevel 
            MainPage.jWhiteWater.pco = (
                helper.RGB2NextionColour(0, 130, 255) if waterLevel.data.whiteWaterLevel > 20 else
                helper.RGB2NextionColour(255, 0, 0)
            )
            MainPage.jGrayWater.val = waterLevel.data.greyWaterLevel
            MainPage.jGrayWater.pco = (
                helper.RGB2NextionColour(150, 150, 150) if waterLevel.data.greyWaterLevel < 80
                else helper.RGB2NextionColour(255, 0, 0)
            )
            MainPage.tWhiteWater.txt = '{:.0f}%'.format(waterLevel.data.whiteWaterLevel)
            MainPage.tGrayWater.txt = '{:.0f}%'.format(waterLevel.data.greyWaterLevel)
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
        event_loop.create_task(cls.updateTemperatures(5))   
        event_loop.create_task(cls.updateBMS(2))
        event_loop.create_task(cls.updateWaterLevel(5))
        event_loop.create_task(cls.updateDualStateButtonValue(1))
