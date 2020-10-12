# Imports
import subprocess
import optparse
import re

# Welcome
print("Welcome to the MAC Changer. \n")

"""Functions"""


# Get arguments from CLI
def get_arguments():
    parser = optparse.OptionParser()

    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC Address")

    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not options.new_mac:
        parser.error("[-] Please specify a new mac, use --help for more info.")

    return options


# Changing MAC Address
def change_mac(interface, new_mac):
    print("[+] Changing MAC Address for: " + interface + " to " + new_mac)

    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw ether ", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


# Checking Current MAC Address
def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))

    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read MAC address.")


# Calling Functions
args = get_arguments()
change_mac(args.interface, args.new_mac)
current_mac = get_current_mac(args.interface)

if current_mac == args.new_mac:
    print("[+] MAC Address was successfully changed to " + current_mac)
else:
    print("[-] MAC Address did not get changed.")
