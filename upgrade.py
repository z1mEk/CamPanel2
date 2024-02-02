#!/usr/bin/python
import io
import subprocess
from general.configLoader import config
from general.deviceManager import device
from nextion import Nextion
import nest_asyncio
from nest_asyncio import asyncio
nest_asyncio.apply()

def git_pull():
    try:
        print(f"git pull")
        result = subprocess.check_output(["git", "pull"])
        result_str = result.decode("utf-8")
        print(f"{result_str}")
        return True if "NextionInterface.tft" in result_str else False
    except Exception as e:
        print("git_pull: {e}")
    return False

async def upload_tft_to_nextion(tft_path):
    print(f"Nextion display firmware update required. This may take a few minutes.\nProgress will be visible on the Nextion display")
    try:
        event_loop = asyncio.get_event_loop()
        nextion_device = device.FindUsbDevice(config.nextion.device)
        nextion_client = Nextion(nextion_device, config.nextion.baudrate, None, event_loop, reconnect_attempts=5, encoding="utf-8")
        await nextion_client.connect()

        with open(tft_path, 'rb') as file:
            buffered_reader = io.BufferedReader(file)
            print(f"Upload file {tft_path} to Nextion...")
            await nextion_client.upload_firmware(buffered_reader, 115200)

        print(f"File {tft_path} uploaded to Nextion")

    except Exception as e:
        print(f"upload tft file error: {e}")

if __name__ == "__main__":
    tft_path = './plugins/hmi/NextionInterface.tft'

    print(f"Stop CamPanel.service")
    subprocess.run(['sudo', 'systemctl', 'stop', 'CamPanel.service'])

    if git_pull():
        asyncio.run(upload_tft_to_nextion(tft_path))

    print(f"Start CamPanel.service")
    subprocess.run(['sudo', 'systemctl', 'start', 'CamPanel.service'])
