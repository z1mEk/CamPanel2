import os
import sys
from hmi import methods as hmiMethods
from general import methods

#region Base Control
class BaseControl(type, object):
    def __new__(cls, name, bases, dct):
        module = sys.modules[dct['__module__']]
        module_name = os.path.splitext(os.path.basename(module.__file__))[0]

        if module_name == "__init__":
            module_name = os.path.basename(os.path.dirname(module.__file__))

        base_class_name = bases[0].__name__ if bases else None

        dct['page'] = module_name
        dct['name'] = name
        dct['fullname'] = f"{module_name}.{name}"
        dct['type'] = base_class_name
        return super().__new__(cls, name, bases, dct)

    def _get_attr(self, attr):
        return methods.RunAsync(hmiMethods.getProperty(self.fullname, attr))

    def _set_attr(self, attr, value):
        methods.RunAsync(hmiMethods.setProperty(self.fullname, attr, value))

#endregion

#region Properties
class PropertyMixin(BaseControl):
    def __init__(self, attr_name):
        self._attr_name = attr_name

    @property
    def value(self):
        return self._get_attr(self._attr_name)

    @value.setter
    def value(self, value):
        self._set_attr(self._attr_name, value)

class ValProperty(PropertyMixin):
    def __init__(self):
        super().__init__('val')

class TxtProperty(PropertyMixin):
    def __init__(self):
        super().__init__('txt')

class FontProperty(PropertyMixin):
    def __init__(self):
        super().__init__('font')

class XcenProperty(PropertyMixin):
    def __init__(self):
        super().__init__('xcen')

class ColourPropertyPco(PropertyMixin):
    def __init__(self):
        super().__init__('pco')
		
class ColourPropertyBco(PropertyMixin):
    def __init__(self):
        super().__init__('bco')

#endregion

#region Methods
class ControlMethods:
    @classmethod
    async def on_touch(cls):
        pass

    @classmethod
    async def on_release(cls):
        pass

#endregion

#region MetaClass combine
class TButtonMeta(
    TxtProperty,
    ColourPropertyPco,
    ColourPropertyBco,
    FontProperty,
    ControlMethods
):
    pass

class TDualStateButtonMeta(
    ValProperty,
    TxtProperty,
    ColourPropertyPco,
    ColourPropertyBco,
    ControlMethods
):
    pass

class TTextMeta(
    TxtProperty,
    ColourProperty,
    ColourPropertyPco,
    ColourPropertyBco,
    XcenProperty,
    ControlMethods):
    pass

class TScrollingTextMeta(
    TxtProperty,
    ColourPropertyPco,
    ColourPropertyBco,
    FontProperty,
    ControlMethods
):
    pass

class TNumberMeta(
    ValProperty,
    ColourPropertyPco,
    ColourPropertyBco,
    FontProperty,
    ControlMethods
):
    pass

class TXFloatMeta(
    ValProperty,
    ColourPropertyPco,
    ColourPropertyBco,
    FontProperty,
    ControlMethods
):
    pass

class TProgressBarMeta(
    ValProperty,
    ColourPropertyPco,
    ColourPropertyBco,
    ControlMethods
):
    pass

class TSliderMeta(
    ValProperty,
    ColourPropertyPco,
    ColourPropertyBco,
    ControlMethods
):
    pass

class TCheckBoxMeta(
    ValProperty,
    ColourPropertyPco,
    ColourPropertyBco,
    ControlMethods
):
    pass

class TRadioMeta(
    ValProperty,
    ColourPropertyPco,
    ColourPropertyBco,
    ControlMethods
):
    pass

#endregion

#region Global control classes
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
