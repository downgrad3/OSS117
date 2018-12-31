from __future__ import unicode_literals

import setting
from modules.core.Utils import Logger, Oss117

import time, random
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class CollectorFather(object):
    # ------------------------- BEGIN: Building the selenium crawler and the logger every collector will have ------------------------- #
    def __init__(self):
        # Initiating the selenium driver, let's crawl
        self.driver = webdriver.Chrome()
        # Logger, because log is life
        self.logger = Logger.initialize_logger(self.__class__.__name__, setting.LOGS_COLLECTORS_DIR)

    def __del__(self):
        self.driver.close()
