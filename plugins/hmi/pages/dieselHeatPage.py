import nest_asyncio
from nest_asyncio import asyncio
nest_asyncio.apply()
from plugins.hmi.controls import TPage, TText, TDualStateButton, TButton, TNumber, TProgressBar
from plugins import dieselHeater, relays
from general.logger import logging

class dieselHeatPage(TPage):
    pass

    class btHeater(TDualStateButton):
        @classmethod
        async def onRelease(cls):
            relays.data.relay2.val = cls.val
            dieselHeater.heater.onOff = cls.val #TODO: to trzeba zmienić, to ma działać inaczej
            if cls.val == 1:
                await dieselHeater.heater.start()
            else:
                await dieselHeater.heater.stop()

    class btThermostat(TDualStateButton):
        @classmethod
        async def onRelease(cls):
            dieselHeater.heater.transmitPacket.thermostatMode = cls.val
        
    class bUp(TButton):
        @classmethod
        async def onTouch(cls):
            await dieselHeater.heater.up()

    class bDown(TButton):
        @classmethod
        async def onTouch(cls):
            await dieselHeater.heater.down()
        
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

    class jT1(TProgressBar):
        pass

    class jT2(TProgressBar):
        pass

    class jT3(TProgressBar):
        pass

    class jT4(TProgressBar):
        pass

    class jT5(TProgressBar):
        pass

    class jT6(TProgressBar):
        pass