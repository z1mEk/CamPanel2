import hmi
from hmi.pages import page0, page1

#region Screen events
async def startup():
    print("startup")

async def auto_sleep():
    print("auto sleep")

async def auto_wake():
    print("auto wake")
    
async def touch_in_sleep(data):
    print(data)

async def touch_coordinate(data):
    print(data)
#endregion

#region Screen methods
async def wakeup():
    hmi.client.command('sleep=0')

async def sleep():
    hmi.client.command('sleep=1')
#endregion

#region Touch events
async def page0_b0_touch():
    await page0.b0.onTouch()

async def page0_t4_touch():
    await page0.t4.onTouch()

async def page0_t5_touch():
    await page0.t5.onTouch()   

async def page1_b0_touch():
    await page1.b0.onTouch()

async def page1_bt0_release():
    await page1.bt0.onRelease()

async def page1_bt1_release():
    await page1.bt1.onRelease()    

async def page1_bt2_release():
    await page1.bt2.onRelease()    

async def page1_bt3_release():
    await page1.bt3.onRelease()     

async def page1_bt4_release():
    await page1.bt4.onRelease()  

async def page1_bt5_release():
    await page1.bt5.onRelease()
#endregion
                  