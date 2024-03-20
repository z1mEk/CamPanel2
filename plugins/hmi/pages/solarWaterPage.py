import nest_asyncio
from nest_asyncio import asyncio
nest_asyncio.apply()
from plugins.hmi.controls import TPage, TText, TDualStateButton, TNumber
from general.logger import logging
from plugins import solarWaterHeating

class solarWaterPage(TPage):

    @classmethod
    async def onShow(cls):
        pass
    
    @classmethod
    async def onExit(cls):
        solarWaterHeating.data.activeHeating = cls.btActive.val
        solarWaterHeating.data.inverterAutoOff = cls.btInverter.val
        solarWaterHeating.data.RsocControl = cls.btBatRsoc.val
        solarWaterHeating.data.pvVoltageControl = cls.btPvVoltage.val
        solarWaterHeating.data.pvPowerControl = cls.btPvPower.val
        solarWaterHeating.data.hourControl = cls.btHour.val

        solarWaterHeating.data.onRsoc = cls.nOnBatRsoc.val
        solarWaterHeating.data.offRsoc = cls.nOffBatRsoc.val
        solarWaterHeating.data.onPvVoltage = cls.nOnPvVoltage.val
        solarWaterHeating.data.offPvVoltage = cls.nOffPvVoltage.val
        solarWaterHeating.data.minPVPower = cls.nPvPower.val

        solarWaterHeating.data.onHour = cls.tOnHour.txt
        solarWaterHeating.data.offHour = cls.tOffHour.txt        

    class btActive(TDualStateButton):
        @classmethod
        def onRelease(cls):
            if cls.btActive.val == 0:
                cls.btInverter = 0

    class btInverter(TDualStateButton):
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
 