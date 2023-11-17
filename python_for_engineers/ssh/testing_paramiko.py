#Testing Paramiko

import paramiko
import time

ip_address = "192.168.1.10"
username = "python_user"
password = "python_password"

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname=ip_address,username=username,password=password)

print (f"Successful connection {ip_address}")

remote_connection = ssh_client.invoke_shell()

remote_connection.send("configure terminal\n")

remote_connection.send("int 1/1/24\n")
remote_connection.send("description testing_paramiko\n")
remote_connection.send("int 1/1/25\n")
remote_connection.send("description testing_paramiko\n")
remote_connection.send("int 1/1/26\n")
remote_connection.send("description testing_paramiko\n")

for n in range (20,25):
    print (f"Creating VLAN: {str(n)}")
    remote_connection.send(f"vlan {str(n)}\n")
    remote_connection.send(f"name PARAMIKO_VLAN_{str(n)}\n")
    time.sleep(2.0)

#remote_connection.send("end\n")

time.sleep(1)
output = remote_connection.recv(65535)
print (output)

ssh_client.close