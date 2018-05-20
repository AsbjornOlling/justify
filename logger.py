
## Logger
# Simple logging utility
class Logger():
    def __init__(self, parent, loglevel):
        self.parent = parent
        self.config = parent.config
        self.logfile = open(self.config.logpath, 'a')


    def log(self, priority, logstring):
        """ Main logging function. called from everywhere """
        # filter according to loglevel
        if priority <= self.loglevel:
            if priority is 0:
                logstring = "[ERROR] " + logstring
            elif priority is 1:
                logstring = "[INFO] " + logstring
            elif priority is 2:
                logstring = "[DEBUG] " + logstring
            elif priority is 3:
                logstring = "[WTF] " + logstring

        self.logfile.write(logstring)
        print(logstring)
