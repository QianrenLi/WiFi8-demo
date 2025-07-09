import logging
import time

from policy.power_greedy import PowerGreedyPolicy
from util.config import load_config
from core.winf import WirelessInterface
from core.wpa_supplicant_cli import WPA_SUPPLICANT_CLI

def _test_scan_config():
    logging.basicConfig(
        filename='log/test_ap_scan.log',
        level=logging.DEBUG,  # Set the logging level (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format='%(asctime)s - %(levelname)s - %(message)s',
    )
    config = load_config('config/test.py')
    wdev = WirelessInterface(config.primal_wdev, config.primal_ip)
    return wdev

def _test_dual_config():
    logging.basicConfig(
        filename='log/test_dual.log',
        level=logging.DEBUG,  # Set the logging level (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format='%(asctime)s - %(levelname)s - %(message)s',
    )
    config = load_config('config/test.py')
    wdevs = [
        WirelessInterface(config.primal_wdev, config.primal_ip),
        WirelessInterface(config.second_wdev, config.second_ip)
    ]
    
    return wdevs

def test_scan(**kwargs):
    wdev = _test_scan_config()
    start_time = time.time()
    wdev.scan_ap(**kwargs)
    end_time = time.time()
    print(wdev.ap_list)
    print(f'Scanning takes {end_time - start_time} s')


def _test_wpa_supplicant_config():
    logging.basicConfig(
        filename='log/test_wpa_supplicant.log',
        level=logging.DEBUG,  # Set the logging level (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format='%(asctime)s - %(levelname)s - %(message)s',
    )
    config = load_config('config/test.py')
    wpa_cli = WPA_SUPPLICANT_CLI(config.primal_wdev, config.primal_ip)
    return wpa_cli

def test_wpa_supplicant():
    wdev = _test_scan_config()
    policy = PowerGreedyPolicy()
    
    while True:
        wdev.scan_ap()
        ap = policy.AP_selection(wdev.ap_list)
        print(ap)
        wdev.connect(ap['ssid'])
        time.sleep(3)

def test_dual_connect():
    wdevs = _test_dual_config()
    policy = PowerGreedyPolicy()
    for idx, wdev in enumerate(wdevs):
        if idx == 0:
            wdev.scan_ap(freq=5220)
            ap = policy.AP_selection(wdev.ap_list)
            print(ap)
            wdev.connect(ap['ssid'])
        else:
            wdev.scan_ap(freq=2462)
            ap = policy.AP_selection(wdev.ap_list)
            print(ap)
            wdev.connect(ap['ssid'])
    
    
    
def test_ap_connect():
    wdev = _test_scan_config()

# test_scan()
# test_scan(freq = 2462)
# test_sense_freq()
# test_ap_react()

# test_wpa_supplicant()
test_dual_connect()