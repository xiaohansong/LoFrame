from header import Header
from status import Status_OK
from status import Status_NOTFOUND
import os
import logging
from config import Config
from abc import abstractmethod
class Filetype(object):
    
    def __init__(self, process_map, extra_header):
        self.lock = True
        self.logger = logging.getLogger(__name__)
        conf = Config()
        root = conf.config_directory["ROOT"]

        requested_file = root + process_map["FILE"]
        self.status = self.__get_status(requested_file)
        self.header = Header(self.status)
        self.process_map = process_map
        self.body = ""
        for key, value in extra_header.iteritems():
            self.header.set_extra(key, value)

    def __get_status(self, requested_file):
        if not os.path.isfile(requested_file):
            # maybe chcanged for dynamic 404 displaying
            return Status_NOTFOUND()
        else:
            return Status_OK(requested_file)

    @abstractmethod
    def set_header(self):
        pass

    def sendinfo(self):
        self.set_header()
        if not isinstance(self.status, Status_OK):
            self.header.set_type("text")
        return self.header.get_header() + self.body

class Filetype_bin(Filetype):
    def __init__(self, process_map, extra_header):
        super(Filetype_bin, self).__init__(process_map,extra_header)
        self.body = self.__load_bin()
        self.len = len(self.body)
        

    def set_header(self):
        self.header.set_first_line(self.status)
        self.header.set_content_length(self.len)
        # header.set_uuid(self.process_map)
        self.header.set_connection_line("close")

    def __load_bin(self):
        path = self.status.file_path
        content = None
        try:
            with open(path, 'rb') as f:
                content = f.read()
        except IOError:
            self.logger.error("File not found. " + path)
            content = ""
        return content

class Filetype_download(Filetype_bin):
    def __init__(self, process_map, extra_header):
        super(Filetype_download, self).__init__(process_map,extra_header)

    def set_header(self):
        super(Filetype_download, self).set_header()
        self.header.set_type("application/octet-stream")


    
class Filetype_image(Filetype_bin):
    def __init__(self, process_map, extra_header):
        super(Filetype_image, self).__init__(process_map,extra_header)

    def set_header(self):
        super(Filetype_image, self).set_header()
        self.header.set_type("image")
    
class Filetype_pdf(Filetype_bin):
    def __init__(self, process_map, extra_header):
        super(Filetype_pdf, self).__init__(process_map,extra_header)

    def set_header(self):
        super(Filetype_pdf, self).set_header()
        self.header.set_type("application/pdf")

class Filetype_text(Filetype):
    def __init__(self, process_map, extra_header):
        super(Filetype_text, self).__init__(process_map,extra_header)
        self.body = self.__load()
        self.len = len(self.body)
        #self.set_header

    def __load(self):
        # fix
        page_path = self.status.file_path
        transformed = ""
        with open(page_path) as f:
            for line in f.readlines():
                #replace the {***} thing
                left_br = line.split("{")
                for i in range(1,len(left_br)):
                    right_br = left_br[i].split("}")
                    if len(right_br) > 1:
                        replace_str = ""
                        try:
                            replace_str = self.process_map[right_br[0]]
                        except KeyError:
                            replace_str = None
                        if replace_str is not None:   
                            line = line.replace("{" + right_br[0] +"}", self.process_map[right_br[0]])
                transformed += line
        return transformed

    def set_header(self):
        self.header.set_first_line = self.status.generate_first_line()
        self.header.set_content_length(self.len)
        self.header.set_connection_line("close")
        self.header.set_type("text/html")
