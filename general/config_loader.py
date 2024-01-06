import json
from types import SimpleNamespace

with open('./config/config.json') as json_file:
    config = json.load(json_file, object_hook=lambda d: SimpleNamespace(**d))
