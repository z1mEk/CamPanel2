import os
import subprocess
from git import Repo
import serial
import time

def git_pull(repo_path):
    repo = Repo(repo_path)
    repo.git.pull()

def check_for_new_tft(tft_path):
    return os.path.exists(tft_path)

def upload_tft_to_nextion(serial_port, tft_path):
    try:
        with serial.Serial(serial_port, 9600, timeout=1) as ser:
            print(f"Connected to {serial_port}")

            # Reading the content of the tft file
            with open(tft_path, 'rb') as f:
                tft_data = f.read()

                # Sending the tft file to Nextion
                ser.write(tft_data)

            print(f"File {tft_path} sent successfully.")

    except serial.SerialException as e:
        print(f"Error: {e}")

def restart_service(service_name):
    subprocess.run(['sudo', 'systemctl', 'restart', service_name])

if __name__ == "__main__":
    # Replace with the path to your git repository
    repo_path = './'

    # Replace with the path to your tft file
    tft_path = './plugins/hmi/NextionInterface.tft'

    # Replace 'COMx' with the appropriate serial port of your Nextion display
    serial_port = '/dev/ttyUSB1'

    # Replace 'Campanel.service' with the name of your service
    service_name = 'Campanel.service'

    # Perform a git pull
    git_pull(repo_path)

    # Check for a new tft file
    if check_for_new_tft(tft_path):
        # Upload the tft file to Nextion
        upload_tft_to_nextion(serial_port, tft_path)

        # Restart the specified service
        restart_service(service_name)
