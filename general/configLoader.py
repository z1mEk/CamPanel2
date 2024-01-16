import json
from types import SimpleNamespace

configFile = './config/config.json'

with open(configFile) as json_file:
    config = json.load(json_file, object_hook=lambda d: SimpleNamespace(**d))

def updateConfigParam(section, param, new_value):
    with open(configFile, 'r') as f:
        config = json.load(f)

    if section in config and param in config[section]:
        if isinstance(config[section][param], list):
            config[section][param] = new_value.split(',')
        else:
            config[section][param] = new_value

        with open(configFile, 'w') as f:
            json.dump(config, f, indent=4)

# Przykład użycia
#update_config_param('nextion', 'startup_commands', 'thsp=60,thup=1,dim=30')
#update_config_param('nextion', 'startup_commands', 'thsp=60,thup=1,dim=30')            


