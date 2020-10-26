# Imports
import requests
import optparse
import re
import urllib.parse


# Getting arguments from CLI
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target", help="Specify Target URL")

    (options, arguments) = parser.parse_args()

    if not options.target:
        parser.error("[-] Please specify a target URL, use --help for more info.")

    return options


# Get Response
def request(url):
    try:
        return requests.get("http://" + url)

    except requests.exceptions.ConnectionError:
        pass


# Target URL
target_url = get_arguments().target
target_links = []

print("\nDiscovering Subdomains\n")

# Reading Wordlist to generate and test Subdomains
with open("/usr/share/wordlists/rockyou.txt", "r") as wordlist_file:
    for line in wordlist_file:
        word = line.strip()
        test_url = word + '.' + target_url
        response = request(test_url)
        if response:
            print("[+] Discovered Subdomain: " + test_url)

print("\nDiscovering Sub-directories\n")

# Reading Wordlist to generate and test sub-directories
with open("/usr/share/wordlists/dirb/common.txt", "r") as wordlist_file:
    for line in wordlist_file:
        word = line.strip()
        test_url = word + '.' + target_url
        response = request(test_url)
        if response:
            print("[+] Discovered Subdirectory: " + test_url)


# Extracting all links in a URL
def extract_links_from(url):
    res = requests.get(url)
    # noinspection PyTypeChecker
    return re.findall('(?:href=")(.*)"', res.content.decode(errors="ignore"))


print("\nDiscovering all links in the target page [Crawling]\n")


# Crawling
def crawl(url):
    href_links = extract_links_from(url)

    for link in href_links:
        link = urllib.parse.urljoin(url, link)

        if "#" in link:
            link = link.split("#")[0]

        if target_url in link and link not in target_links:
            target_links.append(link)
            print(link)
            crawl(link)


# Start Crawling
crawl(target_url)
