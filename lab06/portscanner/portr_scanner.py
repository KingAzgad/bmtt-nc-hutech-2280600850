from scapy.all import *

COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 143, 443, 455, 3389]

def scan_common_ports(target_domain, timeout=2):
    open_ports = []
    target_ip = socket.gethostbyname(target_domain)
    
    for port in COMMON_PORTS:
        response = sr1(IP(dst=target_ip)/TCP(dport=port, flags="S"), timeout=timeout, verbose=0)
        
        if response and response.haslayer(TCP) and response[TCP].flags == 0x12:
            open_ports.append(port)
            send(IP(dst=target_ip)/TCP(dport=port, flags="R"), verbose=0)
    return open_ports

def main():
    target_domain = input("Enter the target domain: ")
    open_ports = scan_common_ports(target_domain)
    
    if open_ports:
        print(f"Open ports on {target_domain}:")
        for port in open_ports:
            print(f"Port {port} is open")
    else:
        print(f"No open ports found on {target_domain}")
        
if __name__ == "__main__":
    main()