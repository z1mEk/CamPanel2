from hmi.pages import controls
from hmi import hmi
from plugins import relays

async def Show():
    await hmi.client.command('page 1')

class b0(controls.TButton):
    name = 'page1.b0'
    pass

class bt0(controls.TDualStateButton):
    name = 'page1.bt0'
    
    @classmethod
    async def onRelease(cls):
        relays.data.relay0.val = cls.val

class bt1(controls.TDualStateButton):
    name = 'page1.bt1'

    @classmethod
    async def onRelease(cls):
        relays.data.relay1.val = cls.val

class bt2(controls.TDualStateButton):
    name = 'page1.bt2'
    
    @classmethod
    async def onRelease(cls):
        relays.data.relay2.val = cls.val

class bt3(controls.TDualStateButton):
    name = 'page1.bt3'

    @classmethod
    async def onRelease(cls):
        relays.data.relay3.val = cls.val

class bt4(controls.TDualStateButton):
    name = 'page1.bt4'

    @classmethod
    async def onRelease(cls):
        relays.data.relay4.val = cls.val

class bt5(controls.TDualStateButton):
    name = 'page1.bt5'

    @classmethod
    async def onRelease(cls):
        relays.data.relay5.val = cls.val
