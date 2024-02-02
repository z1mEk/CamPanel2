import os
import subprocess
from git import Repo
import time
from general.configLoader import config
from general.deviceManager import device
from nextion import Nextion, client
import nest_asyncio
from nest_asyncio import asyncio
nest_asyncio.apply()

def git_pull(repo_path):
    print("Pull data from git")
    repo = Repo(repo_path)
    origin = repo.remotes.origin
    
    result = origin.pull()
    
    print("Git Pull Result:")
    for info in result:
        print(info)

    if repo.git.diff('HEAD~1..HEAD', tft_path):
        print("File tft changed")
        return True
    else:
        print("File tft not changed")
        return False

def upload_tft_to_nextion(tft_path):
    print(f"Read tft file: {tft_path}")
    try:
        with open(tft_path, 'rb') as file:
            file_buffered = file.read()

        print(f"upload txt file: {tft_path}")
        nextion_client.upload_firmware(file_buffered, 115200)
        print(f"file uploaded")
    except Exception as e:
        print(f"upload tft file error: {e}")

def eventHandler(type_, data):
    pass

if __name__ == "__main__":

    # Replace with the path to your tft file
    tft_path = './plugins/hmi/NextionInterface.tft'

    print("Stop CamPanel.service")
    subprocess.run(['sudo', 'systemctl', 'stop', 'CamPanel.service'])

    event_loop = asyncio.get_event_loop()
    print("Find nextion device")
    nextion_device = device.FindUsbDevice(config.nextion.device)
    print("Nextion device is: {nextion_device}")
    global nextion_client
    print("create Nextion object")
    nextion_client = Nextion(nextion_device, config.nextion.baudrate, eventHandler, event_loop, reconnect_attempts=5, encoding="utf-8")
    print("Nextion Connect")
    nextion_client.connect()

    # Sprawdzanie, czy są nowe zmiany w repozytorium dla pliku .tft
    if git_pull("./"):
        upload_tft_to_nextion(tft_path)

    # Restartowanie określonej usługi
    print("Start CamPanel.service")
    subprocess.run(['sudo', 'systemctl', 'start', 'CamPanel.service'])
