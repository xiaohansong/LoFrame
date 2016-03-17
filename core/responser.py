import threading
import time
from client import Client
from processor import Processor

class Responser(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        while True:
            for cl in Client.client_info:
                Client.client_lock = True
                if Client.client_info[cl].upload_ready:
                    bend = Processor(Client.client_info[cl])
                    bend.start()
            Client.client_lock = False
            time.sleep(0.131)