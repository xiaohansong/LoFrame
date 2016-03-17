import datetime
import socket
import logging

class Client(object):
    client_lock = False
    client_info = {}
    def __init__(self, uid, c, addr):
        self.timestamp = datetime.datetime.now()
        self.uid = uid
        self.c = c
        self.addr = addr
        self.session = {}
        self.msg_upload = {}
        self.upload_ready = False
        self.msg_dwload = {}
        self.filetype_generator = None
        self.logger = logging.getLogger(__name__)


    def is_valid(self):
        return self.msg_upload is not None

    def send_msg(self, filetype):
        #filetype: Filetype
        if filetype is None:
            self.logger.warning("FILETYPE EMPTY, will be discarded")
        else:
            try:
                filetype.header.set_uuid(self.uid)
                send_info = filetype.sendinfo()
                total_sent = 0
                ptr = 0
                self.c.setblocking(True)
                while True:
                    # maybe need to be fixed
                    l = self.c.send(send_info[ptr:])
                    total_sent += l
                    if(total_sent == len(send_info)):
                        self.logger.info("Message sent. Size: " + str(total_sent) + "Byte")
                        break
            except socket.error, (value, message):
                self.logger.error("socket.error:\n")
                self.logger.error(value + ", " + message)
                self.logger.error("SOCKET SEND ERROR. WILL SHUTDOWN THIS CLIENT CONNECTION")
                #del client.client_info[self.c]
                self.c.close()

 