import logging
import time

from util.config import load_config
from core.winf import WirelessInterface

def _test_scan_config():
    logging.basicConfig(
        filename='log/test_ap_scan.log',
        level=logging.DEBUG,  # Set the logging level (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format='%(asctime)s - %(levelname)s - %(message)s',
    )
    config = load_config('config/test.py')
    wdev = WirelessInterface(config.wdev)
    return wdev

def test_sense(**kwargs):
    wdev = _test_scan_config()
    start_time = time.time()
    wdev.scan_ap(**kwargs)
    end_time = time.time()
    print(wdev.ap_list)
    print(f'Scanning takes {end_time - start_time} s')
    
def test_ap_react():
    import os
    logging.basicConfig(
        filename='log/test_ap_scan.log',
        level=logging.DEBUG,  # Set the logging level (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format='%(asctime)s - %(levelname)s - %(message)s',
    )
    config = load_config('config/test.py')
    wdev = WirelessInterface(config.wdev)
    while True:
        wdev.scan_ap(channel=36)
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear terminal
        print(wdev.ap_list)

# test_sense()
test_sense(freq = 5745)
# test_sense_freq()
# test_ap_react()