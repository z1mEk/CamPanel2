import nest_asyncio
nest_asyncio.apply()
from plugins.hmi import methods as hmiMethods
from plugins.hmi.controls import TButton, TProgressBar, TText

async def Show():
    await hmiMethods.show(0)

class b0(TButton):
    pass

class j0(TProgressBar):
    pass

class j1(TProgressBar):
    pass

class t1(TText):
    pass

class t2(TText):
    pass

class t3(TText):
    pass

class t4(TText):
    pass

class t5(TText):
    pass
 
class t6(TText):
    pass

class t7(TText): 
    pass
