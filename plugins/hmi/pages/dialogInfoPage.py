import nest_asyncio
from nest_asyncio import asyncio
nest_asyncio.apply()
from plugins.hmi.controls import TPage, TText, TButton
from general.logger import logging
from plugins.hmi import methods as methodsHmi

class dialogInfoPage(TPage):

    previusPage = 0

    @classmethod
    async def showMessage(cls, message, previusPage):
        cls.previusPage = previusPage
        cls.tMessage.txt = message
        await methodsHmi.showPageName(dialogInfoPage.name)

    class tMessage(TText):
        pass

    class bOK(TButton):
        @classmethod
        async def onTouch(cls):
            await methodsHmi.showPageId(dialogInfoPage.previusPage)
