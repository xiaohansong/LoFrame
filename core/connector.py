import socket
import threading
import os
import logging
from receiver import Receiver
from config import Config

class Connector(threading.Thread):
    socket_listen = None
    non_stop = True
    def __init__(self):
        threading.Thread.__init__(self)
        self.logger = logging.getLogger(__name__)
        if Connector.socket_listen is None:
            conf = Config()
            port = conf.config_directory["PORT"]
            try:
                self.listen = socket.socket()
                self.listen.bind(("0.0.0.0",int(os.environ.get('PORT',port))))
            except socket.error:
                self.logger.error("CREATE ERROR. MAYBE PORT IN USE. WILL EXIT.")
                exit()
            self.logger.info("build success!")
        else:
            self.listen = Connector.socket_listen

    def run(self):
        self.listen.listen(15)
        while Connector.non_stop:
            c, addr = self.listen.accept()
            receiver = Receiver(self.listen,c,addr)
            receiver.start()
