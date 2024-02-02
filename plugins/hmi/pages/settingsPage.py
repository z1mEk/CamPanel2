import nest_asyncio
from nest_asyncio import asyncio
nest_asyncio.apply()
from plugins.hmi.controls import TPage, TDualStateButton, TText
from plugins import wifiStatus
from general.logger import logging

class settingsPage(TPage):

    @classmethod
    async def onShow(cls):
        cls.btWifi.val = wifiStatus.data.wifiStatus
    
    @classmethod
    async def onExit(cls):      
        wifiStatus.data.wifiStatus = cls.btWifi.val

    class btWifi(TDualStateButton):
        pass

    class nScreenSaver(TText):
        pass