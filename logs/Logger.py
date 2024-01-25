import json

import Constants


class Logger:
    def __init__(self, pid, web_c):
        self.pid = pid
        self.file = open("../../"+Constants.LOG_PATH+pid+".txt", 'w')
        self.file.close()
        self.num_versions = 0
        self.web_connector = web_c

    def write(self, line):
        self.file = open("../../"+Constants.LOG_PATH+self.pid+".txt", 'a')
        self.file.write("V"+str(self.num_versions)+": "+line+"\n")
        self.file.close()
        self.num_versions += 1
        msg = {'src': self.pid, 'data': line}
        self.web_connector.send_message(json.dumps(msg))
