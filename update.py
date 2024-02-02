import os, io
import subprocess
from git import Repo
import time
from general.configLoader import config
from general.deviceManager import device
from nextion import Nextion, client
import nest_asyncio
from nest_asyncio import asyncio
from general.logger import logging
nest_asyncio.apply()

def git_pull(repo_path):
    print(f"Pull data from git")
    repo = Repo(repo_path)
    origin = repo.remotes.origin
    
    result = origin.pull()

    print(f"{result}")

    # Wypisanie informacji o zmienionych plikach
    for fetch_info in result:
        for diff in repo.index.diff(fetch_info.commit):
            print(f"Changed file: {diff.a_path}")

    if repo.git.diff('HEAD~1..HEAD', tft_path):
        print(f"File tft modified")
        return True
    else:
        print(f"File tft not modified")
        return False

async def upload_tft_to_nextion(tft_path):
    print(f"Read tft file: {tft_path}")
    try:

        event_loop = asyncio.get_event_loop()
        print(f"Find nextion device")
        nextion_device = device.FindUsbDevice(config.nextion.device)
        print(f"Nextion device is: {nextion_device}")
        print(f"create Nextion object")
        nextion_client = Nextion(nextion_device, config.nextion.baudrate, eventHandler, event_loop, reconnect_attempts=5, encoding="utf-8")
        print(f"Nextion Connect")
        await nextion_client.connect()

        with open(tft_path, 'rb') as file:
            buffered_reader = io.BufferedReader(file)
            print(f"upload txt file: {tft_path}")
            await nextion_client.upload_firmware(buffered_reader, 115200)

        print(f"file uploaded")
    except Exception as e:
        print(f"upload tft file error: {e}")

def eventHandler(type_, data):
    pass

if __name__ == "__main__":

    # Replace with the path to your tft file
    tft_path = './plugins/hmi/NextionInterface.tft'

    print(f"Stop CamPanel.service")
    subprocess.run(['sudo', 'systemctl', 'stop', 'CamPanel.service'])

    # Sprawdzanie, czy są nowe zmiany w repozytorium dla pliku .tft
    if git_pull("./"):
        asyncio.run(upload_tft_to_nextion(tft_path))

    # Restartowanie określonej usługi
    print(f"Start CamPanel.service")
    subprocess.run(['sudo', 'systemctl', 'start', 'CamPanel.service'])