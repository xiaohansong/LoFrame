class Header(object):
    def __init__(self, status):
        self.first_line = status.generate_first_line()
        self.length_line = ""
        self.cookie_line = ""
        self.connection_line = ""
        self.extra_line = ""
        self.type_line = ""

    def set_first_line(self, status):
        self.status_code = status.get_status_code()
        self.first_line = status.generate_first_line()

    def set_content_length(self, leng):
        self.length_line = "Content-Length: " + str(leng) + "\r\n"

    def set_uuid(self, uuid):
        if(uuid != ""):
            self.cookie_line = "Set-Cookie: uuid=\"" + uuid +"\"\r\n"

    def set_connection_line(self, command):
        self.connection_line = "Connection: " + command + "\r\n"

    def set_extra(self, key, value):
        self.extra_line += key + ": " + value + "\r\n"

    def set_type(self, filetype):
        self.type_line = "Content-Type: " + filetype + "\r\n"

    def get_header(self):
        return self.first_line + self.length_line + self.cookie_line + self.type_line + self.connection_line + self.extra_line+"\r\n"


