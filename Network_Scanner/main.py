# Imports
import scapy.all as scapy
import optparse

# Welcome
print("Welcome to the Network Scanner. \n")


# Get arguments from CLI
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target", help="Specify the target IP Range")

    (options, arguments) = parser.parse_args()
    if not options.target:
        parser.error("[-] Please specify the target, use --help for more info.")

    return options


# Performing Scan
def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    client_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        client_list.append(client_dict)

    return client_list


# Printing Result
def print_result(results_list):
    print("IP\t\t\tMAC Address\n" + "-" * 36)
    for client in results_list:
        print(client["ip"] + "\t\t" + client["mac"])


# Storing Required Value
args = get_arguments()

# Calling Functions
scan_result = scan(args.target)
print_result(scan_result)
