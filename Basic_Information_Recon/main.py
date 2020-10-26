# Imports
import sys
import requests
import socket
import json

# Checking Input Parameters
if len(sys.argv) < 2:
    print("Usage: " + sys.argv[0] + "[url]")
    sys.exit(1)

# Get Target Headers
request = requests.get("http://" + sys.argv[1])
print("\n" + str(request.headers))

# Get IP of the target
get_host_by_name = socket.gethostbyname(sys.argv[1])
print("\nThe IP address of " + sys.argv[1] + " is: " + get_host_by_name + "\n")

# IP Address Information
request_ip = requests.get("http://ipinfo.io/" + get_host_by_name + "/json")
response = json.loads(request_ip.text)

print("Location: " + response["loc"])
print("Region: " + response["region"])
print("City: " + response["city"])
print("Country: " + response["country"])
