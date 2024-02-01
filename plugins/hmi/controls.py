import os, sys
from plugins.hmi import methods as hmiMethods
from general import methods as generalMethods
from general.logger import logging
import nest_asyncio
from nest_asyncio import asyncio
nest_asyncio.apply()

#region Base Control
class BaseControl(type, object):

    #name = __name__

    def __new__(cls, name, bases, dct):
        module = sys.modules[dct['__module__']]
        module_name = os.path.splitext(os.path.basename(module.__file__))[0]
        base_class_name = bases[0].__name__ if bases else None

        dct["page"] = module_name
        dct["fullname"] = f"{module_name}.{name}"
        dct["type_name"] = base_class_name

        return super().__new__(cls, name, bases, dct)

    def getAtrr(self, attr):
        return asyncio.run(hmiMethods.getProperty(self.fullname, attr))

    def setAttr(self, attr, value):
        asyncio.run(hmiMethods.setProperty(self.fullname, attr, value))

    @property
    def type(self):
        return self.getAtrr('type')
    
    @property
    def id(self):
        return self.getAtrr('id')
    
    @property
    def objname(self):
        return self.getAtrr('objname')
    
    @property
    def vscope(self):
        return self.getAtrr('vscope')
    
#endregion
        
#region Base Page
class BasePage(type, object):

    def __new__(cls, name, bases, dct):
        module = sys.modules[dct['__module__']]
        module_name = os.path.splitext(os.path.basename(module.__file__))[0]
        base_class_name = bases[0].__name__ if bases else None

        dct["name"] = module_name
        dct["fullname"] = module_name
        dct["type_name"] = base_class_name

        return super().__new__(cls, name, bases, dct)    

    def getAtrr(self, attr):
        logging.info(f"fullname = {self.name}")
        return asyncio.run(hmiMethods.getProperty(self.name, attr))

    def setAttr(self, attr, value):
        asyncio.run(hmiMethods.setProperty(self.name, attr, value))

#endregion
        
#region Page Properies
class PageProperty(BasePage):
    @property
    def type(self):
        return self.getAtrr('type')
    
    @property
    def id(self):
        return self.getAtrr('id')
    
    @property
    def vscope(self):
        return self.getAtrr('vscope')    
    
    @property
    def sta(self):
        return self.getAtrr('sta')    

    @property
    def bco(self):
        return self.getAtrr('bco')
    
    @property
    def pic(self):
        return self.getAtrr('pic')
            
    @bco.setter
    def bco(self, value:int):
        self.setAttr('bco', value)  

    @property
    def x(self):
        return self.getAtrr('x')      

    @property
    def y(self):
        return self.getAtrr('y')     

    @property
    def w(self):
        return self.getAtrr('w')      
    
    @property
    def h(self):
        return self.getAtrr('h')             
#endregion

#region Properties
class StaProperty(BaseControl):
    @property
    def sta(self):
        return self.getAtrr('sta')
            
class ValProperty(BaseControl):
    @property
    def val(self):
        return self.getAtrr('val')
        
    @val.setter
    def val(self, value:int):
        self.setAttr('val', value)

class TxtProperty(BaseControl):
    @property
    def txt(self):
        return self.getAtrr('txt')
    
    @property
    def txt_maxl(self):
        return self.getAtrr('txt_maxl')
        
    @txt.setter
    def txt(self, value:txt):
        self.setAttr('txt', value)      

class FontProperty(BaseControl):
    @property
    def font(self):
        return self.getAtrr('font')
        
    @font.setter
    def font(self, value:int):
        self.setAttr('font', value)

class XYcenProperty(BaseControl):
    @property
    def xcen(self):
        return self.getAtrr('xcen')
        
    @xcen.setter
    def xcen(self, value:int):
        self.setAttr('xcen', value)

    @property
    def ycen(self):
        return self.getAtrr('ycen')
        
    @ycen.setter
    def ycen(self, value:int):
        self.setAttr('ycen', value)       

class PcoProperty(BaseControl):
    @property
    def pco(self):
        return self.getAtrr('pco')
        
    @pco.setter
    def pco(self, value:int):
        self.setAttr('pco', value)

class BcoProperty(BaseControl):
    @property
    def bco(self):
        return self.getAtrr('bco')
        
    @bco.setter
    def bco(self, value:int):
        self.setAttr('bco', value)

class Pco2Property(BaseControl):
    @property
    def pco2(self):
        return self.getAtrr('pco2')
        
    @pco2.setter
    def pco2(self, value:int):
        self.setAttr('pco2', value)

