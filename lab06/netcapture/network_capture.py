import subprocess
from scapy.all import *

def get_interfaces():
    result = subprocess.run(["netsh", "interface", "show", "interface"], 
                            capture_output=True, text=True)
    output_lines = result.stdout.splitlines()[3:]
    interfaces = [line.split()[3] for line in output_lines if len(line.split()) >= 4]
    return interfaces

def packet_handler(packet):
    if packet.haslayer(Raw):
        print("captured packet: ")
        print(str(packet))

interface = get_interfaces()

print("Danh sách các giao diện mạng: ")
for i, iface in enumerate(interface, start=1):
    print(f"{i}. {iface}")

choice = int(input("Chọn giao diện mạng( nhập số): "))
selected_iface = interface[choice - 1]

sniff(iface=selected_iface, prn=packet_handler, filter="tcp")