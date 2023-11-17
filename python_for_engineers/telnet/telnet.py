import getpass
import telnetlib
import sys

HOST = "192.168.1.10"
user = input("Enter your telnet account: ")
password = getpass.getpass()

tn = telnetlib.Telnet(HOST)

tn.read_until(b"login: ")
tn.write(user.encode('ascii') + b"\n")
if password:
    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii') + b"\n")

tn.write("enable\n")
tn.write("conf t\n")
tn.write("int 1/1/24\n")
tn.write("description ichangedthis\n")

print(tn.read_all().decode('ascii'))