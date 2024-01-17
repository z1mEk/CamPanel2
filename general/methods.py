import nest_asyncio
nest_asyncio.apply()
from general.logger import logging
import subprocess

def RunAsync(proc):
    event_loop = nest_asyncio.asyncio.get_event_loop()
    ret = event_loop.run_until_complete(proc)
    logging.debug(f"RunAsync({proc}) -> {ret}")
    return ret

def RestartCamPanel():
    subprocess.run(["sudo", "systemctl", "restart", "CamPanel.service"])

def RestartSystem():
    subprocess.run(["sudo", "restart"])
