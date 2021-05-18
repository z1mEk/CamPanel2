import subprocess

class plugin:

    @classmethod
    def initialize(self):
        pid = subprocess.Popen(["python3 ./plugins/webserver/webserver.py", ""]).pid
