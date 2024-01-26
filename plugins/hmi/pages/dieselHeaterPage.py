import nest_asyncio
from nest_asyncio import asyncio
nest_asyncio.apply()
from plugins.hmi.controls import TPage, TText, TDualStateButton, TNumber
from plugins import relays
from general.logger import logging

class dieselHeaterPage(TPage):

    class btHeater(TDualStateButton):
        @classmethod
        async def onRelease(cls):
            relays.data.relay2.val = cls.val
