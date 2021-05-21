from hmi import methods
from general import helper

#region Global controls
class ClassProperties(type):
    name = None
    
    @property
    def val(self):
        return helper.RunAsync(methods.getProperty(self.name, 'val'))
        
    @val.setter
    def val(self, value):
        helper.RunAsync(methods.setProperty(self.name, 'val', value))

    @property
    def txt(self):
        return helper.RunAsync(methods.getProperty(self.name, 'txt'))
        
    @txt.setter
    def txt(self, value):
        helper.RunAsync(methods.setProperty(self.name, 'txt', value))    
        
class TGlobal(object, metaclass=ClassProperties):   
    @classmethod
    async def onTouch(self):
        pass
        
    @classmethod
    async def onRelease(self):
        pass
#endregion

class TButton(TGlobal):
    pass

class TDualStateButton(TGlobal):
    pass

class TText(TGlobal):
    pass

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
