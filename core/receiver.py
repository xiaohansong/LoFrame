'''
GET / HTTP/1.1
Host: 127.0.0.1:7867
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:31.0) Gecko/20100101 Firefox/31.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: keep-alive


'''
import threading
from client import Client
import datetime
import uuid
import time
import logging
import restlist as util

class Receiver(threading.Thread):
    def __init__(self, soc,c,addr):
        threading.Thread.__init__(self)
        self.soc = soc
        self.c = c
        self.addr = addr
        self.cl = None
        self.logger = logging.getLogger(__name__)

    def run(self):
        self.c.setblocking(0) 
        raw_msg = ""
        timeout = 0.6 # 0.6 second timeout
        begin = time.time()
        while time.time() - begin < timeout:
            try:
                data = self.c.recv(8192)
                if data:
                    raw_msg += data
                    #change the beginning time for measurement
                    begin = time.time()
                else:
                    #sleep for sometime to indicate a gap
                    time.sleep(0.1)
            except Exception:
                pass
                
        processed_msg = self.process(raw_msg)
        if processed_msg is not None:
            self.cl.msg_upload = processed_msg
            self.cl.upload_ready = True


    def process(self, msg):
        msg_up = {}
        msg_line = msg.split("\r\n")
        msg_info = msg_line[0].split(" ")
        if len(msg_info) < 2:
            return None
        else:
            # Refactor Needed. For GET & POST
            msg_up['METHOD'] = msg_info[0]

            if '?' in msg_info[1]:
                msg_dest_get = msg_info[1].split("?")
                msg_up['DEST'] = msg_dest_get[0]
                self.logger.debug("Get upload info: " + msg_dest_get[1])
                info_pair = self.getDictByGet(msg_dest_get[1])
                self.logger.debug("info_pair: ")
                for k in info_pair:
                    self.logger.debug(k + " -> " + info_pair[k])
                msg_up.update(info_pair)
                
            else:
                msg_up['DEST'] = msg_info[1]
            
            if(msg_up['METHOD'] not in util.REST_LIST):
                return None
       
        
        if msg_up.get('METHOD','GET') == "POST":
            msg_pair = self.getDictByGet(msg_line[-1])
            msg_up.update(msg_pair)
        if "uuid=\"" in msg:
            cid = msg.split("uuid=\"")[1].split("\"\r\n")[0]
        else:
            cid = str(uuid.uuid4())
        if cid in Client.client_info:
            self.cl = Client.client_info[cid]
            if self.cl.c is not None:
                self.cl.c.close()
                self.cl.c = self.c
                self.cl.addr = self.addr
        else:
            self.cl = Client(cid, self.c,self.addr)

        self.cl.timestamp = datetime.datetime.now()
        Client.client_info[cid] = self.cl
        self.logger.debug("processed map: ")
        for k in msg_up:
            self.logger.debug(k + "  ->  " + msg_up[k])
        return msg_up
    
    def getDictByGet(self, msg):
        msg_pair={}
        self.logger.debug("msg: " + msg)
        msg_get_info = msg.split("&")
        for pair in msg_get_info:
            pair = pair.replace("%40", "@")
            self.logger.debug("pair:" + pair)
            k_v = pair.split("=")
            self.logger.debug("after split: " + k_v[0]+" = " + k_v[1])
            msg_pair[k_v[0]] = k_v[1]
        self.logger.debug("Pair: ")
        for k in msg_pair:
            self.logger.debug(k + "  " + msg_pair[k])
        return msg_pair