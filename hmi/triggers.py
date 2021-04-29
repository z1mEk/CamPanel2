from hmi.pages import page0, page1

### definition of call name for nextion's components. "call_back" procedure must by exists in hmi.pages.page0... ###
components_touch_event = [
        #page0
        {"page_id": 0, "component_id": 9, "touch_event": 1, "call_back": page0.b0.onTouch},
        {"page_id": 0, "component_id": 5, "touch_event": 1, "call_back": page0.t4.onTouch},
        {"page_id": 0, "component_id": 6, "touch_event": 1, "call_back": page0.t5.onTouch},

        #page1
        {"page_id": 1, "component_id": 1, "touch_event": 1, "call_back": page1.b0.onTouch},
        {"page_id": 1, "component_id": 2, "touch_event": 0, "call_back": page1.bt0.onRelease},
        {"page_id": 1, "component_id": 3, "touch_event": 0, "call_back": page1.bt1.onRelease},
        {"page_id": 1, "component_id": 4, "touch_event": 0, "call_back": page1.bt2.onRelease},
        {"page_id": 1, "component_id": 5, "touch_event": 0, "call_back": page1.bt3.onRelease},
        {"page_id": 1, "component_id": 6, "touch_event": 0, "call_back": page1.bt4.onRelease},
        {"page_id": 1, "component_id": 7, "touch_event": 0, "call_back": page1.bt5.onRelease}
    ]