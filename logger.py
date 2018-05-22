
## Logger
# Simple logging utility
class Logger():
    def __init__(self, parent, loglevel):
        self.parent = parent
        self.config = parent.config

        self.loglevel = loglevel
        self.logfile = open(self.config.logpath, 'a')


    def log(self, loglevel, logstring):
        """ Main logging function. called from everywhere """
        # filter according to loglevel
        if self.loglevel >= loglevel:
            if loglevel == 0:
                output = "[ERROR] " + logstring
            elif loglevel == 1:
                output = "[INFO] " + logstring
            elif loglevel == 2:
                output = "[DEBUG] " + logstring
            elif loglevel == 3:
                output = "[WTF] " + logstring

            self.logfile.write(logstring + "\n")
            print(output)
