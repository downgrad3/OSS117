from modules.core.Utils import Logger
import setting


class EvaluatorFather(object):
    def __init__(self):
        # A logger that need to be instanciated in the daughter class
        self.logger = None

    def __del__(self):
        return
