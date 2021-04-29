from hmi import hmi

async def Show():
    await hmi.client.command('page 0')

class b0:
    name = 'page0.b0'

    async def onTouch():
        print("page0.b0 onTouch")

class j0:
    name = 'page0.j0'
    async def getVal():
        return await hmi.client.get(__class__.name + '.val')

    async def setVal(value:int):
        oldValue = await __class__.getVal()
        await hmi.client.set(__class__.name + '.val', value)
        await __class__.onChange(oldValue, value)

    async def onChange(oldValue:int, newValue:int):
        await t2.setTxt('{percent}%'.format(percent=newValue))

class j1:
    name = 'page0.j1'
    async def getVal():
        return await hmi.client.get(__class__.name + '.val')

    async def setVal(value:int):
        oldValue = await __class__.getVal()
        await hmi.client.set(__class__.name + '.val', value)
        await __class__.onChange(oldValue, value)

    async def onChange(oldValue:int, newValue:int):
        await t3.setTxt('{percent}%'.format(percent=newValue))

class t2:
    name = 'page0.t2'
    async def getTxt():
        return await hmi.client.get(__class__.name + '.txt')
        
    async def setTxt(value:str):
        await hmi.client.set(__class__.name + '.txt', value)

class t3:
    name = 'page0.t3'
    async def getTxt():
        return await hmi.client.get(__class__.name + '.txt')
        
    async def setTxt(value:str):
        await hmi.client.set(__class__.name + '.txt', value)

class t4:
    name = 'page0.t4'
    async def getTxt():
        return await hmi.client.get(__class__.name + '.txt')
        
    async def setTxt(value:str):
        await hmi.client.set(__class__.name + '.txt', value)

    async def onTouch():
        print("page0.t4 onTouch")
        await __class__.setTxt("13.2")
        await t6.setTxt("V")   

class t5:
    name = 'page0.t5'
    async def getTxt():
        return await hmi.client.get(__class__.name + '.txt')
        
    async def setTxt(value:str):
        await hmi.client.set(__class__.name + '.txt', value)

    async def onTouch():
        print("page0.t5 onTouch")
        await __class__.setTxt("12.8")
        await t7.setTxt("V")  

class t6:
    name = 'page0.t6'
    async def getTxt():
        return await hmi.client.get(__class__.name + '.txt')
        
    async def setTxt(value:str):
        await hmi.client.set(__class__.name + '.txt', value)

class t7: 
    name = 'page0.t7'
    async def getTxt():
        return await hmi.client.get(__class__.name + '.txt')
        
    async def setTxt(value:str):
        await hmi.client.set(__class__.name + '.txt', value)  