import io
import subprocess
from git import Repo
from general.configLoader import config
from general.deviceManager import device
from plugins.hmi import hmi
import nest_asyncio
from nest_asyncio import asyncio
from general.logger import logging
nest_asyncio.apply()
from plugins.hmi import hmi, helper, methods as methodsHmi
    
class plugin:

    repo_path = "./"
    tft_path = "./plugins/hmi/NextionInterface.tft"

    def git_pull(cls):
        logging.info(f"Pull data from https://github.com/z1mEk/CamPanel2.git")
        repo = Repo(cls.repo_path)
        origin = repo.remotes.origin
        result = origin.pull()

        for fetch_info in result:
            logging.info(f"Commit message: {fetch_info.commit.message}")
            changed_files = [f"[{item.change_type}] {item.a_path}" for item in fetch_info.commit.diff('HEAD~1') if item.change_type in ('M', 'A', 'D')]
            logging.info("Changed files:")
            for changed_file in changed_files:
                logging.info(f"{changed_file}")

        return repo.git.diff('HEAD~1..HEAD', cls.tft_path)

    async def upload_tft_to_nextion(cls, tft_path):
        logging.info(f"Read TFT file: {tft_path}")
        try:

            # event_loop = asyncio.get_event_loop()
            # nextion_device = device.FindUsbDevice(config.nextion.device)
            # nextion_client = Nextion(nextion_device, config.nextion.baudrate, cls.eventHandler, event_loop, reconnect_attempts=5, encoding="utf-8")
            # await nextion_client.connect()

            with open(tft_path, 'rb') as file:
                buffered_reader = io.BufferedReader(file)
                logging.info(f"Upload file: {tft_path}")
                await hmi.client.upload_firmware(buffered_reader, 115200)

            logging.info(f"File {tft_path} uploaded")
            #hmi.client.command("rest")
        except Exception as e:
            logging.info(f"upload tft file error: {e}")

    def eventHandler(type_, data):
        pass   

    async def upgrade():
        logging.info(f"Start upgrade nextion TFT")

        if plugin.git_pull():
            await plugin.upload_tft_to_nextion(plugin.tft_path)

        logging.info(f"Restart CamPanel.service")
        subprocess.run(['sudo', 'systemctl', 'restart', 'CamPanel.service'])

    @classmethod
    async def initialize(cls, event_loop):
        pass
