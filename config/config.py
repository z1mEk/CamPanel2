import json
from types import SimpleNamespace

with open('./config/config.json') as json_file: data = json.load(json_file, object_hook=lambda d: SimpleNamespace(**d))