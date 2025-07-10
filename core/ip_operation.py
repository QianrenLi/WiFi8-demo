import os
import sys
import subprocess as sp

SHELL_POPEN = lambda x: sp.Popen(x, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
SHELL_RUN = lambda x: sp.run(x, stdout=sp.PIPE, stderr=sp.PIPE, check=True, shell=True)

def dhcp_static_ip(ip, ap_ip, winf_name):
    cmd = f"sudo dhcpcd -S ip_address={ip}/24 -S routers={ap_ip} -S domain_name_servers={ap_ip} {winf_name}"
    SHELL_RUN(cmd)