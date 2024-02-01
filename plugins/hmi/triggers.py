from plugins.hmi.pages.mainPage import mainPage
from plugins.hmi.pages.dieselHeatPage import dieselHeatPage
from plugins.hmi.pages.solarWaterPage import solarWaterPage
from plugins.hmi.pages.settingsPage import settingsPage
from plugins.hmi.pages.dialogInfoPage import dialogInfoPage

### definition of call name for nextion's components. "call_back" ###
components_touch_event = [
        #mainPage
        {"page_id": 0, "component_id": 0, "touch_event": 0, "call_back": mainPage.onRelease},
        {"page_id": 0, "component_id": 0, "touch_event": 1, "call_back": mainPage.onTouch},
        {"page_id": 0, "component_id": 0, "touch_event": 2, "call_back": mainPage.onShow},
        {"page_id": 0, "component_id": 0, "touch_event": 3, "call_back": mainPage.onExit},
        {"page_id": 0, "component_id": 2, "touch_event": 1, "call_back": mainPage.jRSOC.onTouch},
        {"page_id": 0, "component_id": 5, "touch_event": 0, "call_back": mainPage.btWaterPump.onRelease},
        {"page_id": 0, "component_id": 6, "touch_event": 0, "call_back": mainPage.btACInverter.onRelease},
        {"page_id": 0, "component_id": 7, "touch_event": 0, "call_back": mainPage.btHeater.onRelease},
        {"page_id": 0, "component_id": 8, "touch_event": 0, "call_back": mainPage.btBoiler.onRelease},
        #solarWaterPage
        {"page_id": 1, "component_id": 0, "touch_event": 0, "call_back": solarWaterPage.onRelease},
        {"page_id": 1, "component_id": 0, "touch_event": 1, "call_back": solarWaterPage.onTouch},
        {"page_id": 1, "component_id": 0, "touch_event": 2, "call_back": solarWaterPage.onShow},
        {"page_id": 1, "component_id": 0, "touch_event": 3, "call_back": solarWaterPage.onExit},
        #dieselHeatPage
        {"page_id": 2, "component_id": 0, "touch_event": 0, "call_back": dieselHeatPage.onRelease},
        {"page_id": 2, "component_id": 0, "touch_event": 1, "call_back": dieselHeatPage.onTouch},
        {"page_id": 2, "component_id": 0, "touch_event": 2, "call_back": dieselHeatPage.onShow},
        {"page_id": 2, "component_id": 0, "touch_event": 3, "call_back": dieselHeatPage.onExit},
        {"page_id": 2, "component_id": 8, "touch_event": 0, "call_back": dieselHeatPage.btHeater.onRelease},
        {"page_id": 2, "component_id": 9, "touch_event": 1, "call_back": dieselHeatPage.bUp.onTouch},
        {"page_id": 2, "component_id": 10, "touch_event": 1, "call_back": dieselHeatPage.bDown.onTouch},
        {"page_id": 2, "component_id": 11, "touch_event": 0, "call_back": dieselHeatPage.btThermostat.onRelease},
        #settingsPage
        {"page_id": 3, "component_id": 0, "touch_event": 0, "call_back": settingsPage.onRelease},
        {"page_id": 3, "component_id": 0, "touch_event": 1, "call_back": settingsPage.onTouch},
        {"page_id": 3, "component_id": 0, "touch_event": 2, "call_back": settingsPage.onShow},
        {"page_id": 3, "component_id": 0, "touch_event": 3, "call_back": settingsPage.onExit},
        #dialogInfoPAge
        {"page_id": 4, "component_id": 3, "touch_event": 1, "call_back": dialogInfoPage.bOK.onTouch},
    ]