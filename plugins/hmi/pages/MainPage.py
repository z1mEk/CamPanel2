import nest_asyncio
nest_asyncio.apply()
from plugins.hmi import methods as hmiMethods
from plugins.hmi.controls import TPage, TButton, TProgressBar, TText, TDualStateButton, TPicture
from plugins import relays

class MainPage(TPage):

    id = 0

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
            relays.data.relay2.val = cls.val

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
        pass

    class tRSOC(TText):
        pass

    class tVoltage(TText):
        pass
    
    class tCurrent(TText):
        pass

    class tPvPower(TText):
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