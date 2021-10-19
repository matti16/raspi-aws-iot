import os
from datetime import datetime

class LastSentUtils:
    date_fmt = "%Y-%m-%d %H:%M:%S"

    def __init__(self, file_path):
        self.file_path = file_path
        directory = os.path.dirname(self.file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

    def remove_last_sent(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def check_upload(self, interval_min):
        if os.path.exists(self.file_path):
            last_sent = open(self.file_path, "r").read()
            last_sent = datetime.strptime(last_sent, self.date_fmt)
            now = datetime.now()
            return (now - last_sent).seconds > interval_min * 60
        else:
            return True  
    
    def update_last_sent(self):
        with open(self.file_path, "w") as f:
            now = datetime.now()
            f.write(now.strftime(self.date_fmt))
