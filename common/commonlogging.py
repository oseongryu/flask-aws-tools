# -*- coding: utf-8 -*-
import json
import logging
import os
import sys
import time
from datetime import datetime
from logging import handlers


class CommonLogging:
    logger = None

    def __init__(self, logFileName):
        # logFormatter = logging.Formatter("%(asctime)s,%(message)s")
        logFormatter = logging.Formatter("%(message)s")
        logHandler = handlers.TimedRotatingFileHandler(filename=logFileName, when="midnight", interval=1, encoding="utf-8")
        logHandler.setFormatter(logFormatter)
        logHandler.suffix = "%Y%m%d"
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logHandler)
