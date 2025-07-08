## This provides functions to sense the existence of WiFi AP in real time
## Should in root privilege
import subprocess as sp
import logging
import re

SHELL_POPEN = lambda x: sp.Popen(x, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
SHELL_RUN = lambda x: sp.run(x, stdout=sp.PIPE, stderr=sp.PIPE, check=True, shell=True)


def RUN_WITH_RES(cmd: str, format = None) -> str:
    try:
        ret = SHELL_RUN(cmd).stdout.decode()
    except sp.CalledProcessError as e:
        ret = e.stderr.decode()
        logging.error(ret)
        return ret
    else:
        if format is not None:
            # Extract matches using regex
            ret = re.findall(format, ret)
            # Filter out empty matches
            ret = [x for x in ret if x]
            
            # Format the result:
            if len(ret) == 0:  # Empty → return empty string
                ret = ''
            elif len(ret) == 1:  # Single match → return as string
                ret = str(ret[0])
        return ret

class WirelessInterface:
    def __init__(self, name):
        self.name = name
        self.ind = self._determine_phy_id()
        self._bring_up()
        pass
    
    def _bring_up(self):
        ## determine if the interface is blocked
        rfkill_output = RUN_WITH_RES(f'rfkill list {self.ind}', format=r'\b(Soft|Hard)\s+blocked:\s+(yes|no)')
        if not rfkill_output:
            return
        hard_blocked = any(output[0] == 'Hard' and output[1] == 'yes' for output in rfkill_output)
        if hard_blocked:
                raise ValueError('The wireless card is hard blocked, please resolve manually')

        soft_blocked = any(output[0] == 'Soft' and output[1] == 'yes' for output in rfkill_output)
        if soft_blocked:
            RUN_WITH_RES(f'rfkill unblock {self.ind}')
        
        ## determine if the interface is up
        status = RUN_WITH_RES(f'ip link show {self.name}', format=r'state\s+(UP|DOWN)')
        if status == 'DOWN':
            RUN_WITH_RES(f'sudo ip link set {self.name} up')
            
        logging.info('Complete the bring up')
        
    def _determine_phy_id(self):
        ret = RUN_WITH_RES(f'cat /sys/class/net/{self.name}/phy80211/index')
        return eval(ret)
        
    def scan_ap(self):
        # RUN_WITH_RES(f'sudo iw dev {self.name} scan')
        return RUN_WITH_RES(f"sudo iwlist {self.name} scanning | egrep 'Cell |Encryption|Quality|Last beacon|ESSID'")

    
        
    