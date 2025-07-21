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
    
    
def test_renewed_connect():
    wdev = _test_scan_config()
    policy = PowerGreedyPolicy()
    
    start_time = time.time()
    # while True:
    wdev.scan_ap(channel=1)
    # ssid = 'TP-LINK_8805'
    # wdev.connect(ssid)
    wdev.connect('LAB1112')
    from core.ip_operation import dhcp_static_ip
    # ap = policy.AP_selection(wdev.ap_list)
    # print(ap)
    dhcp_static_ip('192.168.1.154', '192.168.1.1', wdev.name)
    end_time = time.time()
    print(end_time - start_time)
    
    # wdev.scan_ap()
    # wdev.connect('LAB1112')
    
    
    # print(wdev.ap_list)

def test_dual_connect_with_ip():
    wdevs = _test_dual_config()
    policy = PowerGreedyPolicy()
    from core.ip_operation import dhcp_static_ip
    # ap = policy.AP_selection(wdev.ap_list)
    # print(ap)
    
    for idx, wdev in enumerate(wdevs):
        if idx == 0:
            wdev.scan_ap()
            wdev.connect('HUAWEI-Dual-AP')
            dhcp_static_ip('192.168.3.25', '192.168.3.1', wdev.name)
        else:
            wdev.scan_ap()
            wdev.connect('HUAWEI-Dual-AP_5G')
            dhcp_static_ip('192.168.3.35', '192.168.3.1', wdev.name)
    
    # start_time = time.time()
    # # while True:
    # wdev.scan_ap(channel=1)
    # # ssid = 'TP-LINK_8805'
    # # wdev.connect(ssid)
    # wdev.connect('LAB1112')
    # from core.ip_operation import dhcp_static_ip
    # # ap = policy.AP_selection(wdev.ap_list)
    # # print(ap)
    # dhcp_static_ip('192.168.1.154', '192.168.1.1', wdev.name)
    # end_time = time.time()
    # print(end_time - start_time)

# test_scan()
# test_scan(freq = 2462)
# test_sense_freq()
# test_ap_react()

# test_wpa_supplicant()
# test_dual_connect()
# test_renewed_connect()

test_dual_connect_with_ip()