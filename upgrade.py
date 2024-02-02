#!/usr/bin/python
import io
import subprocess
#from git import Repo
from general.configLoader import config
from general.deviceManager import device
from nextion import Nextion, client
import nest_asyncio
from nest_asyncio import asyncio
nest_asyncio.apply()

def git_pull(repo_path):
    try:
        print(f"Pull data from git")
        result = subprocess.check_output(["git", "pull"])
        result_str = result.decode("utf-8")
        print(f"{result_str}")
        return True if "NextionInterface.tft" in result_str else False
    except Exception as e:
        print("git_pull {e}")
    return False

    # repo = Repo(repo_path)
    # origin = repo.remotes.origin
    
    # result = origin.pull()

    # # Wypisanie informacji o zmienionych plikach
    # for fetch_info in result:
    #     print(f"Commit message: {fetch_info.commit.message}")
    #     changed_files = [f"[{item.change_type}] {item.a_path}" for item in fetch_info.commit.diff('HEAD~1') if item.change_type in ('M', 'A', 'D')]
    #     print("Changed files:")
    #     for changed_file in changed_files:
    #         print(f"{changed_file}")

    # return repo.git.diff('HEAD~1..HEAD', tft_path)

async def upload_tft_to_nextion(tft_path):
    print(f"Read TFT file: {tft_path}")
    try:

        event_loop = asyncio.get_event_loop()
        nextion_device = device.FindUsbDevice(config.nextion.device)
        nextion_client = Nextion(nextion_device, config.nextion.baudrate, eventHandler, event_loop, reconnect_attempts=5, encoding="utf-8")
        await nextion_client.connect()

        with open(tft_path, 'rb') as file:
            buffered_reader = io.BufferedReader(file)
            print(f"Upload file: {tft_path}")
            await nextion_client.upload_firmware(buffered_reader, 115200)

        print(f"File {tft_path} uploaded")

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
