import nest_asyncio
from nest_asyncio import asyncio
nest_asyncio.apply()
from plugins.hmi.controls import TPage, TText, TDualStateButton, TNumber
from general.logger import logging

class settingsPage(TPage):
    pass