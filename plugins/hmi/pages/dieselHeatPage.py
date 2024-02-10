import nest_asyncio
from nest_asyncio import asyncio
nest_asyncio.apply()
from plugins.hmi.controls import TPage, TText, TDualStateButton, TButton, TNumber, TProgressBar, TVariable
from plugins import dieselHeater, relays
from general.logger import logging

class dieselHeatPage(TPage):

    @classmethod
    async def onShow(cls):
        pass #test
    
    @classmethod
    async def onExit(cls):      
        pass

    class btHeater(TDualStateButton):
        @classmethod
        async def onRelease(cls):
            if cls.val == 1:
                await dieselHeater.plugin.start()
            else:
                await dieselHeater.plugin.stop()
            
            dieselHeater.data.onOff = cls.val

    class btThermostat(TDualStateButton):
        @classmethod
        async def onRelease(cls):
            dieselHeater.transmitPacket.thermostatMode = cls.val
        
    class bUp(TButton):
        @classmethod
        async def onTouch(cls):
            await dieselHeater.plugin.up()

    class bDown(TButton):
        @classmethod
        async def onTouch(cls):
            await dieselHeater.plugin.down()

    class tValue(TText):
        pass
        
    class tStatus(TText):
        pass

    class tVoltage(TText):
        pass

    class tRpm(TText):
        pass

    class tFrequency(TText):
        pass

    class tHeaterTemp(TText):
        pass

    class tGlowPlugCurr(TText):
        pass

    class tError(TText):
        pass

    class vaWent(TVariable):
        pass

    class vaHeaterTemp(TVariable):
        pass

    class vaPump(TVariable):
        pass

    class vaGlowCurrent(TVariable):
        pass