class Bco2Property(BaseControl):
    @property
    def bco2(self):
        return self.getAtrr('bco2')
        
    @bco2.setter
    def bco2(self, value:int):
        self.setAttr('bco2', value)        

class PicProperty(BaseControl):
    @property
    def pic(self):
        return self.getAtrr('pic')
        
    @pic.setter
    def pic(self, value:int):
        self.setAttr('pic', value)

class PiccProperty(BaseControl):
    @property
    def picc(self):
        return self.getAtrr('picc')
        
    @picc.setter
    def picc(self, value:int):
        self.setAttr('picc', value)        

class Pic2Property(BaseControl):
    @property
    def pic2(self):
        return self.getAtrr('pic')
        
    @pic2.setter
    def pic2(self, value:int):
        self.setAttr('pic2', value)   

class Picc2Property(BaseControl):
    @property
    def picc2(self):
        return self.getAtrr('picc2')
        
    @picc2.setter
    def picc2(self, value:int):
        self.setAttr('picc2', value)

class BpicProperty(BaseControl):
    @property
    def bpic(self):
        return self.getAtrr('pbic')
        
    @bpic.setter
    def bpic(self, value:int):
        self.setAttr('bpic', value)        

class PpicProperty(BaseControl):
    @property
    def ppic(self):
        return self.getAtrr('pbic')
        
    @ppic.setter
    def ppic(self, value:int):
        self.setAttr('ppic', value)                

class PwProperty(BaseControl):
    @property
    def pw(self):
        return self.getAtrr('pw')
        
    @pw.setter
    def pw(self, value:int):
        self.setAttr('pw', value)     

class IsBrProperty(BaseControl):
    @property
    def isbr(self):
        return self.getAtrr('isbr')
        
    @isbr.setter
    def isbr(self, value:int):
        self.setAttr('isbr', value)           

class SpaXYProperty(BaseControl):
    @property
    def spax(self):
        return self.getAtrr('spax')
    
    @property
    def spay(self):
        return self.getAtrr('spay') 
    
class XYWHProperty(BaseControl):
    @property
    def x(self):
        return self.getAtrr('x')      

    @property
    def y(self):
        return self.getAtrr('y')     

    @property
    def w(self):
        return self.getAtrr('w')      
    
    @property
    def h(self):
        return self.getAtrr('h')     

class StyleProperty(BaseControl):
    @property
    def style(self):
        return self.getAtrr('style')
    
class TimProperty(BaseControl):
    @property
    def tim(self):
        return self.getAtrr('tim')
        
    @tim.setter
    def tim(self, value:int):
        self.setAttr('tim', value)

class EnProperty(BaseControl):
    @property
    def en(self):
        return self.getAtrr('en')
        
    @en.setter
    def en(self, value:int):
        self.setAttr('en', value)         
    
class DirProperty(BaseControl):
    @property
    def dir(self):
        return self.getAtrr('dir')
        
    @dir.setter
    def dir(self, value:int):
        self.setAttr('dir', value)      

class DisProperty(BaseControl):
    @property
    def dis(self):
        return self.getAtrr('dis')
        
    @dis.setter
    def dis(self, value:int):
        self.setAttr('dis', value)        

class LenthProperty(BaseControl):
    @property
    def lenth(self):
        return self.getAtrr('lenth')
        
    @lenth.setter
    def lenth(self, value:int):
        self.setAttr('lenth', value) 
 
class FormatProperty(BaseControl):
    @property
    def format(self):
        return self.getAtrr('format')
        
    @format.setter
    def format(self, value:int):
        self.setAttr('format', value) 

class Ws0Property(BaseControl):
    @property
    def ws0(self):
        return self.getAtrr('ws0')
        
    @ws0.setter
    def ws0(self, value:int):
        self.setAttr('ws0', value) 

class Ws1Property(BaseControl):
    @property
    def ws1(self):
        return self.getAtrr('ws1')
        
    @ws1.setter
    def ws1(self, value:int):
        self.setAttr('ws1', value)         

class DezProperty(BaseControl):
    @property
    def dez(self):
        return self.getAtrr('dez')
        
    @dez.setter
    def dez(self, value:int):
        self.setAttr('dez', value) 

class WidProperty(BaseControl):
    @property
    def wid(self):
        return self.getAtrr('wid')
        
    @wid.setter
    def wid(self, value:int):
        self.setAttr('wid', value) 

class ChProperty(BaseControl):
    @property
    def ch(self):
        return self.getAtrr('ch')
        
    @ch.setter
    def ch(self, value:int):
        self.setAttr('ch', value) 

