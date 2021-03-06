from hmi import methods as hmiMethods
from general import methods

#region Properties
class BaseControl(type, object):
    name = None

    def _getAtrr(self, attr):
        return methods.RunAsync(hmiMethods.getProperty(self.name, attr))

    def _setAttr(self, attr, value):
        methods.RunAsync(hmiMethods.setProperty(self.name, attr, value))

class ValProperty(BaseControl):
    @property
    def val(self):
        return self._getAtrr('val')
        
    @val.setter
    def val(self, value:int):
        self._setAttr('val', value)

class TxtProperty(BaseControl):
    @property
    def txt(self):
        return self._getAtrr('txt')
        
    @txt.setter
    def txt(self, value:txt):
        self._setAttr('txt', value)

class FontProperty(BaseControl):
    @property
    def font(self):
        return self._getAtrr('font')
        
    @font.setter
    def font(self, value:int):
        self._setAttr('font', value)

class XcenProperty(BaseControl):
    @property
    def xcen(self):
        return self._getAtrr('xcen')
        
    @xcen.setter
    def xcen(self, value:int):
        self._setAttr('xcen', value)

class ColourProperty(BaseControl):
    @property
    def pco(self):
        return self._getAtrr('pco')
        
    @pco.setter
    def pco(self, value:int):
        self._setAttr('pco', value)

    @property
    def bco(self):
        return self._getAtrr('bco')
        
    @bco.setter
    def bco(self, value:int):
        self._setAttr('bco', value)
#endregion     

#region Methods
class ControlMethods:
    @classmethod
    async def onTouch(cls):
        pass
        
    @classmethod
    async def onRelease(cls):
        pass
#endregion

#region MetaClass combine
class TButtonMeta(
            TxtProperty,
            ColourProperty,
            FontProperty,
            ControlMethods
        ):
    pass
      
class TDualStateButtonMeta(
            ValProperty,
            TxtProperty,
            ColourProperty,
            ControlMethods
        ):
    pass      

class TTextMeta(
            TxtProperty,
            ColourProperty,
            FontProperty,
            XcenProperty,
            ControlMethods):
    pass 

class TScrollingTextMeta(
            TxtProperty,
            ColourProperty,
            FontProperty,
            ControlMethods
        ):
    pass

class TNumberMeta(
            ValProperty,
            ColourProperty,
            FontProperty,
            ControlMethods
        ):
    pass

class TXFloatMeta(
            ValProperty,
            ColourProperty,
            FontProperty,
            ControlMethods
        ):
    pass

class TProgressBarMeta(
            ValProperty,
            ColourProperty,
            ControlMethods
        ):
    pass

class TSliderMeta(
            ValProperty,
            ColourProperty,
            ControlMethods
        ):
    pass

class TCheckBoxMeta(
            ValProperty,
            ColourProperty,
            ControlMethods
        ):
    pass

class TRadioMeta(
            ValProperty,
            ColourProperty,
            ControlMethods
        ):
    pass
#endregion

#region Global controll classes
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