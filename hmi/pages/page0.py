from hmi.pages import controls
from hmi import hmi, methods

async def Show():
    await hmi.client.command('page 0')

class b0(controls.TButton):
    name = 'page0.b0'
    pass

class j0(controls.TProgressBar):
    name = 'page0.j0'
    pass

class j1(controls.TProgressBar):
    name = 'page0.j1'
    pass

class t2(controls.TText):
    name = 'page0.t2'
    pass

class t3(controls.TText):
    name = 'page0.t3'
    pass

class t4(controls.TText):
    name = 'page0.t4'
    pass

class t5(controls.TText):
    name = 'page0.t5'
    pass
 
class t6(controls.TText):
    name = 'page0.t6'
    pass

class t7(controls.TText): 
    name = 'page0.t7'
    pass