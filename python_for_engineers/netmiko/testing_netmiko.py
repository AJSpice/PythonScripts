#!/usr/bin/env python
import netmiko

from netmiko import ConnectHandler

aruba_10_10_1020 = {
    'device_type': 'aruba_osswitch',
    'ip': '192.168.1.10',
    'username': 'python_user',
    'password': 'python_password',
}


net_connect = ConnectHandler(**aruba_10_10_1020)
#net_connect.find_prompt()
output = net_connect.send_command('show ip int brief')
print (output)

config_commands = ['int 1/1/20', 'description testing_netmiko']
output = net_connect.send_config_set(config_commands)
print (output)

for n in range (200,210):
    print (f"Creating VLAN {str(n)}")
    #config_commands = ['vlan ' + str(n), 'name Python_VLAN ' + str(n)]
    config_commands = [f"vlan {str(n)}", f"name NETMIKO_VLAN {str(n)}"]
    output = net_connect.send_config_set(config_commands)
    print (output) 