from __future__ import unicode_literals

import setting
from modules.core.Utils import Logger
import time
import random

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CollectorFather(object):
    # ------------------------- BEGIN: Building the selenium crawler and the logger every collector will have ------------------------- #
    def __init__(self):
        # Initiating the selenium driver, let's crawl
        self.driver = webdriver.Chrome()

        # A logger that need to instanciate in the daughter class
        self.logger = None

    def __del__(self):
        self.driver.close()
