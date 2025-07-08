from util.config import load_config
from core.sense_wifi import WirelessInterface
import logging

def test_sense():
    logging.basicConfig(
        filename='log/test_ap_scan.log',
        level=logging.DEBUG,  # Set the logging level (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format='%(asctime)s - %(levelname)s - %(message)s',
    )
    config = load_config('config/test.py')
    wdev = WirelessInterface(config.wdev)
    print(wdev.scan_ap())
test_sense()