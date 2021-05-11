import asyncio

class helper:
    def RunAsync(proc):
        return asyncio.get_event_loop().run_until_complete(proc)

class test1:
    async def getVal():
        print('getVal')
        return 33
        
    async def setVal(value):
        print('setVal')

class ClassProperties(type):
    name = None
    
    @property
    def val(self):
        return helper.RunAsync(test1.getVal())
        
    @val.setter
    def val(self, value):
        helper.RunAsync(test1.setVal(value))        
        
    @property
    def txt(self):
        return self._txt
        
    @txt.setter
    def txt(self, value):
        self._txt = value    

class Test(object, metaclass=ClassProperties):
    pass

Test.val = 28
print(Test.val)
