import nest_asyncio
from nest_asyncio import asyncio
nest_asyncio.apply()
from plugins.hmi.controls import TPage, TText, TDualStateButton, TNumber
from general.logger import logging

class solarWaterPage(TPage):

    # @classmethod
    # async def onShow(cls):
    #     logging.info(f"on Show Udało się")

    # @classmethod
    # async def onExit(cls):
    #     logging.info(f"on Exit Udało się")

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
 