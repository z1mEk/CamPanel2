import nest_asyncio
from nest_asyncio import asyncio
nest_asyncio.apply()
from general.logger import logging
import subprocess

def RestartCamPanel():
    subprocess.run(["sudo", "systemctl", "restart", "CamPanel.service"])

def RestartSystem():
    subprocess.run(["sudo", "restart"])
