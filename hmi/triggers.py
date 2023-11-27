# import importlib
# from hmi.pages import *
# import os


# def getComponentsTouchEvent():
#     cte = []
#     pages_directory = "./hmi/pages"
#     module_names = plugin_files = [f[:-3] for f in os.listdir(pages_directory) if f.endswith(".py") and not f.startswith("__")]
#     # Iteruj przez moduły
#     for module_name in module_names:
#         # Importuj moduł dynamicznie
#         module = importlib.import_module(f"hmi.pages.{module_name}")

#             # Sprawdź klasy w module
#         for class_name in dir(module):
#             cls = getattr(module, class_name)

#             # Sprawdź, czy klasa zawiera metody onTouch i onRelease
#             if hasattr(cls, 'onTouch'):
#                 cte.append({
#                     "page_id": cls.page_id,
#                     "component_id": cls.component_id,
#                     "touch_event": 1,
#                     "call_back": cls.onTouch
#                 })

#             if hasattr(cls, 'onRelease'):
#                 cte.append({
#                     "page_id": cls.page_id,
#                     "component_id": cls.component_id,
#                     "touch_event": 0,
#                     "call_back": cls.onRelease
#                 })
#     return cte

# # Inicjalizuj listę components_touch_event
# components_touch_event = getComponentsTouchEvent()

from hmi.pages import page0, page1

### definition of call name for nextion's components. "call_back" ###
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