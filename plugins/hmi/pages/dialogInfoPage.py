import nest_asyncio
from nest_asyncio import asyncio
nest_asyncio.apply()
from plugins.hmi.controls import TPage, TText, TButton
from general.logger import logging
from plugins.hmi import methods as methodsHmi

class dialogInfoPage(TPage):

    returnPageId = 0

    @classmethod
    async def showMessage(cls, message, returnPageId, autoCloseTime=0):
        cls.returnPageId = returnPageId
        cls.tMessage.txt = message
        await methodsHmi.showPageName(dialogInfoPage.name)
        if cls.autoCloseTime > 0:
            await asyncio.sleep(autoCloseTime)
            await methodsHmi.showPageId(dialogInfoPage.returnPageId)

    class tMessage(TText):
        pass

    class bOK(TButton):
        @classmethod
        async def onTouch(cls):
            await methodsHmi.showPageId(dialogInfoPage.returnPageId)
