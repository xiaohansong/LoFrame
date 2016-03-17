import datetime
from client import Client
import threading
import time

class Clean(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            client_newinfo = []
            for cl in Client.client_info:
                now_time = datetime.datetime.now()
                if(now_time.minute - Client.client_info[cl].timestamp.minute > 20):
                    client_newinfo.append(cl)
            for cl in client_newinfo:
                del Client.client_info[cl]
            time.sleep(1)

