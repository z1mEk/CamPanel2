import nest_asyncio
from nest_asyncio import asyncio
nest_asyncio.apply()
from plugins.hmi.controls import TPage, TText, TDualStateButton, TNumber
from general.logger import logging
from plugins import solarWaterHeating

class solarWaterPage(TPage):

    @classmethod
    async def onShow(cls):
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
        solarWaterPage.tOffHour.txt =solarWaterHeating.data.offHour
    
    @classmethod
    async def onExit(cls):
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

    class btActive(TDualStateButton):
        pass

    class btBatRsoc(TDualStateButton):
        pass

    class btPvVoltage(TDualStateButton):
        pass

    class btPvPower(TDualStateButton):
        pass

    class btHour(TDualStateButton):
        pass

    class nOnBatRsoc(TNumber):
        pass

    class nOffBatRsoc(TNumber):
        pass

    class nOnPvVoltage(TNumber):
        pass

    class nOffPvVoltage(TNumber):
        pass

    class nPvPower(TNumber):
        pass

    class tOnHour(TText):
        pass

    class tOffHour(TText):
        pass
 