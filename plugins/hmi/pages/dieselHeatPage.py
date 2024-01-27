import nest_asyncio
from nest_asyncio import asyncio
nest_asyncio.apply()
from plugins.hmi.controls import TPage, TText, TDualStateButton, TNumber
from plugins import dieselHeater, relays
from general.logger import logging

class dieselHeatPage(TPage):
    pass

    class btHeater(TDualStateButton):
        @classmethod
        async def onRelease(cls):
            relays.data.relay2.val = cls.val
            dieselHeater.heater.onOff = cls.val

    class btThermostat(TDualStateButton):
        @classmethod
        async def onRelease(cls):
            return await super().onRelease()