class GdcProperty(BaseControl):
    @property
    def gdc(self):
        return self.getAtrr('gdc')
        
    @gdc.setter
    def gdc(self, value:int):
        self.setAttr('gdc', value) 

class GdwProperty(BaseControl):
    @property
    def gdw(self):
        return self.getAtrr('gdw')
        
    @gdw.setter
    def gdw(self, value:int):
        self.setAttr('gdw', value) 

class GdhProperty(BaseControl):
    @property
    def gdh(self):
        return self.getAtrr('gdh')
        
    @gdh.setter
    def gdh(self, value:int):
        self.setAttr('gdh', value) 

class Pco0Property(BaseControl):
    @property
    def pco0(self):
        return self.getAtrr('pco0')
        
    @pco0.setter
    def pco0(self, value:int):
        self.setAttr('pco0', value) 

class ModeProperty(BaseControl):
    @property
    def mode(self):
        return self.getAtrr('mode')
        
    @mode.setter
    def mode(self, value:int):
        self.setAttr('mode', value)     

class PstaProperty(BaseControl):
    @property
    def psta(self):
        return self.getAtrr('psta')
        
    @psta.setter
    def psta(self, value:int):
        self.setAttr('psta', value)  

class HigProperty(BaseControl):
    @property
    def hig(self):
        return self.getAtrr('hig')
        
    @hig.setter
    def hig(self, value:int):
        self.setAttr('hig', value)      

class MaxvalProperty(BaseControl):
    @property
    def maxval(self):
        return self.getAtrr('maxval')
        
    @maxval.setter
    def maxval(self, value:int):
        self.setAttr('maxval', value)     

class MinvalProperty(BaseControl):
    @property
    def minval(self):
        return self.getAtrr('minval')
        
    @minval.setter
    def minval(self, value:int):
        self.setAttr('minval', value)                               

class Bco1Property(BaseControl):
    @property
    def bco1(self):
        return self.getAtrr('bco1')
        
    @bco1.setter
    def bco1(self, value:int):
        self.setAttr('bco1', value)  

class Pic1Property(BaseControl):
    @property
    def pic1(self):
        return self.getAtrr('pic1')
        
    @pic1.setter
    def pic1(self, value:int):
        self.setAttr('pic1', value)          

class Picc1Property(BaseControl):
    @property
    def picc1(self):
        return self.getAtrr('picc1')
        
    @picc1.setter
    def picc1(self, value:int):
        self.setAttr('picc1', value) 

#endregion     

#region Methods
class ControlMethods:
    @classmethod
    async def onTouch(cls):
        pass
        
    @classmethod
    async def onRelease(cls):
        pass

class PageControlMethods:   
    @classmethod
    async def onShow(cls):
        pass

    @classmethod
    async def onExit(cls):
        pass

    @classmethod
    async def onTouch(cls):
        pass
        
    @classmethod
    async def onRelease(cls):
        pass

#endregion

#region MetaClass combine
class TPageMeta(
            PageProperty,
            PageControlMethods
        ):
    pass

#style
class TTextMeta(
            TxtProperty,
            StaProperty,
            StyleProperty,
            FontProperty,
            PcoProperty,
            BcoProperty,
            PicProperty,
            PiccProperty,
            XYcenProperty,
            PwProperty,
            IsBrProperty,
            XYWHProperty,            
            ControlMethods
        ):
    pass 

class TScrollingTextMeta(
            TxtProperty,
            StaProperty,
            StyleProperty,
            DirProperty,
            DisProperty,
            TimProperty,
            EnProperty,
            FontProperty,
            PcoProperty,
            BcoProperty,
            PicProperty,
            PiccProperty,
            XYcenProperty,
            PwProperty,
            IsBrProperty,
            XYWHProperty,            
            ControlMethods
        ):
    pass

class TNumberMeta(
            ValProperty,
            StaProperty,
            StyleProperty,
            FontProperty,
            LenthProperty,
            PcoProperty,
            BcoProperty,
            PicProperty,
            PiccProperty,
            XYcenProperty,
            PwProperty,
            IsBrProperty,
            XYWHProperty,            
            ControlMethods
        ):
    pass

class TXFloatMeta(
            ValProperty,
            StaProperty,
            StyleProperty,
            FontProperty,
            Ws0Property,
            Ws1Property,
            PcoProperty,
            BcoProperty,
            PicProperty,
            PiccProperty,
            XYcenProperty,
            PwProperty,
            SpaXYProperty,
            IsBrProperty,
            XYWHProperty,            
            ControlMethods
        ):
    pass

