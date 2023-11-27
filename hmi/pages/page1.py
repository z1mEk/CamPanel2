import asyncio
from hmi import controls, methods
#from plugins import relays

async def Show():
    await methods.show(1)

class b0(controls.TButton):
    @classmethod
    async def onTouch(cls):
        pass

    @classmethod
    async def onTouch(cls):
        #relays.data.relay0.val = cls.val
        pass   

class bt0(controls.TDualStateButton):
    @classmethod
    async def onRelease(cls):
        print("Jakiesi cosi!")

class bt1(controls.TDualStateButton):
    @classmethod
    async def onRelease(cls):
        #relays.data.relay1.val = cls.val
        pass

class bt2(controls.TDualStateButton):
    @classmethod
    async def onRelease(cls):
        #relays.data.relay2.val = cls.val
        pass

class bt3(controls.TDualStateButton):
    @classmethod
    async def onRelease(cls):
        #relays.data.relay3.val = cls.val
        pass

class bt4(controls.TDualStateButton):
    @classmethod
    async def onRelease(cls):
        #relays.data.relay4.val = cls.val
        pass

class bt5(controls.TDualStateButton):
    @classmethod
    async def onRelease(cls):
        #relays.data.relay5.val = cls.val
        pass
