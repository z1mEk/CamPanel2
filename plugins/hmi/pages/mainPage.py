import nest_asyncio
from nest_asyncio import asyncio
import subprocess
nest_asyncio.apply()
from plugins.hmi import methods as hmiMethods
from plugins.hmi.controls import TPage, TButton, TProgressBar, TText, TDualStateButton, TPicture
from plugins import relays, dieselHeater, otaUpgrade
from general.logger import logging
from plugins.hmi.pages.dialogInfoPage import dialogInfoPage

class mainPage(TPage):

    @classmethod
    async def onShow(cls):
        pass
    
    @classmethod
    async def onExit(cls):      
        pass

    class bExtPages(TButton):
        pass

    class btWaterPump(TDualStateButton):
        @classmethod
        async def onRelease(cls):
            relays.data.relay0.val = cls.val

    class btACInverter(TDualStateButton): 
        @classmethod
        async def onRelease(cls):
            relays.data.relay1.val = cls.val

    class btHeater(TDualStateButton):
        @classmethod
        async def onRelease(cls):
            try:
                relays.data.relay2.val = cls.val

                if cls.val == 1:
                    await dieselHeater.plugin.start()
                else:
                    await dieselHeater.plugin.stop()
            except Exception as e:
                logging.error(f"btHeater onRelease - {e}")

            await hmiMethods.showPageName("dieselHeatPage")

    class btBoiler(TDualStateButton):
        @classmethod
        async def onRelease(cls):
            relays.data.relay3.val = cls.val

    class jWhiteWater(TProgressBar):
        pass

    class jGrayWater(TProgressBar):
        pass    

    class tWhiteWater(TText):
        pass

    class tGrayWater(TText):
        pass

    class tTime(TText):
        pass

    class tInTemp(TText):
        pass

    class tOutTemp(TText):
        pass

    class jRSOC(TProgressBar):
        @classmethod
        async def onTouch(cls):
            subprocess.Popen(['python', 'update.py'])
            await asyncio.sleep(3)

    class tRSOC(TText):
        pass

    class tVoltage(TText):
        pass
    
    class tCurrent(TText):
        pass

    class tPvPower(TText):
        pass

    class tPvVoltage(TText):
        pass

    class tPvCurrent(TText):
        pass

    class pPvStatus(TPicture):
        pass

    class pSolar(TPicture):
        pass

    class tTopBar(TText):
        pass

    class tInTempUnit(TText):
        pass

    class tOutTempUnit(TText):
        pass