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

#         # Sprawdź klasy w module
#         for class_name in dir(module):
#             cls = getattr(module, class_name)

#             # Sprawdź, czy klasa zawiera metody onTouch i onRelease
#             if hasattr(cls, 'onTouch'):
#                 cte.append({
#                     "page_id": cls.page_id,
#                     "component_id": cls.id,
#                     "touch_event": 1,
#                     "call_back": cls.onTouch
#                 })

#             if hasattr(cls, 'onRelease'):
#                 cte.append({
#                     "page_id": cls.page_id,
#                     "component_id": cls.id,
#                     "touch_event": 0,
#                     "call_back": cls.onRelease
#                 })
#     return cte

# # Inicjalizuj listę components_touch_event
#if components_touch_event == None:
#   components_touch_event = getComponentsTouchEvent()

from plugins.hmi.pages.MainPage import MainPage

### definition of call name for nextion's components. "call_back" ###
components_touch_event = [
        #MainPage
        {"page_id": 0, "component_id": 5, "touch_event": 0, "call_back": MainPage.btWaterPump.onRelease},
        {"page_id": 0, "component_id": 6, "touch_event": 0, "call_back": MainPage.btACInverter.onRelease},
        {"page_id": 0, "component_id": 7, "touch_event": 0, "call_back": MainPage.btHeater.onRelease},
        {"page_id": 0, "component_id": 8, "touch_event": 0, "call_back": MainPage.btBoiler.onRelease},
    ]