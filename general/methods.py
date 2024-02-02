import nest_asyncio
from nest_asyncio import asyncio
nest_asyncio.apply()
from general.logger import logging
import subprocess

def RestartCamPanel():
    subprocess.run(["sudo", "systemctl", "restart", "CamPanel.service"])

def RestartSystem():
    subprocess.run(["sudo", "restart"])

def Upgrade():
    logging.info("Rozpoczynam aktualizację urządzenia.")
    try:
        subprocess.run(["python", "./update.py"])
    except Exception as e:
        logging.error(f"Proces aktualizacji: {e}")