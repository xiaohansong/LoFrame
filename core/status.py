from abc import abstractmethod
from config import Config

class Status(object):
    def __init__(self, file_path):
        self.file_path = file_path

    def generate_first_line(self):
        return "HTTP/1.1 200 OK\r\n"

    @abstractmethod
    def get_status_code(self):
        pass

class Status_OK(Status):
    def __init__(self, file_path):
        super(Status_OK, self).__init__(file_path)

    def get_status_code(self):
        return "200"

class Status_NOTFOUND(Status):
    def __init__(self):
        super(Status_NOTFOUND, self).__init__("")
        conf =  Config()
        root = conf.config_directory["ROOT"]
        path = conf.config_directory["E404"]
        self.file_path = root + path

    def get_status_code(self):
        return "404"