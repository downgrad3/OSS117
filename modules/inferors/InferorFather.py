import setting
from modules.core.Utils import Logger


class InferorFather(object):
    def __init__(self):
        # A logger that need to be instanciated in the daughter class
        self.logger = None

    def __del__(self):
        return
