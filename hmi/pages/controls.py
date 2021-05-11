from hmi import hmi

class ClassProperties(type):
    name = None
    _val = None
    _txt = None
    
    @property
    def val(self):
        print("get", self.name, self._val)
        return self._val
        
    @val.setter
    def val(self, value):
        print("set", self.name, value)
        self._val = value
        
    @property
    def txt(self):
        print("get", self.name, self._txt)
        return self._txt
        
    @txt.setter
    def txt(self, value):
        print("set", self.name, value)
        self._txt = value 

class TGlobal(object, metaclass=ClassProperties):   
    @classmethod
    async def getVal(self):
        return await hmi.client.get(self.name + '.val')

    @classmethod
    async def setVal(self, value:int):
        await hmi.client.set(self.name + '.val', value) 

    @classmethod
    async def getTxt(self):
        return await hmi.client.get(self.name + '.txt')
        
    @classmethod
    async def setTxt(self, value:str):
        await hmi.client.set(self.name + '.txt', value)        

    @classmethod
    async def getFont(self):
        return await hmi.client.get(self.name + '.font')

    @classmethod
    async def setFont(self, value:int):
        await hmi.client.set(self.name + '.font', value) 

    @classmethod
    async def getBco(self):
        return await hmi.client.get(self.name + '.bco')

    @classmethod
    async def setBco(self, value:int):
        await hmi.client.set(self.name + '.bco', value) 

    @classmethod
    async def getPco(self):
        return await hmi.client.get(self.name + '.pco')

    @classmethod
    async def setPco(self, value:int):
        await hmi.client.set(self.name + '.pco', value)  

    @classmethod
    async def getXcen(self):
        return await hmi.client.get(self.name + '.xcen')

    @classmethod
    async def setXcen(self, value:int):
        await hmi.client.set(self.name + '.xcen', value)        

    @classmethod
    async def getYcen(self):
        return await hmi.client.get(self.name + '.xcen')

    @classmethod
    async def setYcen(self, value:int):
        await hmi.client.set(self.name + '.xcen', value)    

    @classmethod
    async def getIsbr(self):
        return await hmi.client.get(self.name + '.isb')

    @classmethod
    async def setIsb(self, value:int):
        await hmi.client.set(self.name + '.isb', value)   

    @classmethod
    async def getSpax(self):
        return await hmi.client.get(self.name + '.spax')

    @classmethod
    async def setSpax(self, value:int):
        await hmi.client.set(self.name + '.spax', value)     

    @classmethod
    async def getSpay(self):
        return await hmi.client.get(self.name + '.spay')

    @classmethod
    async def setSpay(self, value:int):
        await hmi.client.set(self.name + '.spay', value)                                 

    @classmethod
    async def onTouch(self):
        pass
        
    @classmethod
    async def onRelease(self):
        pass

class TButton(TGlobal):
    pass

class TDualStateButton(TGlobal):
    pass

class TText(TGlobal):
    @classmethod
    async def setPw(self, value:int):
        await hmi.client.set(self.name + '.pw', value)        

    @classmethod
    async def getPw(self) -> int:
        return await hmi.client.get(self.name + '.pw')

class TScrollingText(TGlobal):
    pass

class TNumber(TGlobal):
    pass

class TXFloat(TGlobal):
    pass

class TProgressBar(TGlobal):
    pass

class TSlider(TGlobal):
    pass

class TCheckBox(TGlobal):
    pass

class TRadio(TGlobal):
    pass
