import nest_asyncio
from nest_asyncio import asyncio
nest_asyncio.apply()
from plugins.hmi import hmi, helper, methods as methodsHmi
from plugins.hmi.pages.mainPage import mainPage
from plugins.hmi.pages.solarWaterPage import solarWaterPage
from plugins.hmi.pages.dieselHeatPage import dieselHeatPage
from plugins import dalyBms, epeverTracer, waterLevel, relays, temperatures , solarWaterHeating, dieselHeater
from datetime import datetime
from general.logger import logging
from general.configLoader import config

class plugin:

    @classmethod
    async def updateTime(cls, interval):
        while True:
            if await methodsHmi.getCurrentPageId() == 0:
                mainPage.tTime.txt = datetime.now().strftime("%-H:%M")
            await asyncio.sleep(interval)

    @classmethod
    async def updateTemperatures(cls, interval):
        while True:
            if await methodsHmi.getCurrentPageId() == 0:
                mainPage.tInTemp.txt = '{:.0f}'.format(temperatures.data.inTemp)
                mainPage.tOutTemp.txt = '{:.0f}'.format(temperatures.data.outTemp)
            await asyncio.sleep(interval)

    @classmethod
    async def updateDalyBMS(cls, interval):
        while True:
            if await methodsHmi.getCurrentPageId() == 0:
                mainPage.jRSOC.val = dalyBms.data.RSOC
                mainPage.tRSOC.txt = '{:.0f}'.format(dalyBms.data.RSOC)
                mainPage.tVoltage.txt = '{:.2f}V'.format(dalyBms.data.totalVoltage)
                
                mainPage.tCurrent.txt = (
                    '{:.0f}mA'.format(dalyBms.data.currentFlex) if abs(dalyBms.data.currentMiliAmper) < 1000 else
                    '{:.2f}A'.format(dalyBms.data.currentFlex) if abs(dalyBms.data.currentMiliAmper) < 10000 else
                    '{:.1f}A'.format(dalyBms.data.currentFlex) if abs(dalyBms.data.currentMiliAmper) < 100000 else
                    '{:.0f}A'.format(dalyBms.data.currentFlex)
                )
                
                mainPage.jRSOC.pco = (
                    helper.RGB2NextionColour(255, 0, 0) if dalyBms.data.RSOC <= 15 else
                    helper.RGB2NextionColour(255, 255, 0) if dalyBms.data.RSOC <= 30 else
                    helper.RGB2NextionColour(0, 255, 0)
                )
            
            await asyncio.sleep(interval)

    @classmethod
    async def updateEpeverTracer(cls, interval):
        while True:
            if await methodsHmi.getCurrentPageId() == 0:
                mainPage.tPvVoltage.txt = '{:.0f}V'.format(epeverTracer.data.pv.voltage)
                mainPage.tPvCurrent.txt = '{:.0f}A'.format(epeverTracer.data.pv.current)
                mainPage.tPvPower.txt = '{:.0f}W'.format(epeverTracer.data.pv.power)
            await asyncio.sleep(interval)

    @classmethod
    async def updateWaterLevel(cls, interval):
        while True:
            if await methodsHmi.getCurrentPageId() == 0:
                mainPage.jWhiteWater.val = waterLevel.data.whiteWaterLevel 
                mainPage.jWhiteWater.pco = (
                    helper.RGB2NextionColour(0, 130, 255) if waterLevel.data.whiteWaterLevel > 20 else
                    helper.RGB2NextionColour(255, 0, 0)
                )

                mainPage.jGrayWater.val = waterLevel.data.greyWaterLevel
                mainPage.jGrayWater.pco = (
                    helper.RGB2NextionColour(150, 150, 150) if waterLevel.data.greyWaterLevel < 80
                    else helper.RGB2NextionColour(255, 0, 0)
                )
                mainPage.tWhiteWater.txt = '{:.0f}%'.format(waterLevel.data.whiteWaterLevel)
                mainPage.tGrayWater.txt = '{:.0f}%'.format(waterLevel.data.greyWaterLevel)
            await asyncio.sleep(interval)      

    @classmethod
    async def updateDualStateButtonValue(cls, interval):
        while True:
            if await methodsHmi.getCurrentPageId() == 0:
                mainPage.btWaterPump.val = relays.data.relay0.val
                mainPage.btACInverter.val = relays.data.relay1.val
                mainPage.btHeater.val = relays.data.relay2.val
                mainPage.btBoiler.val = relays.data.relay3.val
            await asyncio.sleep(interval) 

    @classmethod
    async def initSolarsolarWaterHeatingDataToPage(cls):
        solarWaterPage.btActive.val = solarWaterHeating.data.activeHeating
        solarWaterPage.btBatRsoc.val = solarWaterHeating.data.RsocControl
        solarWaterPage.btPvVoltage.val = solarWaterHeating.data.pvVoltageControl
        solarWaterPage.btPvPower.val = solarWaterHeating.data.pvPowerControl
        solarWaterPage.btHour.val = solarWaterHeating.data.hourControl

        solarWaterPage.nOnBatRsoc.val = solarWaterHeating.data.onRsoc
        solarWaterPage.nOffBatRsoc.val = solarWaterHeating.data.offRsoc
        solarWaterPage.nOnPvVoltage.val = solarWaterHeating.data.onPvVoltage
        solarWaterPage.nOffPvVoltage.val = solarWaterHeating.data.offPvVoltage
        solarWaterPage.nPvPower.val = solarWaterHeating.data.minPVPower

        solarWaterPage.tOnHour.txt = solarWaterHeating.data.onHour
        solarWaterPage.tOffHour.txt = solarWaterHeating.data.offHour   
        await asyncio.sleep(1) 

    @classmethod
    async def updateSolarsolarWaterHeatingData(cls, interval): 
        while True:
            if await methodsHmi.getCurrentPageId() == 1:
                solarWaterHeating.data.activeHeating = solarWaterPage.btActive.val
                solarWaterHeating.data.RsocControl = solarWaterPage.btBatRsoc.val
                solarWaterHeating.data.pvVoltageControl = solarWaterPage.btPvVoltage.val
                solarWaterHeating.data.pvPowerControl = solarWaterPage.btPvPower.val
                solarWaterHeating.data.hourControl = solarWaterPage.btHour.val

                solarWaterHeating.data.onRsoc = solarWaterPage.nOnBatRsoc.val
                solarWaterHeating.data.offRsoc = solarWaterPage.nOffBatRsoc.val
                solarWaterHeating.data.onPvVoltage = solarWaterPage.nOnPvVoltage.val
                solarWaterHeating.data.offPvVoltage = solarWaterPage.nOffPvVoltage.val
                solarWaterHeating.data.minPVPower = solarWaterPage.nPvPower.val

                solarWaterHeating.data.onHour = solarWaterPage.tOnHour.txt
                solarWaterHeating.data.offHour = solarWaterPage.tOffHour.txt
            await asyncio.sleep(interval)                

    @classmethod
    async def updateDieselHeaterData(cls, interval):
        while True:
            try:
                if await methodsHmi.getCurrentPageId() == 2:
                    dieselHeatPage.tValue.txt = "{:.1f}".format(dieselHeater.data.displayGradHzValue)
                    dieselHeatPage.btHeater.val = relays.data.relay2.val
                    dieselHeatPage.btThermostat.val = dieselHeater.transmitPacket.thermostatMode
                    dieselHeatPage.tStatus.txt = "{:.0f}".format(dieselHeater.data.runState)
                    dieselHeatPage.tVoltage.txt = "{:.1f}V".format(dieselHeater.data.supplyVoltage)
                    dieselHeatPage.tRpm.txt = "{:.0f}".format(dieselHeater.data.fanRpm)
                    dieselHeatPage.tFrequency.txt = "{:.1f}Hz".format(dieselHeater.data.actualPumpFreq)
                    dieselHeatPage.tHeaterTemp.txt = "{:.0f}°C".format(dieselHeater.data.heatExchTemp)
                    dieselHeatPage.tGlowPlugCurr.txt = "{:.2f}A".format(dieselHeater.data.glowPlugCurrent)
                    dieselHeatPage.tError.txt = dieselHeater.data.errorDisplay
            except Exception as e:
                logging.error(f"updateDieselHeaterData - {e}")
            await asyncio.sleep(interval)  

    @classmethod
    async def initialize(cls, event_loop): 
        event_loop.create_task(hmi.create(event_loop))
        event_loop.create_task(cls.updateTime(1))
        event_loop.create_task(cls.updateTemperatures(5))   
        event_loop.create_task(cls.updateDalyBMS(2))
        event_loop.create_task(cls.updateEpeverTracer(2))
        event_loop.create_task(cls.updateWaterLevel(2))
        event_loop.create_task(cls.updateDualStateButtonValue(1))
        event_loop.create_task(cls.initSolarsolarWaterHeatingDataToPage())
        event_loop.create_task(cls.updateSolarsolarWaterHeatingData(1))
        event_loop.create_task(cls.updateDieselHeaterData(1))