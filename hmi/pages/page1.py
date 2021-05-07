from hmi.pages import controls
from hmi import hmi

async def Show():
    await hmi.client.command('page 1')

class b0(controls.TButton):
    name = 'page1.b0'
    pass

class bt0(controls.TDualStateButton):
    name = 'page1.bt0'
    pass

class bt1(controls.TDualStateButton):
    name = 'page1.bt1'
    pass

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
