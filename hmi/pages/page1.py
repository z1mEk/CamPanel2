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
        relays.relay0.val = cls.val
        print(relays.data.relay0.address, relays.data.data.relay0.val)

class bt1(controls.TDualStateButton):
    name = 'page1.bt1'

    @classmethod
    async def onRelease(cls):
        relays.data.relay1.val = cls.val
        print(relays.data.relay1.address, relays.data.relay1.val)

class bt2(controls.TDualStateButton):
    name = 'page1.bt2'
    pass

class bt3(controls.TDualStateButton):
    name = 'page1.bt3'
    pass

class bt4(controls.TDualStateButton):
    name = 'page1.bt4'
    pass

class bt5(controls.TDualStateButton):
    name = 'page1.bt5'
    pass
