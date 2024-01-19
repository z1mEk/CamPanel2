import nest_asyncio
nest_asyncio.apply()
from general.logger import logging
import subprocess

def RestartCamPanel():
    subprocess.run(["sudo", "systemctl", "restart", "CamPanel.service"])

def RestartSystem():
    subprocess.run(["sudo", "restart"])
