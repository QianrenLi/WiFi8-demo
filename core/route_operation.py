import subprocess as sp
import psutil
import socket

SHELL_POPEN = lambda x: sp.Popen(x, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
SHELL_RUN = lambda x: sp.run(x, stdout=sp.PIPE, stderr=sp.PIPE, check=True, shell=True)

from ipaddress import ip_network

def seperate_nic(winf_names, netmask=24):
    initial_priority = 100

    # Get all network interface addresses
    net_addrs = psutil.net_if_addrs()
    nic_info = {}    
    for nic in winf_names:
        nic = nic.strip()
        if not nic:
            continue
        
        addresses = net_addrs[nic]
        # Iterate through each address associated with the interface
        for snicaddr in addresses:
            # Check for IPv4 addresses and retrieve their netmask
            if snicaddr.family == socket.AF_INET:
                ip_addr = ip_network(f"{snicaddr.address}/{netmask}", strict=False)
                nic_info[nic] = {
                    'ip': snicaddr.address,
                    'netmask': snicaddr.netmask,
                    'subnet' : str(ip_addr),
                    'gateway' : str(ip_addr[1]),
                    'priority': initial_priority
                }
        initial_priority += 1
                
    for nic, info in nic_info.items():
        # Set the interface metric
        SHELL_RUN(
            f'sudo ip route add {info["subnet"]} dev {nic} table {info["priority"]}'
        )
        SHELL_RUN(
            f'sudo ip route add default via {info["gateway"]} dev {nic} table {info["priority"]}'
        )
        SHELL_RUN(
            f'sudo ip rule add from {info["ip"]} lookup {info["priority"]} priority {info["priority"]}'
        )

def clean_up(winf_names):
    # Remove all routing rules and routes for the specified interfaces
    initial_priority = 100
    net_addrs = psutil.net_if_addrs()
    nic_info = {}    
    for nic in winf_names:
        nic = nic.strip()
        if not nic:
            continue
        
        addresses = net_addrs[nic]
        # Iterate through each address associated with the interface
        for snicaddr in addresses:
            # Check for IPv4 addresses and retrieve their netmask
            if snicaddr.family == socket.AF_INET:
                nic_info[nic] = {
                    'ip': snicaddr.address,
                    'priority': initial_priority
                }
            initial_priority += 1
            
    for nic in winf_names:
        nic = nic.strip()
        if not nic:
            continue
        
        SHELL_RUN(f'sudo ip rule del from {nic_info[nic]["ip"]} lookup {nic_info[nic]["priority"]}')
        SHELL_RUN(f'sudo ip route flush table {nic_info[nic]["priority"]}')

        
        
if __name__ == '__main__':
    winf_names = ['wlx081f7165e561', 'wlx081f7163a93d']
    seperate_nic(winf_names)
    # clean_up(winf_names)
        