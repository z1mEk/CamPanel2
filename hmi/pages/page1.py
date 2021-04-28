from hmi import hmi
from hmi.pages import page0
from hmi import screen

async def Show():
    await hmi.client.command('page 1')

class b0():
    name = 'page1.b0'

    async def onTouch():
        print("page1.b0 onTouch")

class bt0():
    name = 'page1.bt0'
    async def getVal():
        return await hmi.client.get(__class__.name + '.val')

    async def setVal(value):
        await hmi.client.set(__class__.name + '.val', value)

    async def onRelease():
        val = await __class__.getVal()
        print("page1.bt0 onRelease")
        if val == 1:
            await page0.j0.setVal(30)
        else:
            await page0.j0.setVal(0)

class bt1():
    name = 'page1.bt1'
    async def getVal():
        return await hmi.client.get(__class__.name + '.val')

    async def setVal(value):
        await hmi.client.set(__class__.name + '.val', value)

    async def onRelease():
        val = await __class__.getVal()
        print("page1.bt1 onRelease")
        if val == 1:
            await page0.j0.setVal(50)
        else:
            await page0.j0.setVal(0)

class bt2():
    name = 'page1.bt2'
    async def getVal():
        return await hmi.client.get(__class__.name + '.val')

    async def setVal(value):
        await hmi.client.set(__class__.name + '.val', value)

    async def onRelease():
        val = await __class__.getVal()
        print("page1.bt1 onRelease")
        if val == 1:
            await page0.j0.setVal(80)
        else:
            await page0.j0.setVal(0)

class bt3():
    name = 'page1.bt3'
    async def getVal():
        return await hmi.client.get(__class__.name + '.val')

    async def setVal(value):
        await hmi.client.set(__class__.name + '.val', value)

    async def onRelease():
        val = await __class__.getVal()
        print("page1.bt3 onRelease")
        if val == 1:
            await page0.j1.setVal(30)
        else:
            await page0.j1.setVal(0)

class bt4():
    name = 'page1.bt4'
    async def getVal():
        return await hmi.client.get(__class__.name + '.val')

    async def setVal(value):
        await hmi.client.set(__class__.name + '.val', value)

    async def onRelease():
        val = await __class__.getVal()
        print("page1.bt4 onRelease")
        if val == 1:
            await page0.j1.setVal(30)
        else:
            await page0.j1.setVal(0)

class bt5():
    name = 'page1.bt5'
    async def getVal():
        return await hmi.client.get(__class__.name + '.val')

    async def setVal(value):
        await hmi.client.set(__class__.name + '.val', value)

    async def onRelease():
        val = await __class__.getVal()
        print("page1.bt5 onRelease")
        if val == 1:
            await page0.j1.setVal(30)
        else:
            await page0.j1.setVal(0)