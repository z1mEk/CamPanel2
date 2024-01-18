import nest_asyncio
nest_asyncio.apply()
from plugins.hmi.controls import TPage, TText, TDualStateButton, TNumber
from general.logger import logging

class solarWaterPage(TPage):

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
 