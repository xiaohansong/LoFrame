class Config(object):
    def __init__(self):
        self.config_directory = {}
        with open("core/conf") as f:
            for line in f.readlines():
                linestr = line[:-1]
                self.config_directory[linestr.split(" = ")[0]] = linestr.split(" = ")[1]
