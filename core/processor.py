import threading
import logging
from client import Client
from api import API
from filetype import Filetype_text
from filetype import Filetype_image
from filetype import Filetype_pdf
from filetype import Filetype_download

class Processor(threading.Thread):
    
    text_type = ["html","htm","txt", "css", "js"]
    image_type = ["jpg", "png", "gif"]
    pdf_type = ["pdf"]

    def __init__(self,client):
        threading.Thread.__init__(self)
        self.cl = client
        self.filetype = None
        self.logger = logging.getLogger(__name__)

    def process(self):
        self.cl.upload_ready = False
        #may load session or upload map here.
        #check if input is messed up.
        if not self.cl.is_valid():
            return

        ctrl_obj = API.runControllerByClient(self.cl)
        if ctrl_obj is None:
            # Go To E404 Logic
            self.logger.info("OBJ is NONE")
            return
        else:
            self.cl.session = ctrl_obj.session
            self.identify_file_type(ctrl_obj.process_map, ctrl_obj.extraheader)

    def identify_file_type(self, process_map, extraheader):
        suffix = process_map["FILE"].split(".")[-1].lower() # maybe bug. like "abhtml"
        if(suffix in Processor.text_type):
            self.filetype = Filetype_text(process_map, extraheader)
        elif (suffix in Processor.image_type):
            self.filetype = Filetype_image(process_map, extraheader)
        elif (suffix in Processor.pdf_type):
            self.filetype = Filetype_pdf(process_map, extraheader)
        else:
            self.filetype = Filetype_download(process_map, extraheader)

        Client.client_info[self.cl.uid].msg_upload = {}

    def run(self):
        self.process()
        Client.client_info[self.cl.uid].send_msg(self.filetype)
        