from plugins.hmi.pages.MainPage import MainPage

### definition of call name for nextion's components. "call_back" ###
components_touch_event = [
        #MainPage
        {"page_id": 0, "component_id": 0, "touch_event": 0, "call_back": MainPage.onRelease},
        {"page_id": 0, "component_id": 0, "touch_event": 1, "call_back": MainPage.onTouch},
        {"page_id": 0, "component_id": 5, "touch_event": 0, "call_back": MainPage.btWaterPump.onRelease},
        {"page_id": 0, "component_id": 6, "touch_event": 0, "call_back": MainPage.btACInverter.onRelease},
        {"page_id": 0, "component_id": 7, "touch_event": 0, "call_back": MainPage.btHeater.onRelease},
        {"page_id": 0, "component_id": 8, "touch_event": 0, "call_back": MainPage.btBoiler.onRelease},
    ]