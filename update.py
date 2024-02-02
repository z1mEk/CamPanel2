import os
import subprocess
from git import Repo
import serial
from tqdm import tqdm
import time

def git_pull(repo_path):
    repo = Repo(repo_path)
    origin = repo.remotes.origin
    
    # Przechwycenie wyniku polecenia git pull
    result = origin.pull()
    
    # Wypisanie wyniku za pomocą print
    print("Git Pull Result:")
    for info in result:
        print(info)

    # Sprawdzanie, czy są zmiany w pliku .tft
    changes = repo.git.diff('HEAD~1..HEAD', tft_path)
    if changes:
        print("File tft changed")
        return True
    else:
        print("File tft not changed")
        return False

def check_for_new_tft(tft_path):
    return os.path.exists(tft_path)

def upload_tft_to_nextion(serial_port, tft_path):
    try:
        with serial.Serial(serial_port, 115200, timeout=1) as ser:
            print(f"Connected to {serial_port}")

            # Reading the content of the tft file
            with open(tft_path, 'rb') as f:
                tft_data = f.read()

                # Pasek postępu dla wgrywania pliku tft
                with tqdm(total=len(tft_data), desc="Uploading TFT File", unit="B", unit_scale=True) as pbar:
                    # Wysyłanie pliku tft do Nextion
                    ser.write(tft_data)
                    pbar.update(len(tft_data))

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
    service_name = 'CamPanel.service'

    # Sprawdzanie, czy są nowe zmiany w repozytorium dla pliku .tft
    if git_pull(repo_path):
        # Sprawdzanie, czy jest nowy plik tft
        if check_for_new_tft(tft_path):
            # Wgrywanie pliku tft na wyświetlacz Nextion
            upload_tft_to_nextion(serial_port, tft_path)

            # Restartowanie określonej usługi
            restart_service(service_name)
