import os

PRINT_LOG = True

class Logger():
    def __init__(self, print_log=False):
        self.print_log = print_log

    def print(self, message):
        if self.print_log:
            print(message)


LoggerSingleton = Logger(os.getenv('PRINT_LOG', PRINT_LOG))