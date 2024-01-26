from plugins.hmi.pages.mainPage import mainPage
#from plugins.hmi.pages.dieselHeaterPage import dieselHeatPage

### definition of call name for nextion's components. "call_back" ###
components_touch_event = [
        #mainPage
        {"page_id": 0, "component_id": 0, "touch_event": 0, "call_back": mainPage.onRelease},
        {"page_id": 0, "component_id": 0, "touch_event": 1, "call_back": mainPage.onTouch},
        {"page_id": 0, "component_id": 5, "touch_event": 0, "call_back": mainPage.btWaterPump.onRelease},
        {"page_id": 0, "component_id": 6, "touch_event": 0, "call_back": mainPage.btACInverter.onRelease},
        {"page_id": 0, "component_id": 7, "touch_event": 0, "call_back": mainPage.btHeater.onRelease},
        {"page_id": 0, "component_id": 8, "touch_event": 0, "call_back": mainPage.btBoiler.onRelease},

        #{"page_id": 2, "component_id": 8, "touch_event": 0, "call_back": mainPage.btBoiler.onRelease},
    ]