
## Logger
# Super simple logging utility
class Logger():
    def __init__(self, loglevel):
        self.loglevel = loglevel


    def log(self, priority, string):
        """ Main logging function. called from everywhere """
        if priority <= self.loglevel:
            print(string)
        
