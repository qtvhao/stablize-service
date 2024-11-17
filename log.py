class Log:
    """
    Class to log messages to the console
    """
    def __init__(self, log_file):
        self.log_file = log_file
        self.app_log_file = "/tmp/app.log"

    def log(self, message):
        """
        Logs a message to the console and the log file
        """
        print(message)
        message = f"{message}"
        with open(self.log_file, "a") as f:
            f.write(message + "\n")
        with open(self.app_log_file, "a") as f:
            f.write(message + "\n")
#

