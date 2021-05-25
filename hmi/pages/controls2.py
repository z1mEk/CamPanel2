from hmi import methods
from general import helper

#region Properties
class ClassName(type, object):
    name = None

class ValProperty(ClassName):
    @property
    def val(self):
        return helper.RunAsync(methods.getProperty(self.name, 'val'))
        
    @val.setter
    def val(self, value):
        helper.RunAsync(methods.setProperty(self.name, 'val', value))

class TxtProperty(ClassName):
    @property
    def txt(self):
        return helper.RunAsync(methods.getProperty(self.name, 'txt'))
        
    @txt.setter
    def txt(self, value):
        helper.RunAsync(methods.setProperty(self.name, 'txt', value)) 

class ColourProperty(ClassName):
    @property
    def pco(self):
        return helper.RunAsync(methods.getProperty(self.name, 'pco'))
        
    @pco.setter
    def pco(self, value):
        helper.RunAsync(methods.setProperty(self.name, 'pco', value))

    @property
    def bco(self):
        return helper.RunAsync(methods.getProperty(self.name, 'bco'))
        
    @bco.setter
    def bco(self, value):
        helper.RunAsync(methods.setProperty(self.name, 'bco', value))   
#endregion     

#region Methods
class ControlMethods:
    @classmethod
    async def onTouch(self):
        pass
        
    @classmethod
    async def onRelease(self):
        pass
#endregion

#region MetaClass combine
class TButtonMeta(TxtProperty, ColourProperty, ControlMethods):
    pass
      
class TDualStateButtonMeta(ValProperty, TxtProperty, ColourProperty, ControlMethods):
    pass      

class TTextMeta(TxtProperty, ColourProperty, ControlMethods):
    pass 

class TScrollingTextMeta(TxtProperty, ColourProperty, ControlMethods):
    pass

class TNumberMeta(ValProperty, ColourProperty, ControlMethods):
    pass

class TXFloatMeta(ValProperty, ColourProperty, ControlMethods):
    pass

class TProgressBarMeta(ValProperty, ColourProperty, ControlMethods):
    pass

class TSliderMeta(ValProperty, ColourProperty, ControlMethods):
    pass

class TCheckBoxMeta(ValProperty, ColourProperty, ControlMethods):
    pass

class TRadioMeta(ValProperty, ColourProperty, ControlMethods):
    pass
#endregion

#region Global controlls class
class TButton(metaclass=TButtonMeta):
    pass

class TDualStateButton(metaclass=TDualStateButtonMeta):
    pass

class TText(metaclass=TTextMeta):
    pass

class TScrollingText(metaclass=TScrollingTextMeta):
    pass

class TNumber(metaclass=TNumberMeta):
    pass

class TXFloat(metaclass=TXFloatMeta):
    pass

class TProgressBar(metaclass=TProgressBarMeta):
    pass

class TSlider(metaclass=TSliderMeta):
    pass

class TCheckBox(metaclass=TCheckBoxMeta):
    pass

class TRadio(metaclass=TRadioMeta):
    pass
#endregion