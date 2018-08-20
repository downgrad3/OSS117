from modules.core.Utils import Logger, Oss117
import setting


class EvaluatorFather(object):
    def __init__(self):
        # A logger because log is life
        self.logger = Logger.initialize_logger(self.__class__.__name__, setting.LOGS_EVALUATORS_DIR)

    def __del__(self):
        return
