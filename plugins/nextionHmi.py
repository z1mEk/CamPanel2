import nest_asyncio
nest_asyncio.apply()
from plugins.hmi import hmi, helper, methods as methodsHmi
from plugins.hmi.pages.MainPage import MainPage
from plugins.hmi.pages.solarWaterPage import solarWaterPage
from plugins import dalyBms, epeverTracer, waterLevel, relays, temperatures #, wifiStatus, solarWaterHeating
from datetime import datetime
from general.logger import logging
from general.configLoader import config

class plugin:

    @classmethod
    async def updateTime(cls, interval):
        while True:
            if methodsHmi.sendme() == 0:
                MainPage.tTime.txt = datetime.now().strftime("%-H:%M")
            await nest_asyncio.asyncio.sleep(interval)

    @classmethod
    async def updateTemperatures(cls, interval):
        while True:
            if methodsHmi.sendme() == 0:
                MainPage.tInTemp.txt = '{:.0f}'.format(temperatures.data.inTemp)
                MainPage.tOutTemp.txt = '{:.0f}'.format(temperatures.data.outTemp)
            await nest_asyncio.asyncio.sleep(interval)

    @classmethod
    async def updateDalyBMS(cls, interval):
        while True:
            if methodsHmi.sendme() == 0:
                MainPage.jRSOC.val = dalyBms.data.RSOC
                MainPage.tRSOC.txt = '{:.0f}'.format(dalyBms.data.RSOC)
                MainPage.tVoltage.txt = '{:.2f}V'.format(dalyBms.data.totalVoltage)

                MainPage.tCurrent.txt = (
                    '{:.0f}mA'.format(dalyBms.data.currentFlex) if abs(dalyBms.data.currentMiliAmper) < 1000 else
                    '{:.2f}A'.format(dalyBms.data.currentFlex) if abs(dalyBms.data.currentMiliAmper) < 10000 else
                    '{:.1f}A'.format(dalyBms.data.currentFlex) if abs(dalyBms.data.currentMiliAmper) < 100000 else
                    '{:.0f}A'.format(dalyBms.data.currentFlex)
                )
                
                MainPage.jRSOC.pco = (
                    helper.RGB2NextionColour(255, 0, 0) if dalyBms.data.RSOC <= 15 else
                    helper.RGB2NextionColour(255, 255, 0) if dalyBms.data.RSOC <= 30 else
                    helper.RGB2NextionColour(0, 255, 0)
                )
            
            await nest_asyncio.asyncio.sleep(interval)

    @classmethod
    async def updateEpeverTracer(cls, interval):
        while True:
            if methodsHmi.sendme() == 0:
                MainPage.tPvVoltage.txt = '{:.0f}V'.format(epeverTracer.data.pv.voltage)
                MainPage.tPvCurrent.txt = '{:.0f}A'.format(epeverTracer.data.pv.current)
                MainPage.tPvPower.txt = '{:.0f}W'.format(epeverTracer.data.pv.power)
            await nest_asyncio.asyncio.sleep(interval)

    @classmethod
    async def updateWaterLevel(cls, interval):
        while True:
            if methodsHmi.sendme() == 0:
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
            if methodsHmi.sendme() == 0:
                MainPage.btWaterPump.val = relays.data.relay0.val
                MainPage.btACInverter.val = relays.data.relay1.val
                MainPage.btHeater.val = relays.data.relay2.val
                MainPage.btBoiler.val = relays.data.relay3.val
            await nest_asyncio.asyncio.sleep(interval) 

    # @classmethod
    # async def initSolarsolarWaterHeatingDataToPage(cls):
    #     solarWaterPage.btActive.val = solarWaterHeating.data.activeHeating
    #     solarWaterPage.btBatRsoc.val = solarWaterHeating.data.RsocControl
    #     solarWaterPage.btPvVoltage.val = solarWaterHeating.data.pvVoltageControl
    #     solarWaterPage.btPvPower.val = solarWaterHeating.data.pvPowerControl
    #     solarWaterPage.btHour.val = solarWaterHeating.data.hourControl

    #     solarWaterPage.nOnBatRsoc.val = solarWaterHeating.data.onRsoc
    #     solarWaterPage.nOffBatRsoc.val = solarWaterHeating.data.offRsoc
    #     solarWaterPage.nOnPvVoltage.val = solarWaterHeating.data.onPvVoltage
    #     solarWaterPage.nOffPvVoltage.val = solarWaterHeating.data.offPvVoltage
    #     solarWaterPage.nPvPower.val = solarWaterHeating.data.minPVPower
        
    #     solarWaterPage.tOnHour.txt = solarWaterHeating.data.onHour
    #     solarWaterPage.tOffHour.txt = solarWaterHeating.data.offHour   
    #     await nest_asyncio.asyncio.sleep(1) 

    # @classmethod
    # async def updateSolarsolarWaterHeatingData(cls):
    #     solarWaterHeating.data.activeHeating = solarWaterPage.btActive.val
    #     solarWaterHeating.data.RsocControl = solarWaterPage.btBatRsoc.val
    #     solarWaterHeating.data.pvVoltageControl = solarWaterPage.btPvVoltage.val
    #     solarWaterHeating.data.pvPowerControl = solarWaterPage.btPvPower.val
    #     solarWaterHeating.data.hourControl = solarWaterPage.btHour.val

    #     solarWaterHeating.data.onRsoc = solarWaterPage.nOnBatRsoc.val
    #     solarWaterHeating.data.offRsoc = solarWaterPage.nOffBatRsoc.val
    #     solarWaterHeating.data.onPvVoltage = solarWaterPage.nOnPvVoltage.val
    #     solarWaterHeating.data.offPvVoltage = solarWaterPage.nOffPvVoltage.val
    #     solarWaterHeating.data.minPVPower = solarWaterPage.nPvPower.val

    #     solarWaterHeating.data.onHour = solarWaterPage.tOnHour.txt
    #     solarWaterHeating.data.offHour = solarWaterPage.tOffHour.txt
    #     await nest_asyncio.asyncio.sleep(1)                
        
    @classmethod
    async def initialize(cls, event_loop): 
        event_loop.create_task(hmi.create(event_loop))
        event_loop.create_task(cls.updateTime(1))
        event_loop.create_task(cls.updateTemperatures(10))   
        event_loop.create_task(cls.updateDalyBMS(2))
        event_loop.create_task(cls.updateEpeverTracer(2))
        event_loop.create_task(cls.updateWaterLevel(30))
        event_loop.create_task(cls.updateDualStateButtonValue(1))
        #event_loop.create_task(cls.initSolarsolarWaterHeatingDataToPage())