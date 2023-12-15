from plugins.hmi import methods as hmiMethods
from plugins.hmi.controls import TButton, TDualStateButton
from plugins import relays

async def Show():
    await hmiMethods.show(1)

class b0(TButton):
    pass 

class bt0(TDualStateButton):
    @classmethod
    async def onRelease(cls):
        relays.data.relay0.val = cls.val

class bt1(TDualStateButton):
    @classmethod
    async def onRelease(cls):
        relays.data.relay1.val = cls.val

class bt2(TDualStateButton):
    @classmethod
    async def onRelease(cls):
        relays.data.relay2.val = cls.val

class bt3(TDualStateButton):
    @classmethod
    async def onRelease(cls):
        relays.data.relay3.val = cls.val

class bt4(TDualStateButton):
    @classmethod
    async def onRelease(cls):
        relays.data.relay4.val = cls.val

class bt5(TDualStateButton):
    @classmethod
    async def onRelease(cls):
        relays.data.relay5.val = cls.val