class TButtonMeta(
            TxtProperty,
            StaProperty,
            StyleProperty,
            PcoProperty,
            Pco2Property,
            BcoProperty,
            Bco2Property,
            FontProperty,
            PicProperty,
            Pic2Property,
            PiccProperty,
            Picc2Property,
            XYcenProperty,
            SpaXYProperty,
            IsBrProperty,
            XYWHProperty,
            ControlMethods
        ):
    pass

class TProgressBarMeta(
            StaProperty,
            ValProperty,
            DezProperty,
            PcoProperty,
            BcoProperty,
            BpicProperty,
            PpicProperty,
            XYWHProperty,
            ControlMethods
        ):
    pass

class TPictureMeta(
            PicProperty,
            XYWHProperty,
            ControlMethods
        ):
    pass

class TCropMeta(
            PiccProperty,
            XYWHProperty,
            ControlMethods            
        ):
    pass

class THotspotMeta(
            XYWHProperty,
            ControlMethods  
        ):
    pass

class TTouchCapMeta(
            BaseControl,
            ControlMethods
        ):
    pass

class TGaugeMeta(
            StaProperty,
            BcoProperty,
            ValProperty,
            WidProperty,
            PcoProperty,
            PicProperty,
            PiccProperty,
            XYWHProperty,
            ControlMethods             
        ):
    pass

class TWaveformMeta(
            StaProperty,
            XYWHProperty,
            DirProperty,
            ChProperty,
            GdcProperty,
            GdwProperty,
            GdhProperty,
            Pco0Property,
            DisProperty,
            ControlMethods             
        ):
    pass
      
class TDualStateButtonMeta(
            ValProperty,
            TxtProperty,
            StaProperty,
            StyleProperty,
            PcoProperty,
            Pco2Property,
            BcoProperty,
            Bco2Property,
            FontProperty,
            PicProperty,
            Pic2Property,
            PiccProperty,
            Picc2Property,
            XYcenProperty,
            SpaXYProperty,
            IsBrProperty,
            XYWHProperty,
            ControlMethods
        ):
    pass      

class TSliderMeta(
            ValProperty,
            PcoProperty,
            BcoProperty,
            ModeProperty,
            PstaProperty,
            WidProperty,
            HigProperty,
            MaxvalProperty,
            MinvalProperty,
            Bco1Property,
            Pic1Property,
            Picc1Property,
            XYWHProperty,
            ControlMethods
        ):
    pass

class TTimerMeta(
            TimProperty,
            EnProperty
        ):
    pass

class TVariableMeta(
            StaProperty,
            ValProperty,
            TxtProperty
        ):
    pass

class TCheckBoxMeta(
            ValProperty,
            PcoProperty,
            BcoProperty,
            XYWHProperty,
            ControlMethods
        ):
    pass

class TRadioMeta(
            ValProperty,
            PcoProperty,
            BcoProperty,
            XYWHProperty,
            ControlMethods
        ):
    pass

class TQRcodeMeta(
            StaProperty,
            TxtProperty,
            PcoProperty,
            BcoProperty,
            PicProperty,
            XYWHProperty,
            ControlMethods
        ):
    pass
#endregion

#region Global controll classes
class TPage(metaclass=TPageMeta):
    pass

class TText(metaclass=TTextMeta):
    pass

class TScrollingText(metaclass=TScrollingTextMeta):
    pass

class TNumber(metaclass=TNumberMeta):
    pass

class TXFloat(metaclass=TXFloatMeta):
    pass

class TButton(metaclass=TButtonMeta):
    pass

class TProgressBar(metaclass=TProgressBarMeta):
    pass

class TPicture(metaclass=TPictureMeta):
    pass

class TCrop(metaclass=TCropMeta):
    pass

class THotspot(metaclass=THotspotMeta):
    pass

class TTouchCap(metaclass=TTouchCapMeta):
    pass

class TGauge(metaclass=TGaugeMeta):
    pass

class TWaveform(metaclass=TWaveformMeta):
    pass

class TSlider(metaclass=TSliderMeta):
    pass

class TTimer(metaclass=TTimerMeta): 
    pass

class TVariable(metaclass=TVariableMeta):
    pass

class TDualStateButton(metaclass=TDualStateButtonMeta):
    pass

class TCheckBox(metaclass=TCheckBoxMeta):
    pass

class TRadio(metaclass=TRadioMeta):
    pass

class TQRcode(metaclass=TQRcodeMeta):
    pass

#endregion
