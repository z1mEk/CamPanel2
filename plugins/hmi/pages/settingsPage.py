import nest_asyncio
from nest_asyncio import asyncio
nest_asyncio.apply()
from plugins.hmi.controls import TPage, TText, TDualStateButton, TNumber
from general.logger import logging

class settingsPage(TPage):

    @classmethod
    async def onShow(cls):
        return await super().onShow()
    
    @classmethod
    async def onExit(cls):      
        return await super().onExit()