import importlib

def load_config(config_name:str):
    config_name = config_name.replace('/', '.')
    config_name = '.'.join(config_name.split('.')[:-1])
    # Dynamically load the config module
    config_module = importlib.import_module(config_name)
    return config_module