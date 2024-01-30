from plugins.hmi.pages.mainPage import mainPage
from plugins.hmi.pages.dieselHeatPage import dieselHeatPage

### definition of call name for nextion's components. "call_back" ###
components_touch_event = [
        #mainPage
        {"page_id": 0, "component_id": 5, "touch_event": 0, "call_back": mainPage.btWaterPump.onRelease},
        {"page_id": 0, "component_id": 6, "touch_event": 0, "call_back": mainPage.btACInverter.onRelease},
        {"page_id": 0, "component_id": 7, "touch_event": 0, "call_back": mainPage.btHeater.onRelease},
        {"page_id": 0, "component_id": 8, "touch_event": 0, "call_back": mainPage.btBoiler.onRelease},
        
        #dieselHeatPage
        {"page_id": 2, "component_id": 8, "touch_event": 0, "call_back": dieselHeatPage.btHeater.onRelease},
        {"page_id": 2, "component_id": 9, "touch_event": 1, "call_back": dieselHeatPage.bUp.onTouch},
        {"page_id": 2, "component_id": 10, "touch_event": 1, "call_back": dieselHeatPage.bDown.onTouch},
        {"page_id": 2, "component_id": 11, "touch_event": 0, "call_back": dieselHeatPage.btThermostat.onRelease},
    ]