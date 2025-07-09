import os
import sys
import subprocess as sp

SHELL_POPEN = lambda x: sp.Popen(x, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
SHELL_RUN = lambda x: sp.run(x, stdout=sp.PIPE, stderr=sp.PIPE, check=True, shell=True)

TEMPLATE_CONFIG = lambda ssid: '''
network={
    ssid=\"%s\"
    key_mgmt=NONE
}''' % ssid

class WPA_SUPPLICANT_CLI():
    def __init__(self, wdev_name, ip):
        self.name = wdev_name
        self.ip = ip
        self.path = "./config/wpa_supplicant/wifi8-%s.conf" % wdev_name
        self.ctrl_interface = f"/var/run/wpa_supplicant_{wdev_name}"
        if not os.path.exists(self.path):
            SHELL_RUN(f'touch {self.path}')
            with open(self.path, 'w') as f:
                f.write('update_config=1\n')
                f.write('ap_scan=2') ## We do not want AP scan to affect the process (?)
                
            print("Create file successful")
        self.ssid = self._read_existing_ssid() ## We do not generalized to same SSID with different frequency or MAC
        self.is_started = False
    
    def _read_existing_ssid(self):
        with open(self.path, 'r') as f:
            wpa_config = f.readlines()
            
        ssid_set = []
        for line in wpa_config:
            if 'ssid=' in line:
                ssid = line.split('ssid=')[1].strip().strip('"')
                ssid_set.append(ssid)
        return ssid_set
    
    def add_ssid(self, ssid):
        if ssid not in self.ssid:
            self.ssid.append(ssid)
            with open(self.path, 'a') as f:
                f.write(TEMPLATE_CONFIG(ssid))
    
    def _start_wpa_supplicant(self):
        cmd = "sudo wpa_supplicant -B -i %s -c %s -C %s" % (self.name, self.path, self.ctrl_interface)
        # cmd += f"; sudo dhcpcd -S ip_address={self.ip}/24 -S routers=192.168.3.1 -S domain_name_servers=192.168.3.1 {self.name}"
        SHELL_RUN(cmd)
        self.is_started = True

    def _reload_wpa_supplicant(self):
        cmd = f"sudo wpa_cli -i {self.name} -p {self.ctrl_interface} reconfigure"
        # cmd += f"; sudo dhcpcd -S ip_address={self.ip}/24 -S routers=192.168.3.1 -S domain_name_servers=192.168.3.1 {self.name}"
        SHELL_RUN(cmd)
    
    def _stop_wpa_supplicant(self):
        cmd = f'sudo pkill -f "wpa_supplicant -B -i {self.name}"'
        SHELL_RUN(cmd)
        self.is_started = False
        
    def connect(self, network_id):
        if not self.is_started:
            self._start_wpa_supplicant()
        else:
            self._reload_wpa_supplicant()
            
        cmd  = f"sudo wpa_cli -i {self.name} -p {self.ctrl_interface} enable_network {network_id}"
        cmd += f"; sudo wpa_cli -i {self.name} -p {self.ctrl_interface} select_network {network_id}"
        cmd += f"; sudo wpa_cli -i {self.name} -p {self.ctrl_interface} disconnect"
        cmd += f"; sudo wpa_cli -i {self.name} -p {self.ctrl_interface} reconnect"
        SHELL_RUN(cmd)
        
    def clear(self):
        ## rm wpa_supplicant.conf
        if self.is_started:
            self._stop_wpa_supplicant()
        SHELL_RUN(f'rm {self.path}')