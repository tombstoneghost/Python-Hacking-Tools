# Imports
import optparse
import scapy.all as scapy


# Getting Arguments from CLi
def get_args():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Specify interface to use")

    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")

    return options


# Get MAC Address
def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    return answered_list[0][1].hwsrc


# Sniffing Data
def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)


# Processing Sniffed Packet
def process_sniffed_packet(packet):
    if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
        try:
            real_mac = get_mac(packet[scapy.ARP].psrc)
            response_mac = packet[scapy.ARP].hwsrc

            if real_mac != response_mac:
                print("[+] You are under attack")
            print(packet.show())

        except IndexError:
            pass


args = get_args()

sniff(args.interface)
